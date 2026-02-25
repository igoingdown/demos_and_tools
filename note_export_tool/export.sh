#!/bin/bash
# ============================================================
# Mac 备忘录导出脚本（跳过智能文件夹）
# 用法：bash export_notes.sh [输出目录]
# 默认输出到 ~/Desktop/notes_export
# ============================================================

OUTPUT_DIR="${1:-$HOME/Desktop/notes_export}"
mkdir -p "$OUTPUT_DIR"

echo "📁 导出目录：$OUTPUT_DIR"
echo "⏳ 正在读取备忘录数据库..."

python3 - "$OUTPUT_DIR" <<'PYEOF'
import sys, os, re, shutil, sqlite3, tempfile, zlib
from datetime import datetime, timezone

output_dir = sys.argv[1]

# ── 工具函数 ──────────────────────────────────────────────
def safe_name(s, max_len=80):
    s = re.sub(r'[/\\:*?"<>|\x00-\x1f]', '_', s)
    s = s.strip('. ')
    return s[:max_len] if s else "untitled"

def write_text(path, content):
    base, ext = os.path.splitext(path)
    counter = 1
    actual = path
    while os.path.exists(actual):
        actual = f"{base}_{counter}{ext}"
        counter += 1
    with open(actual, 'w', encoding='utf-8') as f:
        f.write(content)
    return actual

def copy_file(src, dst_dir, filename):
    base, ext = os.path.splitext(filename)
    dst = os.path.join(dst_dir, filename)
    counter = 1
    while os.path.exists(dst):
        dst = os.path.join(dst_dir, f"{base}_{counter}{ext}")
        counter += 1
    shutil.copy2(src, dst)
    return dst

def apple_ts(ts):
    if ts is None:
        return "未知"
    try:
        base = datetime(2001, 1, 1, tzinfo=timezone.utc).timestamp()
        return datetime.fromtimestamp(base + float(ts)).strftime('%Y-%m-%d %H:%M:%S')
    except:
        return str(ts)

def read_varint(data, pos):
    """读取 protobuf varint，返回 (值, 新pos)"""
    result = 0
    shift = 0
    while pos < len(data):
        b = data[pos]
        pos += 1
        result |= (b & 0x7F) << shift
        shift += 7
        if not (b & 0x80):
            break
    return result, pos

def extract_text_from_proto(data):
    """
    从 Notes protobuf 中精确提取正文文本。
    
    结构分析（来自 hex dump）：
      外层 field 1 (0x08): varint
      外层 field 2 (0x12): length-delimited → 这是正文容器
        内层 field 1 (0x08): varint
        内层 field 2 (0x10): varint  
        内层 field 3 (0x1a): length-delimited → 这是正文文本字符串
          正文 field 2 (0x12): length-delimited → 实际文字内容
          正文 field 3 (0x1a): length-delimited → 格式 ranges（不要）
    
    策略：找外层 field 2 (0x12) 的内容块，在其中找 field 3 (0x1a)，
    再在其中取第一个 field 2 (0x12) 的字符串，即为纯文本。
    """
    try:
        pos = 0
        n = len(data)

        # 跳过外层 field 1 (tag=0x08, varint)
        if pos < n and data[pos] == 0x08:
            pos += 1
            _, pos = read_varint(data, pos)

        # 读外层 field 2 (tag=0x12, length-delimited) → 正文容器
        if pos >= n or data[pos] != 0x12:
            return None
        pos += 1
        outer_len, pos = read_varint(data, pos)
        outer_data = data[pos: pos + outer_len]

        # 在 outer_data 里找 field 3 (tag=0x1a)
        # outer_data 结构：field1(0x08) + field2(0x10) + field3(0x1a: 正文blob)
        p = 0
        on = len(outer_data)

        # 跳过 field 1 (0x08)
        if p < on and outer_data[p] == 0x08:
            p += 1
            _, p = read_varint(outer_data, p)

        # 跳过 field 2 (0x10)
        if p < on and outer_data[p] == 0x10:
            p += 1
            _, p = read_varint(outer_data, p)

        # 读 field 3 (0x1a) → 正文 blob
        if p >= on or outer_data[p] != 0x1a:
            return None
        p += 1
        inner_len, p = read_varint(outer_data, p)
        inner_data = outer_data[p: p + inner_len]

        # inner_data 结构：
        #   field 2 (0x12): 纯文本字符串  ← 只取这个
        #   field 3 (0x1a): 格式 ranges  ← 忽略
        ip = 0
        in_n = len(inner_data)

        # 跳过可能的 field 1
        if ip < in_n and inner_data[ip] == 0x08:
            ip += 1
            _, ip = read_varint(inner_data, ip)

        # 读 field 2 (0x12) → 纯文本
        if ip >= in_n or inner_data[ip] != 0x12:
            return None
        ip += 1
        text_len, ip = read_varint(inner_data, ip)
        text_bytes = inner_data[ip: ip + text_len]

        return text_bytes.decode('utf-8', errors='replace').strip()

    except Exception:
        return None

