#!/bin/bash
# ============================================================
# 手写备忘录 OCR 导出脚本
# 依赖：本地 ollama 运行 qwen3-vl（或其他视觉模型）
# 用法：bash ocr_drawings.sh [备忘录导出目录]
# 默认读取 ~/Desktop/notes_export（与 export_notes.sh 输出对应）
# ============================================================

NOTES_EXPORT_DIR="${1:-$HOME/Desktop/notes_export}"

echo "📁 备忘录导出目录：$NOTES_EXPORT_DIR"
echo "⏳ 开始 OCR 手写附件..."

python3 - "$NOTES_EXPORT_DIR" <<'PYEOF'
import sys, os, re, shutil, sqlite3, tempfile, json, base64, urllib.request, urllib.error

notes_export_dir = sys.argv[1]

notes_base = os.path.expanduser(
    "~/Library/Group Containers/group.com.apple.notes/"
)
db_path = os.path.join(notes_base, "NoteStore.sqlite")

OLLAMA_URL   = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "qwen3-vl:32b"
OCR_PROMPT   = (
    "这是一张手写笔记图片。请将图片中所有手写文字完整转录为纯文本，"
    "保持原有的换行和段落结构，不要添加任何解释或额外内容，只输出转录文字。"
    "如果图片中没有文字，只回复：（无文字内容）"
)

# ── 工具函数 ──────────────────────────────────────────────
def safe_name(s, max_len=80):
    s = re.sub(r'[/\\:*?"<>|\x00-\x1f]', '_', s)
    s = s.strip('. ')
    return s[:max_len] if s else "untitled"

def check_ollama():
    """检查 ollama 是否在运行"""
    try:
        req = urllib.request.urlopen("http://localhost:11434/api/tags", timeout=3)
        data = json.loads(req.read())
        models = [m["name"] for m in data.get("models", [])]
        print(f"✅ Ollama 运行中，已加载模型：{models}")
        # 检查目标模型是否存在（模糊匹配）
        matched = [m for m in models if OLLAMA_MODEL.split(":")[0] in m]
        if not matched:
            print(f"⚠️  未找到 {OLLAMA_MODEL}，请确认模型名称")
            print(f"   可用模型：{models}")
            return False
        return True
    except Exception as e:
        print(f"❌ 无法连接 Ollama：{e}")
        print("   请确认 ollama serve 正在运行")
        return False

def ocr_image(image_path):
    """调用 ollama qwen3-vl 对图片做 OCR"""
    with open(image_path, "rb") as f:
        img_b64 = base64.b64encode(f.read()).decode("utf-8")

    payload = json.dumps({
        "model": OLLAMA_MODEL,
        "prompt": OCR_PROMPT,
        "images": [img_b64],
        "stream": False,
        "options": {
            "temperature": 0.1,   # 低温度，减少幻觉
            "num_predict": 2048,
        }
    }).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as resp:
            result = json.loads(resp.read())
            return result.get("response", "").strip()
    except urllib.error.URLError as e:
        return f"[OCR 失败：{e}]"
    except Exception as e:
        return f"[OCR 异常：{e}]"

def find_fallback_image(identifier):
    """
    在 Accounts/<uuid>/FallbackImages/<identifier>/1_xxx/FallbackImage.png 下找图
    优先 FallbackImage.png（高清），找不到则用 Previews 下的缩略图
    """
    accounts_dir = os.path.join(notes_base, "Accounts")
    if not os.path.isdir(accounts_dir):
        return None

    for account_uuid in os.listdir(accounts_dir):
        account_path = os.path.join(accounts_dir, account_uuid)
        if not os.path.isdir(account_path):
            continue

        # 优先找 FallbackImage（完整尺寸）
        fb_base = os.path.join(account_path, "FallbackImages", identifier)
        if os.path.isdir(fb_base):
            for sub in os.listdir(fb_base):
                candidate = os.path.join(fb_base, sub, "FallbackImage.png")
                if os.path.isfile(candidate):
                    return candidate

        # 次选：Previews 下的大图（优先选尺寸更大的）
        previews_dir = os.path.join(account_path, "Previews")
        if os.path.isdir(previews_dir):
            candidates = [
                os.path.join(previews_dir, f)
                for f in os.listdir(previews_dir)
                if identifier in f and f.endswith(".png")
            ]
            if candidates:
                # 选文件最大的
                return max(candidates, key=lambda p: os.path.getsize(p))

    return None

# ── 主流程 ────────────────────────────────────────────────
if not check_ollama():
    sys.exit(1)

