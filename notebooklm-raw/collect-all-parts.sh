#!/usr/bin/env bash
# 分 Part 采集全部缺失 raw（P1/P5-P9；P2-P4 已完成）
set -uo pipefail
export HTTPS_PROXY=http://127.0.0.1:7897 HTTP_PROXY=http://127.0.0.1:7897
REPO=/home/thesumst/.cursor/worktrees/ai__SSH__wsl_/zodi
NLM=$REPO/.cursor/skills/ai-course-notebooklm/scripts/nlm-collect.py
LOG=$REPO/notebooklm-raw/collect-all-parts.log

cd "$REPO"
echo "=== collect-all-parts $(date -Iseconds) ===" | tee "$LOG"

PARTS=(
  "week1-2"
  "week8"
  "week10"
  "week12"
  "week13-14"
  "week15"
)

for p in "${PARTS[@]}"; do
  echo "--- START $p $(date -Iseconds) ---" | tee -a "$LOG"
  if python3 "$NLM" "notebooklm-raw/manifests/${p}.json" --delay 8 2>&1 | tee -a "$LOG"; then
    echo "--- OK $p ---" | tee -a "$LOG"
  else
    echo "--- FAIL $p (exit $?) ---" | tee -a "$LOG"
  fi
done

echo "=== DONE $(date -Iseconds) ===" | tee -a "$LOG"