def html_to_plain(html):
    html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'</(p|div|li|h\d|tr)>', '\n', html, flags=re.IGNORECASE)
    html = re.sub(r'<[^>]+>', '', html)
    html = html.replace('&nbsp;', ' ').replace('&amp;', '&') \
               .replace('&lt;', '<').replace('&gt;', '>') \
               .replace('&quot;', '"').replace('&#39;', "'")
    html = re.sub(r'\n{3,}', '\n\n', html)
    return html.strip()

def decode_note_data(raw):
    """
    解压 ZDATA，双路径提取文本：
    路径1：含 HTML → HTML 解析，精确截断到最后关闭标签
    路径2：纯 protobuf → 精确解析 proto 结构，只取正文字段
    """
    if raw is None:
        return None
    try:
        idx = raw.find(b'\x1f\x8b')
        if idx == -1:
            return None
        decompressed = zlib.decompress(raw[idx:], 16 + zlib.MAX_WBITS)

        # ── 路径1：含 HTML ────────────────────────────────
        html_start = re.search(rb'<(html|body|div|p)[^>]{0,200}>', decompressed, re.IGNORECASE)
        if html_start:
            text = decompressed.decode('utf-8', errors='replace')
            end_tags = list(re.finditer(r'</(html|body|div|p|ul|ol)>', text, re.IGNORECASE))
            if end_tags:
                text = text[html_start.start(): end_tags[-1].end()]
            else:
                text = text[html_start.start():]
            return html_to_plain(text)

        # ── 路径2：精确解析 protobuf 结构 ─────────────────
        return extract_text_from_proto(decompressed)

    except Exception:
        return None

def uti_to_desc(uti):
    if not uti: return '附件'
    u = uti.lower()
    if 'drawing' in u or 'sketch' in u: return '手写涂鸦'
    if 'jpeg' in u or 'jpg' in u:       return '图片(jpg)'
    if 'png'  in u:                      return '图片(png)'
    if 'heic' in u or 'heif' in u:      return '图片(heic)'
    if 'gif'  in u:                      return '图片(gif)'
    if 'tiff' in u:                      return '图片(tiff)'
    if 'quicktime' in u or 'movie' in u: return '视频(mov)'
    if 'mpeg-4' in u or 'mp4' in u:     return '视频(mp4)'
    if 'mp3'  in u:                      return '音频(mp3)'
    if 'm4a'  in u:                      return '音频(m4a)'
    if 'aiff' in u:                      return '音频(aiff)'
    if 'pdf'  in u:                      return 'PDF'
    if 'scan' in u:                      return '扫描件'
    if 'plain-text' in u:               return '文本'
    if 'html' in u:                      return '网页'
    return uti

def is_drawing(uti):
    return uti and ('drawing' in uti.lower() or 'sketch' in uti.lower())

# ── 复制数据库 ────────────────────────────────────────────
db_path = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
)
notes_base = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/"
)

if not os.path.exists(db_path):
    print(f"❌ 找不到备忘录数据库：{db_path}")
    sys.exit(1)

print(f"✅ 数据库：{db_path}\n")

tmp_dir = tempfile.mkdtemp()
tmp_db  = os.path.join(tmp_dir, "NoteStore.sqlite")
shutil.copy2(db_path, tmp_db)
for ext in ("-wal", "-shm"):
    src = db_path + ext
    if os.path.exists(src):
        shutil.copy2(src, tmp_db + ext)

total_notes       = 0
total_attachments = 0
empty_body        = 0
errors            = []
notes_with_att    = []

