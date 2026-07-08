**中文** | [English](./README_EN.md)

# Chinese-pdf-to-md-ocr — 简体中文 / 繁体中文 PDF 批量 OCR 转换 Markdown

把当前文件夹里的**扫描版 PDF**（图片型、没法选中文字的那种），一键批量做中文 OCR，最后输出成 Markdown（`.md`），按页分节。

用的是 RapidOCR（模型内置在包里，不依赖 paddle），原始 PDF 一个不动。

## 使用方法

1. 需要转换简体，下载 `convert_ocr.py` 和 `双击运行_OCR.bat`，放进同一个文件夹
2. 需要转换繁体，下载 `convert_ocr_繁体.py` 和 `OCR繁体_v2.bat`，放进同一个文件夹
3. 把要识别的扫描版 PDF 也放进这个文件夹
4. 双击bat文件，等待运行完成
5. 享受！结果在同目录的 `ocr_md_output` 文件夹里，每个 PDF 对应一个 `.md`

## 说明

- 需要电脑装有 Python 3.12（Windows 可从 [python.org](https://www.python.org) 安装）
- 首次运行会自动联网安装依赖（pymupdf、rapidocr-onnxruntime），请保持窗口开着别关
- OCR 较慢，每页一两秒，几百页的书可能要一二十分钟，请耐心
- 老扫描书识别不可能 100% 准，字太小识别不好的话，把脚本里 `DPI = 200` 改成 `300`（更慢但更准）
- 输出的 md 按"第 N 页"分节，方便对照原书定位
