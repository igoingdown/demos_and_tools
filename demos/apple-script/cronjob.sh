#!/bin/bash

# 定义要执行的AppleScript脚本的路径
script_path="$HOME/github/python_demo_and_tool/demos/apple-script/cur_day_note.scpt"

# 创建一个临时文件来存储当前的Crontab任务
tmp_file=$(mktemp)

# 将现有的Crontab任务导出到临时文件中
crontab -l > "$tmp_file"

# 在临时文件中添加新的Crontab任务（每天早上8点执行指定的AppleScript脚本）
echo "0 8 * * * osascript $script_path" >> "$tmp_file"

# 将临时文件中的内容加载回Crontab
crontab "$tmp_file"

# 删除临时文件
rm "$tmp_file"

echo "Crontab任务已添加"
