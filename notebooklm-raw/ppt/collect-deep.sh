#!/usr/bin/env bash
# 续跑 PPT 深采：自动 resume 未完成 run，日志落盘
set -euo pipefail
cd "$(dirname "$0")/../.."
export HTTPS_PROXY="${HTTPS_PROXY:-http://127.0.0.1:7897}"
export HTTP_PROXY="${HTTP_PROXY:-$HTTPS_PROXY}"
NLM=.cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py
LOG=notebooklm-raw/ppt/collect-deep.log

manifests=(
  ppt01-deep ppt02-deep ppt04-deep ppt06-deep
  ppt08-deep ppt09-deep ppt10-deep
)

exec > >(tee -a "$LOG") 2>&1
echo "=== $(date -Iseconds) collect-deep start ==="

for m in "${manifests[@]}"; do
  mod="${m%-deep}"
  manifest="notebooklm-raw/manifests/${m}.json"
  run_root="notebooklm-raw/${mod}/runs"

  latest=""
  if [ -d "$run_root/latest" ]; then
    latest=$(readlink -f "$run_root/latest" 2>/dev/null || true)
  fi
  # 无 latest 软链时：取最近 run 目录
  if [ -z "$latest" ] && [ -d "$run_root" ]; then
    latest=$(ls -td "$run_root"/202* 2>/dev/null | head -1 || true)
  fi

  if [ -n "$latest" ] && [ -f "$latest/run.meta.json" ]; then
    status=$(python3 -c "import json; print(json.load(open('$latest/run.meta.json')).get('status',''))")
    if [ "$status" = "completed" ]; then
      echo "[skip] $m already completed at $latest"
      continue
    fi
    echo "[resume] $m from $latest (status=$status)"
    python3 "$NLM" "$manifest" --resume "$latest" --delay 6
  else
    echo "[new] $m"
    python3 "$NLM" "$manifest" --delay 6
  fi
done

echo "=== $(date -Iseconds) collect-deep done ==="
