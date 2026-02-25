#!/bin/bash
# 探查手写附件预览图可行性

python3 << 'PYEOF'
import os, shutil, sqlite3, tempfile

notes_base = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/"
)
db_path = os.path.join(notes_base, "NoteStore.sqlite")

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

# ── 1. 列出 notes_base 下所有一级目录，看有哪些缓存目录 ──
print("=== Group Container 下所有一级目录 ===")
for entry in sorted(os.listdir(notes_base)):
    full = os.path.join(notes_base, entry)
    if os.path.isdir(full):
        # 统计文件数
        count = sum(len(files) for _, _, files in os.walk(full))
        print(f"  {entry}/  ({count} 个文件)")

# ── 2. 重点检查 FallbackImages 目录 ──
print("\n=== FallbackImages 目录探查 ===")
fb_dir = os.path.join(notes_base, "FallbackImages")
if os.path.isdir(fb_dir):
    count = 0
    for root, dirs, files in os.walk(fb_dir):
        for f in files:
            full_path = os.path.join(root, f)
            size = os.path.getsize(full_path)
            rel = os.path.relpath(full_path, fb_dir)
            print(f"  {rel}  ({size} bytes)")
            count += 1
            if count >= 20:
                print("  ... (只显示前20个)")
                break
        if count >= 20:
            break
    if count == 0:
        print("  目录存在但为空")
else:
    print("  ❌ FallbackImages 目录不存在")

# ── 3. 检查其他可能存预览图的目录 ──
for candidate in ["Previews", "Thumbnails", "Cache", "Assets"]:
    p = os.path.join(notes_base, candidate)
    if os.path.isdir(p):
        count = sum(len(files) for _, _, files in os.walk(p))
        print(f"\n=== {candidate}/ 目录（{count} 个文件）===")
        shown = 0
        for root, dirs, files in os.walk(p):
            for f in files:
                full_path = os.path.join(root, f)
                size = os.path.getsize(full_path)
                rel = os.path.relpath(full_path, p)
                print(f"  {rel}  ({size} bytes)")
                shown += 1
                if shown >= 10:
                    print("  ...")
                    break
            if shown >= 10:
                break

# ── 4. 取5条手写附件记录，用 identifier 在整个 notes_base 下搜文件 ──
print("\n=== 手写附件 identifier 文件搜索 ===")
cur.execute("""
    SELECT a.ZIDENTIFIER, n.ZTITLE1
    FROM ZICCLOUDSYNCINGOBJECT a
    JOIN ZICCLOUDSYNCINGOBJECT n ON a.ZNOTE = n.Z_PK
    WHERE a.ZTYPEUTI LIKE '%drawing%'
      AND a.ZIDENTIFIER IS NOT NULL
      AND (a.ZMARKEDFORDELETION IS NULL OR a.ZMARKEDFORDELETION = 0)
    LIMIT 5
""")
drawings = cur.fetchall()

for d in drawings:
    ident = d["ZIDENTIFIER"]
    title = d["ZTITLE1"]
    print(f"\n  备忘录:「{title}」identifier={ident}")
    found = []
    for root, dirs, files in os.walk(notes_base):
        for f in files:
            if ident.upper() in f.upper() or ident.upper() in root.upper():
                full_path = os.path.join(root, f)
                size = os.path.getsize(full_path)
                found.append(f"    ✅ {os.path.relpath(full_path, notes_base)}  ({size} bytes)")
    if found:
        for line in found:
            print(line)
    else:
        print(f"    ❌ 未找到任何相关文件")

# ── 5. 检查 ZICASSETSIGNATURE 表，看是否有缓存路径信息 ──
print("\n=== ZICASSETSIGNATURE 表样本（手写附件相关）===")
cur.execute("""
    SELECT s.*, a.ZIDENTIFIER, a.ZTYPEUTI
    FROM ZICASSETSIGNATURE s
    JOIN ZICCLOUDSYNCINGOBJECT a ON s.ZCLOUDSYNCINGOBJECT = a.Z_PK
    WHERE a.ZTYPEUTI LIKE '%drawing%'
    LIMIT 5
""")
rows = cur.fetchall()
if rows:
    for r in rows:
        print(f"  {dict(r)}")
else:
    print("  无记录")

conn.close()
shutil.rmtree(tmp_dir)
PYEOF
