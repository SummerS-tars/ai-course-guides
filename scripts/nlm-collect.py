#!/usr/bin/env python3
"""
NotebookLM 分层采集脚本 — 将对话原始内容落盘，运行轨迹可追踪。

用法:
  python scripts/nlm-collect.py manifests/week1-2.json
  python scripts/nlm-collect.py manifests/week1-2.json --only L0-positioning,L1-week1
  python scripts/nlm-collect.py manifests/week1-2.json --dry-run
  python scripts/nlm-collect.py manifests/week1-2.json --resume notebooklm-raw/week1-2/runs/20260609-120000
  python scripts/nlm-collect.py manifests/week1-2.json --delay 5

输出目录:
  notebooklm-raw/<module>/runs/<timestamp>/
    run.meta.json
    run.log
    <batch-id>.prompt.txt
    <batch-id>.answer.md
    <batch-id>.answer.json   # notebooklm ask --json
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# --- Paths ---
REPO_ROOT = Path(__file__).resolve().parent.parent
RAW_ROOT = REPO_ROOT / "notebooklm-raw"
SKILL_DIR = Path.home() / "service/openclaw/workspace/skills/notebooklm-integration"
SYNC_AUTH = SKILL_DIR / "scripts/sync-auth.py"
NOTEBOOKLM_CLI = SKILL_DIR / ".venv/bin/notebooklm"
DEFAULT_PROXY = "http://127.0.0.1:7897"


def log(msg: str, log_file: Path | None = None) -> None:
    line = f"[{datetime.now().strftime('%H:%M:%S')}] {msg}"
    print(line, flush=True)
    if log_file:
        with log_file.open("a", encoding="utf-8") as f:
            f.write(line + "\n")


def run_cmd(
    cmd: list[str],
    *,
    env: dict[str, str] | None = None,
    timeout: int = 180,
) -> subprocess.CompletedProcess[str]:
    merged = os.environ.copy()
    if env:
        merged.update(env)
    return subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        env=merged,
        timeout=timeout,
        check=False,
    )


def ensure_auth(log_file: Path | None) -> None:
    if not SYNC_AUTH.exists():
        raise FileNotFoundError(f"sync-auth 不存在: {SYNC_AUTH}")
    log("同步认证…", log_file)
    r = run_cmd([sys.executable, str(SYNC_AUTH)], timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"sync-auth 失败:\n{r.stdout}\n{r.stderr}")
    log("认证 OK", log_file)


def notebook_use(notebook_id: str, env: dict[str, str], log_file: Path | None) -> None:
    log(f"选定 Notebook: {notebook_id}", log_file)
    r = run_cmd([str(NOTEBOOKLM_CLI), "use", notebook_id], env=env, timeout=60)
    if r.returncode != 0:
        raise RuntimeError(f"notebooklm use 失败:\n{r.stdout}\n{r.stderr}")


def notebook_clear(env: dict[str, str], log_file: Path | None) -> None:
    log("清空会话上下文 (notebooklm clear)", log_file)
    r = run_cmd([str(NOTEBOOKLM_CLI), "clear"], env=env, timeout=30)
    if r.returncode != 0:
        raise RuntimeError(f"notebooklm clear 失败:\n{r.stdout}\n{r.stderr}")


def ask_notebooklm(
    prompt: str,
    notebook_id: str,
    env: dict[str, str],
    log_file: Path | None,
    timeout: int,
) -> dict:
    log(f"提问 ({len(prompt)} 字)…", log_file)
    r = run_cmd(
        [str(NOTEBOOKLM_CLI), "ask", "--json", "-n", notebook_id, prompt],
        env=env,
        timeout=timeout,
    )
    if r.returncode != 0:
        raise RuntimeError(
            f"notebooklm ask 失败 (exit {r.returncode}):\n"
            f"stdout:\n{r.stdout}\nstderr:\n{r.stderr}"
        )
    # CLI 可能在 JSON 前打印 dim 信息，取最后一个 JSON 对象
    text = r.stdout.strip()
    start = text.find("{")
    if start < 0:
        raise RuntimeError(f"未解析到 JSON 输出:\n{text}")
    data = json.loads(text[start:])
    return data


def load_manifest(path: Path) -> dict:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def batch_done(run_dir: Path, batch_id: str) -> bool:
    return (run_dir / f"{batch_id}.answer.json").exists()


def save_batch(
    run_dir: Path,
    batch: dict,
    answer_data: dict,
    elapsed: float,
) -> None:
    bid = batch["id"]
    (run_dir / f"{bid}.prompt.txt").write_text(batch["prompt"], encoding="utf-8")
    answer_text = answer_data.get("answer", "")
    (run_dir / f"{bid}.answer.md").write_text(answer_text, encoding="utf-8")
    payload = {
        "batch_id": bid,
        "layer": batch.get("layer"),
        "title": batch.get("title"),
        "elapsed_seconds": round(elapsed, 2),
        "conversation_id": answer_data.get("conversation_id"),
        "is_follow_up": answer_data.get("is_follow_up"),
        "answer": answer_text,
        "references": answer_data.get("references"),
        "raw": {k: v for k, v in answer_data.items() if k != "raw_response"},
    }
    (run_dir / f"{bid}.answer.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def update_meta(run_dir: Path, meta: dict) -> None:
    (run_dir / "run.meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="NotebookLM 分层采集并落盘")
    parser.add_argument("manifest", type=Path, help="manifest JSON 路径")
    parser.add_argument(
        "--only",
        type=str,
        default="",
        help="逗号分隔的 batch id，仅运行指定批次",
    )
    parser.add_argument("--dry-run", action="store_true", help="只打印计划，不调用 API")
    parser.add_argument(
        "--resume",
        type=Path,
        default=None,
        help="续跑已有 run 目录（跳过已完成 batch）",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=3.0,
        help="批次间等待秒数（默认 3）",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=180,
        help="单次 ask 超时秒数（默认 180）",
    )
    parser.add_argument("--no-auth", action="store_true", help="跳过 sync-auth")
    parser.add_argument(
        "--proxy",
        type=str,
        default=DEFAULT_PROXY,
        help=f"HTTP 代理（默认 {DEFAULT_PROXY}）",
    )
    args = parser.parse_args()

    manifest_path = args.manifest if args.manifest.is_absolute() else REPO_ROOT / args.manifest
    if not manifest_path.exists():
        print(f"manifest 不存在: {manifest_path}", file=sys.stderr)
        return 1

    mf = load_manifest(manifest_path)
    module = mf["module"]
    notebook_id = mf["notebook_id"]
    batches: list[dict] = mf["batches"]
    only_ids = {x.strip() for x in args.only.split(",") if x.strip()}
    if only_ids:
        batches = [b for b in batches if b["id"] in only_ids]
        if not batches:
            print(f"未匹配到 batch: {only_ids}", file=sys.stderr)
            return 1

    if args.resume:
        run_dir = args.resume if args.resume.is_absolute() else REPO_ROOT / args.resume
    else:
        ts = datetime.now().strftime("%Y%m%d-%H%M%S")
        run_dir = RAW_ROOT / module / "runs" / ts

    if args.dry_run:
        run_dir_display = run_dir
        log_file = None
        log(f"模块: {module} | 批次数: {len(batches)} | 将输出到: {run_dir_display}")
        for i, b in enumerate(batches, 1):
            log(
                f"  {i}. [{b.get('layer','?')}] {b['id']} "
                f"clear={b.get('clear_conversation', False)}"
            )
        log("dry-run 结束")
        return 0

    run_dir.mkdir(parents=True, exist_ok=True)
    log_file = run_dir / "run.log"

    # 写入 manifest 快照
    (run_dir / "manifest.snapshot.json").write_text(
        json.dumps(mf, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    meta = {
        "module": module,
        "notebook_id": notebook_id,
        "manifest": str(manifest_path.relative_to(REPO_ROOT))
        if manifest_path.is_relative_to(REPO_ROOT)
        else str(manifest_path),
        "run_dir": str(run_dir.relative_to(REPO_ROOT))
        if run_dir.is_relative_to(REPO_ROOT)
        else str(run_dir),
        "started_at": datetime.now(timezone.utc).isoformat(),
        "finished_at": None,
        "batches": [],
        "status": "running",
    }
    update_meta(run_dir, meta)

    log(f"模块: {module} | 批次数: {len(batches)} | 输出: {run_dir}", log_file)

    if not NOTEBOOKLM_CLI.exists():
        print(f"notebooklm CLI 不存在: {NOTEBOOKLM_CLI}", file=sys.stderr)
        return 1

    proxy_env = {
        "HTTP_PROXY": args.proxy,
        "HTTPS_PROXY": args.proxy,
    }

    try:
        if not args.no_auth:
            ensure_auth(log_file)
        notebook_use(notebook_id, proxy_env, log_file)

        for i, batch in enumerate(batches, 1):
            bid = batch["id"]
            if args.resume and batch_done(run_dir, bid):
                log(f"跳过已完成 batch {i}/{len(batches)}: {bid}", log_file)
                meta["batches"].append({"id": bid, "status": "skipped"})
                update_meta(run_dir, meta)
                continue

            log(f"--- batch {i}/{len(batches)}: [{batch.get('layer')}] {bid} ---", log_file)

            if batch.get("clear_conversation"):
                notebook_clear(proxy_env, log_file)

            t0 = time.time()
            try:
                answer_data = ask_notebooklm(
                    batch["prompt"],
                    notebook_id,
                    proxy_env,
                    log_file,
                    args.timeout,
                )
                elapsed = time.time() - t0
                save_batch(run_dir, batch, answer_data, elapsed)
                log(f"完成 {bid} ({elapsed:.1f}s)", log_file)
                meta["batches"].append(
                    {
                        "id": bid,
                        "layer": batch.get("layer"),
                        "status": "ok",
                        "elapsed_seconds": round(elapsed, 2),
                        "conversation_id": answer_data.get("conversation_id"),
                    }
                )
            except Exception as e:
                elapsed = time.time() - t0
                log(f"失败 {bid} ({elapsed:.1f}s): {e}", log_file)
                meta["batches"].append(
                    {
                        "id": bid,
                        "layer": batch.get("layer"),
                        "status": "error",
                        "error": str(e),
                        "elapsed_seconds": round(elapsed, 2),
                    }
                )
                meta["status"] = "partial_error"
                meta["finished_at"] = datetime.now(timezone.utc).isoformat()
                update_meta(run_dir, meta)
                raise

            update_meta(run_dir, meta)
            if i < len(batches) and args.delay > 0:
                log(f"等待 {args.delay}s…", log_file)
                time.sleep(args.delay)

        meta["status"] = "completed"
        meta["finished_at"] = datetime.now(timezone.utc).isoformat()
        update_meta(run_dir, meta)
        log("全部完成", log_file)
        return 0

    except Exception as e:
        log(f"运行中止: {e}", log_file)
        meta["status"] = meta.get("status", "error")
        meta["finished_at"] = datetime.now(timezone.utc).isoformat()
        meta["error"] = str(e)
        update_meta(run_dir, meta)
        return 1


if __name__ == "__main__":
    sys.exit(main())
