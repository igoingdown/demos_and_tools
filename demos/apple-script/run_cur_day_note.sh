#!/bin/bash
# cur_day_note.scpt 的 cron 包装：带日志和重试。
#
# 解决的问题：Notes 的 AppleEvent 调用会偶发失败（观测到 -1712 超时、-10000
# 处理程序失败）。直接在 crontab 里跑 osascript 时，失败只进本地邮件，实际
# 表现就是某天悄悄少了一篇备忘录。
#
# 重试安全性依赖 cur_day_note.scpt 的幂等性：该脚本只创建不存在的标题，
# 所以重跑不会产生重复条目，部分成功（如周日多篇里失败了一篇）也能补齐。
#
# 用法：0 8 * * * /path/to/run_cur_day_note.sh

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCPT="$SCRIPT_DIR/cur_day_note.scpt"

LOG_DIR="${NOTE_LOG_DIR:-$HOME/Library/Logs/cur_day_note}"
LOG_FILE="$LOG_DIR/cur_day_note.log"

MAX_ATTEMPTS="${NOTE_MAX_ATTEMPTS:-5}"
RETRY_DELAY="${NOTE_RETRY_DELAY:-60}"

mkdir -p "$LOG_DIR"

log() {
	printf '%s [%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" "$2" >>"$LOG_FILE"
}

if [[ ! -f "$SCPT" ]]; then
	log ERROR "脚本不存在: $SCPT"
	exit 1
fi

log INFO "开始"

for ((attempt = 1; attempt <= MAX_ATTEMPTS; attempt++)); do
	out=$(osascript "$SCPT" 2>&1)
	rc=$?

	if [[ $rc -eq 0 ]]; then
		log INFO "成功（第 $attempt 次尝试）${out:+: $out}"
		exit 0
	fi

	log WARN "第 $attempt/$MAX_ATTEMPTS 次尝试失败 (rc=$rc): $out"

	if [[ $attempt -lt $MAX_ATTEMPTS ]]; then
		log INFO "等待 ${RETRY_DELAY}s 后重试"
		sleep "$RETRY_DELAY"
	fi
done

log ERROR "重试 $MAX_ATTEMPTS 次后仍失败，备忘录可能未创建"

# 失败时弹通知，避免静默丢失
osascript -e 'display notification "每日备忘录创建失败，详见日志" with title "cur_day_note"' \
	>/dev/null 2>&1 || true

exit 1