# 复制数据库
tmp_dir = tempfile.mkdtemp()
tmp_db  = os.path.join(tmp_dir, "NoteStore.sqlite")
shutil.copy2(db_path, tmp_db)
for ext in ("-wal", "-shm"):
    src = db_path + ext
    if os.path.exists(src):
        shutil.copy2(src, tmp_db + ext)

total   = 0
success = 0
failed  = 0
no_img  = 0

try:
    conn = sqlite3.connect(tmp_db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    # 查所有手写附件，关联备忘录标题和文件夹信息
    cur.execute("""
        SELECT
            a.ZIDENTIFIER  AS identifier,
            a.ZTYPEUTI     AS uti,
            n.ZTITLE1      AS note_title,
            f.ZTITLE2      AS folder_name,
            acc.ZNAME      AS account_name
        FROM ZICCLOUDSYNCINGOBJECT a
        JOIN ZICCLOUDSYNCINGOBJECT n   ON a.ZNOTE    = n.Z_PK
        JOIN ZICCLOUDSYNCINGOBJECT f   ON n.ZFOLDER  = f.Z_PK
        LEFT JOIN ZICCLOUDSYNCINGOBJECT acc ON f.ZACCOUNT4 = acc.Z_PK
        WHERE a.ZTYPEUTI LIKE '%drawing%'
          AND a.ZIDENTIFIER IS NOT NULL
          AND (a.ZMARKEDFORDELETION IS NULL OR a.ZMARKEDFORDELETION = 0)
          AND (n.ZMARKEDFORDELETION IS NULL OR n.ZMARKEDFORDELETION = 0)
        ORDER BY account_name, folder_name, note_title
    """)
    drawings = cur.fetchall()
    print(f"\n📝 共找到 {len(drawings)} 个手写附件，开始 OCR...\n")

    for d in drawings:
        identifier   = d["identifier"]
        note_title   = (d["note_title"] or "untitled").strip()
        folder_name  = d["folder_name"] or "未命名文件夹"
        account_name = d["account_name"] or "本地账户"
        total += 1

        print(f"  [{total}/{len(drawings)}] 「{note_title}」/ {folder_name}", end=" ", flush=True)

        # 找到对应导出目录下的 _attachments 文件夹
        att_dir = os.path.join(
            notes_export_dir,
            safe_name(account_name),
            safe_name(folder_name),
            safe_name(note_title) + "_attachments"
        )
        os.makedirs(att_dir, exist_ok=True)

        # 找预览图
        image_path = find_fallback_image(identifier)
        if not image_path:
            print("❌ 未找到预览图")
            no_img += 1
            # 更新占位文件说明
            placeholder = os.path.join(att_dir, "手写涂鸦_未找到预览图.txt")
            with open(placeholder, 'w', encoding='utf-8') as f:
                f.write(f"identifier: {identifier}\n未找到 FallbackImage，可能尚未在本地渲染。\n")
            continue

        img_size = os.path.getsize(image_path) // 1024
        print(f"→ 图片 {img_size}KB", end=" ", flush=True)

        # OCR
        ocr_text = ocr_image(image_path)

        if ocr_text.startswith("[OCR 失败") or ocr_text.startswith("[OCR 异常"):
            print(f"❌ {ocr_text}")
            failed += 1
            continue

        print(f"✅ ({len(ocr_text)} 字符)")

        # 写入 OCR 结果到 _attachments 目录
        ocr_file = os.path.join(att_dir, "手写内容_OCR.txt")
        # 如果已存在（多个手写附件），追加
        mode = 'a' if os.path.exists(ocr_file) else 'w'
        with open(ocr_file, mode, encoding='utf-8') as f:
            if mode == 'a':
                f.write("\n\n" + "─" * 30 + "\n\n")
            f.write(f"[来源图片：{os.path.basename(image_path)}]\n\n")
            f.write(ocr_text)
            f.write("\n")

        # 同时把预览图也复制过去，方便对照
        dst_img = os.path.join(att_dir, f"手写原图_{identifier[:8]}.png")
        if not os.path.exists(dst_img):
            shutil.copy2(image_path, dst_img)

        success += 1

    conn.close()

finally:
    shutil.rmtree(tmp_dir, ignore_errors=True)

# ── 汇总 ──────────────────────────────────────────────────
print(f"\n{'═' * 55}")
print(f"✅ OCR 完成！")
print(f"   成功：{success} 个")
if no_img  > 0: print(f"   无预览图：{no_img} 个（可能未在本地渲染）")
if failed  > 0: print(f"   失败：{failed} 个")
print(f"\n📂 结果已写入各备忘录的 _attachments/手写内容_OCR.txt")

PYEOF

echo ""
echo "🎉 脚本执行结束"
