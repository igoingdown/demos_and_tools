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
    WHERE n.ZTITLE1 = '问题'
    LIMIT 1
""")
row = cur.fetchone()
raw = row["ZDATA"]
idx = raw.find(b'\x1f\x8b')
decompressed = zlib.decompress(raw[idx:], 16 + zlib.MAX_WBITS)

print(f"解压后总长度: {len(decompressed)} bytes")
print(f"\n=== 完整原始内容(repr) ===")
print(repr(decompressed))

print(f"\n=== 尝试 UTF-8 解码（replace模式）===")
text = decompressed.decode('utf-8', errors='replace')
print(repr(text))

# 看看里面有哪些可打印字符串（长度>=4）
print(f"\n=== 提取所有可打印字符串(长度>=4) ===")
strings = re.findall(r'[ -~\u4e00-\u9fff]{4,}', text)
for s in strings:
    print(f"  {repr(s)}")

conn.close()
shutil.rmtree(tmp_dir)
PYEOF