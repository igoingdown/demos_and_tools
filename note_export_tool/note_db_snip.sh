#!/bin/bash
# 探查 Notes 数据库结构

python3 << 'PYEOF'
import os, shutil, sqlite3, tempfile

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
cur  = conn.cursor()

# 所有表
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r[0] for r in cur.fetchall()]
print("=== 所有表 ===")
for t in tables:
    print(" ", t)

# 每张表的列名
print("\n=== 各表列名 ===")
for t in tables:
    cur.execute(f"PRAGMA table_info('{t}')")
    cols = [r[1] for r in cur.fetchall()]
    print(f"\n[{t}]")
    print("  " + ", ".join(cols))

conn.close()
shutil.rmtree(tmp_dir)
PYEOF
