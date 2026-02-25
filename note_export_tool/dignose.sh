#!/bin/bash
# 诊断脚本：查明附件结构和报错根因

python3 << 'PYEOF'
import os, shutil, sqlite3, tempfile, zlib, re

db_path = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/NoteStore.sqlite"
)
notes_base = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/"
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

# ── 1. 查一条名字含日期格式的备忘录，看 note_id 类型和附件行 ──
print("=== 问题备忘录（标题含 Monday/Wednesday 等）的 note_id 字段类型 ===")
cur.execute("""
    SELECT Z_PK, ZTITLE1, ZNOTE, ZFOLDER, ZFOLDERTYPE, ZTYPEUTI
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZTITLE1 LIKE '%Monday%' OR ZTITLE1 LIKE '%Wednesday%' OR ZTITLE1 LIKE '%Saturday%'
    LIMIT 5
""")
rows = cur.fetchall()
for r in rows:
    print(f"  Z_PK={r['Z_PK']} (type={type(r['Z_PK']).__name__})  ZTITLE1={r['ZTITLE1']}  ZNOTE={r['ZNOTE']}  ZFOLDER={r['ZFOLDER']}  ZFOLDERTYPE={r['ZFOLDERTYPE']}  ZTYPEUTI={r['ZTYPEUTI']}")

# ── 2. 看 ZNOTE IS NULL 过滤是否有问题 ──
print("\n=== ZNOTE 字段的值分布（前20条）===")
cur.execute("""
    SELECT ZNOTE, ZFOLDER, ZTITLE1, ZFOLDERTYPE, ZTYPEUTI
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZMARKEDFORDELETION IS NULL OR ZMARKEDFORDELETION = 0
    LIMIT 20
""")
for r in cur.fetchall():
    print(f"  ZNOTE={r['ZNOTE']}  ZFOLDER={r['ZFOLDER']}  TITLE={r['ZTITLE1']}  FOLDERTYPE={r['ZFOLDERTYPE']}  UTI={r['ZTYPEUTI']}")

# ── 3. 找一条有手写附件的备忘录，看附件行长什么样 ──
print("\n=== 含 drawing/sketch/handwrit 类 UTI 的行 ===")
cur.execute("""
    SELECT Z_PK, ZTITLE1, ZNOTE, ZFOLDER, ZTYPEUTI, ZFILENAME, ZIDENTIFIER, ZGENERATION1
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZTYPEUTI LIKE '%draw%' OR ZTYPEUTI LIKE '%sketch%' OR ZTYPEUTI LIKE '%handwrit%' OR ZTYPEUTI LIKE '%ink%'
    LIMIT 10
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  Z_PK={r['Z_PK']}  ZNOTE={r['ZNOTE']}  ZFOLDER={r['ZFOLDER']}  UTI={r['ZTYPEUTI']}  FILE={r['ZFILENAME']}  ID={r['ZIDENTIFIER']}  GEN={r['ZGENERATION1']}")
else:
    print("  （未找到，尝试扩大搜索）")
    cur.execute("""
        SELECT DISTINCT ZTYPEUTI FROM ZICCLOUDSYNCINGOBJECT
        WHERE ZTYPEUTI IS NOT NULL AND ZNOTE IS NOT NULL
        ORDER BY ZTYPEUTI
    """)
    utis = [r['ZTYPEUTI'] for r in cur.fetchall()]
    print("  附件行的所有 UTI 类型：")
    for u in utis:
        print(f"    {u}")

# ── 4. 看附件行用什么字段关联备忘录 ──
print("\n=== 抽查5条附件行（ZNOTE不为NULL）的所有关键字段 ===")
cur.execute("""
    SELECT Z_PK, ZNOTE, ZACCOUNT1, ZACCOUNT, ZFOLDER, ZTYPEUTI,
           ZFILENAME, ZIDENTIFIER, ZGENERATION1, ZMEDIALOCATION,
           ZATTACHMENT, ZNOTE1
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZNOTE IS NOT NULL AND ZTYPEUTI IS NOT NULL
    LIMIT 5
""")
for r in cur.fetchall():
    print(dict(r))

# ── 5. 看 Media 目录结构 ──
print("\n=== Media 目录前3层结构 ===")
media_dir = os.path.join(notes_base, "Media")
if os.path.isdir(media_dir):
    count = 0
    for root, dirs, files in os.walk(media_dir):
        depth = root.replace(media_dir, '').count(os.sep)
        if depth > 2:
            continue
        indent = '  ' * depth
        print(f"{indent}{os.path.basename(root)}/")
        for f in files[:3]:
            print(f"{indent}  {f}")
        count += 1
        if count > 30:
            print("  ... (截断)")
            break
else:
    print("  Media 目录不存在")

conn.close()
shutil.rmtree(tmp_dir)
PYEOF
