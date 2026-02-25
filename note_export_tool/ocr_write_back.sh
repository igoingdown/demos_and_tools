#!/bin/bash
# ============================================================
# 将 OCR 结果追加写回到对应备忘录末尾
# 用法：bash writeback_ocr.sh [备忘录导出目录]
# ============================================================

NOTES_EXPORT_DIR="${1:-$HOME/Desktop/notes_export}"

echo "📁 导出目录：$NOTES_EXPORT_DIR"
echo "⏳ 开始将 OCR 结果写回备忘录..."

python3 - "$NOTES_EXPORT_DIR" <<'PYEOF'
import sys, os, subprocess, tempfile

notes_export_dir = sys.argv[1]
WRITEBACK_MARKER = "【手写内容 OCR 识别结果】"

def run_applescript(script):
    tmp = tempfile.NamedTemporaryFile(
        suffix=".applescript", mode='w', encoding='utf-8', delete=False
    )
    tmp.write(script)
    tmp.close()
    try:
        result = subprocess.run(
            ["osascript", tmp.name],
            capture_output=True, text=True
        )
        return result.stdout.strip(), result.stderr.strip()
    finally:
        os.unlink(tmp.name)

def as_str(s):
    """
    Python 字符串 → AppleScript 字符串字面量。
    处理双引号、反斜杠、换行（换行用 ASCII character 10 拼接）。
    """
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    parts = s.split('\n')
    as_parts = [f'"{p}"' for p in parts]
    return ' & (ASCII character 10) & '.join(as_parts)

def get_note_body(folder_name, note_title):
    """
    遍历所有账户查找文件夹，不依赖账户名，避免数据库名与 App 名不一致问题。
    """
    script = f'''tell application "Notes"
    set targetFolder to missing value
    repeat with a in accounts
        repeat with f in folders of a
            if name of f is {as_str(folder_name)} then
                set targetFolder to f
                exit repeat
            end if
        end repeat
        if targetFolder is not missing value then exit repeat
    end repeat
    if targetFolder is missing value then
        error "找不到文件夹: {folder_name}"
    end if
    set theNote to first note of targetFolder whose name is {as_str(note_title)}
    return body of theNote
end tell
'''
    return run_applescript(script)

def append_to_note(folder_name, note_title, ocr_text):
    current_body, err = get_note_body(folder_name, note_title)
    if err and not current_body:
        return False, f"读取失败：{err}"

    if WRITEBACK_MARKER in current_body:
        return None, "已写回，跳过"

    # 构造追加 HTML（无原始换行，全部在一行内）
    ocr_lines = ocr_text.strip().split('\n')
    ocr_html = ''.join(
        f'<div>{line if line.strip() else "&nbsp;"}</div>'
        for line in ocr_lines
    )
    append_html = (
        '<div><br></div>'
        '<div>──────────────────────</div>'
        f'<div>{WRITEBACK_MARKER}</div>'
        '<div>以下为 AI OCR 识别的手写内容，仅供参考：</div>'
        '<div><br></div>'
        + ocr_html
    )
    new_body = current_body + append_html

    script = f'''tell application "Notes"
    set targetFolder to missing value
    repeat with a in accounts
        repeat with f in folders of a
            if name of f is {as_str(folder_name)} then
                set targetFolder to f
                exit repeat
            end if
        end repeat
        if targetFolder is not missing value then exit repeat
    end repeat
    if targetFolder is missing value then
        error "找不到文件夹: {folder_name}"
    end if
    set theNote to first note of targetFolder whose name is {as_str(note_title)}
    set body of theNote to {as_str(new_body)}
end tell
'''
    out, err = run_applescript(script)
    if err and 'error' in err.lower():
        return False, f"写入失败：{err}"
    return True, "成功"

# ── 检查权限 ──────────────────────────────────────────────
print("🔍 检查备忘录访问权限...")
out, err = run_applescript('tell application "Notes" to return name of first account')
if err and not out:
    print(f"❌ 无法访问备忘录：{err}")
    print("   系统设置 → 隐私与安全性 → 自动化 → 终端 → 备忘录 开启")
    sys.exit(1)
print(f"✅ 备忘录访问正常\n")

# ── 遍历导出目录 ──────────────────────────────────────────
total = success = skipped = failed = 0
fail_log = []

for account_dir in sorted(os.listdir(notes_export_dir)):
    account_path = os.path.join(notes_export_dir, account_dir)
    if not os.path.isdir(account_path):
        continue
    for folder_dir in sorted(os.listdir(account_path)):
        folder_path = os.path.join(account_path, folder_dir)
        if not os.path.isdir(folder_path):
            continue
        for entry in sorted(os.listdir(folder_path)):
            if not entry.endswith("_attachments"):
                continue
            ocr_file = os.path.join(folder_path, entry, "手写内容_OCR.txt")
            if not os.path.isfile(ocr_file):
                continue

            note_title_safe = entry[:-len("_attachments")]
            txt_file = os.path.join(folder_path, note_title_safe + ".txt")
            real_title = note_title_safe
            if os.path.isfile(txt_file):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    first_line = f.readline().strip()
                    if first_line.startswith("标题："):
                        real_title = first_line[len("标题："):]

            with open(ocr_file, 'r', encoding='utf-8') as f:
                ocr_text = f.read().strip()
            if not ocr_text or ocr_text == "（无文字内容）":
                continue

            total += 1
            print(f"  [{total}] 「{real_title}」[{folder_dir}]", end=" ", flush=True)

            # 写回时只用文件夹名查找，不依赖账户名
            ok, msg = append_to_note(folder_dir, real_title, ocr_text)
            if ok is True:
                print(f"✅ {msg}"); success += 1
            elif ok is None:
                print(f"⏭  {msg}"); skipped += 1
            else:
                print(f"❌ {msg}"); failed += 1
                fail_log.append(f"[{folder_dir}] 「{real_title}」：{msg}")

# ── 汇总 ──────────────────────────────────────────────────
print(f"\n{'═'*55}")
print(f"✅ 写回完成！成功：{success} 条", end="")
if skipped: print(f"  跳过：{skipped} 条", end="")
if failed:  print(f"  失败：{failed} 条", end="")
print()
if fail_log:
    for line in fail_log:
        print(f"   {line}")

PYEOF

echo ""
echo "🎉 脚本执行结束"