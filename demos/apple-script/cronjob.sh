#!/bin/bash
# 注册每日备忘录的 crontab 任务（每天早上 8 点）。
# 重复执行不会产生重复条目。

set -uo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 走 wrapper 而不是直接 osascript：wrapper 带日志和重试，
# 避免 Notes 偶发失败时静默少一篇备忘录
runner="$SCRIPT_DIR/run_cur_day_note.sh"
entry="0 8 * * * $runner"

if [[ ! -x "$runner" ]]; then
	echo "错误：$runner 不存在或不可执行" >&2
	exit 1
fi

tmp_file=$(mktemp)
trap 'rm -f "$tmp_file"' EXIT

# 没有 crontab 时 crontab -l 会返回非 0，这里不算错误
crontab -l 2>/dev/null >"$tmp_file" || true

if grep -Fq "$runner" "$tmp_file"; then
	echo "Crontab 任务已存在，无需重复添加"
	exit 0
fi

# 清理旧写法（直接调用 osascript 的那条），避免一天跑两次
if grep -q "cur_day_note.scpt" "$tmp_file"; then
	grep -v "cur_day_note.scpt" "$tmp_file" >"$tmp_file.new" && mv "$tmp_file.new" "$tmp_file"
	echo "已移除旧的 osascript 直调任务"
fi

echo "$entry" >>"$tmp_file"
crontab "$tmp_file"

echo "Crontab 任务已添加：$entry"
