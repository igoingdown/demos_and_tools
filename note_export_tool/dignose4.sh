#!/bin/bash
python3 << 'PYEOF'
import os, shutil, sqlite3, tempfile, zlib, re

db_path = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
)
tmp_dir = tempfile.mkdtemp()
tmp_db  = os.path.join(tmp_dir, "NoteStore.sqlite")
shutil.copy2(db_path, tmp_db)
for ext in ("-wal", "-shm"):
    src = db_path + ext
    if os.path.exists(src):
        shutil.copy2(src, tmp_db + ext)

conn = sqlite3.connect(tmp_db)
conn.row_factory = sqlite3.Row
cur = conn.cursor()

cur.execute("""
    SELECT n.Z_PK, n.ZTITLE1, d.ZDATA
    FROM ZICCLOUDSYNCINGOBJECT n
    LEFT JOIN ZICNOTEDATA d ON d.ZNOTE = n.Z_PK
    WHERE n.ZTITLE1 = '高考手机作弊'
    LIMIT 1
""")
row = cur.fetchone()
raw = row["ZDATA"]
idx = raw.find(b'\x1f\x8b')
decompressed = zlib.decompress(raw[idx:], 16 + zlib.MAX_WBITS)

print(f"解压后总长度: {len(decompressed)} bytes")
print(f"\n=== 完整 hex dump ===")
for i in range(0, len(decompressed), 16):
    chunk = decompressed[i:i+16]
    hex_part = ' '.join(f'{b:02x}' for b in chunk)
    # 可打印字符显示原字符，否则显示点
    def show(b):
        if 0x20 <= b <= 0x7e:
            return chr(b)
        try:
            # 尝试 UTF-8 中文
            return '·'
        except:
            return '.'
    ascii_part = ''.join(show(b) for b in chunk)
    print(f"  {i:04x}  {hex_part:<47}  {ascii_part}")

print(f"\n=== 正文结束后的 bytes（找到最后一个中文字符之后的内容）===")
# 找最后一个中文字符的位置
text = decompressed.decode('utf-8', errors='replace')
last_cjk = -1
for i, c in enumerate(text):
    if '\u4e00' <= c <= '\u9fff':
        last_cjk = i

if last_cjk >= 0:
    print(f"最后中文字符位置(字符索引): {last_cjk}, 字符: '{text[last_cjk]}'")
    after_text = text[last_cjk+1:last_cjk+200]
    print(f"之后的内容(repr): {repr(after_text)}")
    
    # 转换回 bytes 位置
    before_bytes = text[:last_cjk+1].encode('utf-8', errors='replace')
    byte_pos = len(before_bytes)
    print(f"对应 bytes 位置: {byte_pos}")
    after_bytes = decompressed[byte_pos:byte_pos+100]
    print(f"之后的 bytes(hex): {' '.join(f'{b:02x}' for b in after_bytes)}")

conn.close()
shutil.rmtree(tmp_dir)
PYEOF
