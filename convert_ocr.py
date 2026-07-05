# -*- coding: utf-8 -*-
# 批量对【扫描版】PDF 做中文 OCR,输出 Markdown(.md)
# 用 RapidOCR(模型内置,不依赖 paddle)
# 把本文件、运行的 bat 和你的 PDF 放同一文件夹,双击 bat 即可。
# 注意:OCR 较慢,每页一两秒,几百页要等;老扫描书识别不可能 100% 准。

import sys
import os
import subprocess
import importlib.util
import tempfile
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def ensure(import_name, pip_spec):
    """缺组件就自动 pip 安装"""
    if importlib.util.find_spec(import_name) is None:
        print(f"首次运行,正在安装 {pip_spec} …(要联网下载,请稍等,别关窗口)\n")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + pip_spec.split())
        print()


# 安装两个组件:PDF 渲染 + OCR 引擎(模型已内置在包里)
ensure("fitz", "pymupdf")
ensure("rapidocr_onnxruntime", "rapidocr-onnxruntime")

import fitz  # PyMuPDF
from rapidocr_onnxruntime import RapidOCR

print("正在加载中文 OCR 引擎……\n")
engine = RapidOCR()

base = Path(__file__).resolve().parent
out_dir = base / "ocr_md_output"
out_dir.mkdir(exist_ok=True)

DPI = 200  # 字太小识别不好可改成 300(更慢)

pdfs = sorted(p for p in base.iterdir() if p.is_file() and p.suffix.lower() == ".pdf")

if not pdfs:
    print("没找到 PDF 文件。")
    print(f"请把扫描版 PDF 和本程序放在同一个文件夹里:\n  {base}")
else:
    print(f"找到 {len(pdfs)} 个 PDF。\n提醒:扫描书 OCR 较慢,几百页可能要一二十分钟,请耐心。\n")
    for pdf in pdfs:
        print(f"=== 开始处理: {pdf.name} ===")
        try:
            doc = fitz.open(str(pdf))
            total = len(doc)
            parts = []
            with tempfile.TemporaryDirectory() as td:
                tmp_png = os.path.join(td, "page.png")
                for i in range(total):
                    page = doc[i]
                    pix = page.get_pixmap(dpi=DPI)
                    pix.save(tmp_png)
                    result, _ = engine(tmp_png)
                    lines = []
                    if result:
                        for item in result:
                            lines.append(item[1])  # item = [box, text, score]
                    parts.append(f"## 第 {i + 1} 页\n\n" + "\n".join(lines))
                    print(f"  进度: {i + 1}/{total} 页", end="\r")
            doc.close()
            md = "\n\n".join(parts)
            (out_dir / (pdf.stem + ".md")).write_text(md, encoding="utf-8")
            print(f"\n  ✓ 已保存: {pdf.stem}.md\n")
        except Exception as e:
            print(f"\n  ✗ 失败: {pdf.name}  原因: {e}\n")
    print(f"全部完成。结果在这个文件夹里:\n  {out_dir}")