try:
    conn = sqlite3.connect(tmp_db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT
            f.Z_PK    AS folder_id,
            f.ZTITLE2 AS folder_name,
            a.ZNAME   AS account_name
        FROM ZICCLOUDSYNCINGOBJECT f
        LEFT JOIN ZICCLOUDSYNCINGOBJECT a ON f.ZACCOUNT4 = a.Z_PK
        WHERE f.ZFOLDERTYPE IS NOT NULL
          AND f.ZSMARTFOLDERQUERYJSON IS NULL
          AND (f.ZMARKEDFORDELETION IS NULL OR f.ZMARKEDFORDELETION = 0)
        ORDER BY account_name, folder_name
    """)
    folders = cur.fetchall()
    print(f"📂 找到 {len(folders)} 个普通文件夹（已跳过智能文件夹）\n")

    for folder in folders:
        folder_id    = folder["folder_id"]
        folder_name  = folder["folder_name"] or "未命名文件夹"
        account_name = folder["account_name"] or "本地账户"

        dir_path = os.path.join(output_dir, safe_name(account_name), safe_name(folder_name))
        os.makedirs(dir_path, exist_ok=True)

        cur.execute("""
            SELECT
                n.Z_PK               AS note_id,
                n.ZTITLE1            AS title,
                n.ZCREATIONDATE1     AS created,
                n.ZMODIFICATIONDATE1 AS modified,
                d.ZDATA              AS zdata
            FROM ZICCLOUDSYNCINGOBJECT n
            LEFT JOIN ZICNOTEDATA d ON d.ZNOTE = n.Z_PK
            WHERE n.ZFOLDER = ?
              AND n.ZNOTE IS NULL
              AND (n.ZMARKEDFORDELETION IS NULL OR n.ZMARKEDFORDELETION = 0)
        """, (folder_id,))
        notes = cur.fetchall()

        print(f"  📁 [{account_name}] / {folder_name} — {len(notes)} 条")

        for note in notes:
            try:
                note_id  = note["note_id"]
                title    = (note["title"] or "untitled").strip()
                created  = apple_ts(note["created"])
                modified = apple_ts(note["modified"])

                plain = decode_note_data(note["zdata"])
                if not plain:
                    plain = "（内容为空或无法解析）"
                    empty_body += 1

                file_path = os.path.join(dir_path, safe_name(title) + ".txt")
                write_text(file_path, (
                    f"标题：{title}\n"
                    f"创建：{created}\n"
                    f"修改：{modified}\n"
                    f"文件夹：{account_name} / {folder_name}\n"
                    f"{'─' * 40}\n\n"
                    f"{plain}\n"
                ))
                total_notes += 1

                # ── 附件 ──────────────────────────────────
                cur.execute("""
                    SELECT
                        Z_PK        AS att_pk,
                        ZTYPEUTI    AS uti,
                        ZFILENAME   AS filename,
                        ZIDENTIFIER AS identifier
                    FROM ZICCLOUDSYNCINGOBJECT
                    WHERE ZNOTE = ?
                      AND ZTYPEUTI IS NOT NULL
                      AND ZATTACHMENT IS NULL
                      AND (ZMARKEDFORDELETION IS NULL OR ZMARKEDFORDELETION = 0)
                """, (note_id,))
                attachments = cur.fetchall()

                if not attachments:
                    continue

                att_dir = os.path.join(dir_path, safe_name(title) + "_attachments")
                os.makedirs(att_dir, exist_ok=True)

                type_count  = {}
                exported    = 0
                drawing_cnt = 0

                for att in attachments:
                    uti        = att["uti"] or ''
                    filename   = att["filename"] or ''
                    identifier = att["identifier"] or ''
                    desc       = uti_to_desc(uti)

                    type_count[desc] = type_count.get(desc, 0) + 1
                    total_attachments += 1

                    if is_drawing(uti):
                        drawing_cnt += 1
                        placeholder = os.path.join(att_dir, f"手写涂鸦_{drawing_cnt}.txt")
                        write_text(placeholder,
                            f"此附件为 Apple 手写涂鸦（UTI: {uti}）\n"
                            f"identifier: {identifier}\n"
                            f"手写数据存储于数据库私有格式，无法直接导出为图片。\n"
                            f"请在「备忘录」App 中打开「{title}」查看。\n"
                        )
                        exported += 1
                        continue

                    if not identifier:
                        continue

                    media_path = os.path.join(notes_base, "Media", identifier)
                    if not os.path.isdir(media_path):
                        continue

                    for root, dirs, files in os.walk(media_path):
                        for fname in files:
                            src_file = os.path.join(root, fname)
                            copy_file(src_file, att_dir, fname)
                            exported += 1

                notes_with_att.append((title, f"{account_name}/{folder_name}", type_count, exported))

            except Exception as e:
                errors.append(f"[{account_name}/{folder_name}] {note['title']}：{e}")

    conn.close()

except sqlite3.OperationalError as e:
    print(f"\n❌ 数据库读取失败：{e}")
    shutil.rmtree(tmp_dir, ignore_errors=True)
    sys.exit(1)

finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)

print(f"\n{'═' * 55}")
print(f"✅ 导出完成！共 {total_notes} 条备忘录，{total_attachments} 个附件")
if empty_body:
    print(f"⚠️  {empty_body} 条内容为空（可能是加密备忘录）")

if notes_with_att:
    print(f"\n📎 含附件的备忘录（共 {len(notes_with_att)} 条）：")
    for title, folder_path, type_count, exported in notes_with_att:
        type_summary = '、'.join(f"{desc} {cnt} 个" for desc, cnt in type_count.items())
        print(f"   ▸ 「{title}」[{folder_path}]")
        print(f"     附件：{type_summary}（导出 {exported} 个）")

print(f"\n📂 位置：{output_dir}")

if errors:
    log_path = os.path.join(output_dir, "_export_errors.log")
    with open(log_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(errors))
    print(f"⚠️  {len(errors)} 条出错，详见：{log_path}")

PYEOF

echo ""
echo "🎉 脚本执行结束"