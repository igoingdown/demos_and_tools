#!/bin/bash
python3 << 'PYEOF'
import os, shutil, sqlite3, tempfile

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

# 找 2022.08.10 这条备忘录的 Z_PK
cur.execute("SELECT Z_PK, ZTITLE1 FROM ZICCLOUDSYNCINGOBJECT WHERE ZTITLE1 LIKE '%2022.08.10%'")
notes = cur.fetchall()
print("=== 2022.08.10 备忘录 ===")
for n in notes:
    print(f"  Z_PK={n['Z_PK']}  TITLE={n['ZTITLE1']}")
    note_id = n['Z_PK']

    # 查其附件行
    cur.execute("""
        SELECT Z_PK, ZNOTE, ZTYPEUTI, ZFILENAME, ZIDENTIFIER, ZGENERATION1,
               ZATTACHMENT, ZNOTE1, ZACCOUNT1
        FROM ZICCLOUDSYNCINGOBJECT
        WHERE ZNOTE = ?
    """, (note_id,))
    atts = cur.fetchall()
    print(f"  附件行数：{len(atts)}")
    for a in atts:
        print(f"    {dict(a)}")

    # 在 Media 目录下找 identifier 对应的文件
    print(f"\n  Media 目录搜索：")
    for a in atts:
        ident = a['ZIDENTIFIER']
        if not ident:
            continue
        p = os.path.join(notes_base, "Media", ident)
        print(f"    identifier={ident}")
        if os.path.isdir(p):
            for root, dirs, files in os.walk(p):
                for f in files:
                    full = os.path.join(root, f)
                    print(f"      ✅ {full}  ({os.path.getsize(full)} bytes)")
        else:
            print(f"      ❌ 路径不存在: {p}")
            # 模糊搜索
            media_dir = os.path.join(notes_base, "Media")
            if os.path.isdir(media_dir):
                for d in os.listdir(media_dir):
                    if ident[:8].upper() in d.upper():
                        print(f"      🔍 近似匹配: {d}")

# 同时打印 ZATTACHMENT 列全量情况（搞清楚附件关联字段）
print("\n=== ZICCLOUDSYNCINGOBJECT 里 ZATTACHMENT 不为 NULL 的行样本 ===")
cur.execute("""
    SELECT Z_PK, ZTITLE1, ZNOTE, ZFOLDER, ZTYPEUTI, ZFILENAME, ZIDENTIFIER, ZATTACHMENT
    FROM ZICCLOUDSYNCINGOBJECT
    WHERE ZATTACHMENT IS NOT NULL
    LIMIT 5
""")
for r in cur.fetchall():
    print(f"  {dict(r)}")

conn.close()
shutil.rmtree(tmp_dir)
PYEOF