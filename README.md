<div align="center">

# 📄 DocConvert-AI

**Lightweight AI Document Intelligence Conversion & Knowledge Extraction Engine**

**轻量级AI文档智能转换与知识提取引擎**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Zero Dependencies](https://img.shields.io/badge/dependencies-zero-brightgreen.svg)]()
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)]()

[English](#english) | [简体中文](#简体中文) | [繁體中文](#繁體中文)

</div>

---

<a name="english"></a>
## 🎉 Introduction

**DocConvert-AI** is a lightweight, zero-dependency document conversion engine that transforms complex documents into structured, AI-ready formats. Built with pure Python and utilizing only the standard library, it requires no external dependencies while supporting multiple input and output formats.

### 💡 Why DocConvert-AI?

- **🚀 Zero Dependencies**: Pure Python implementation, no pip install hell
- **📦 Lightweight**: Single file, easy to integrate and deploy
- **🔄 Multi-Format Support**: PDF, DOCX, XLSX, PPTX, HTML, Markdown, TXT
- **📤 Flexible Export**: Markdown, JSON, HTML, Plain Text
- **⚡ Fast Processing**: Optimized for speed and efficiency
- **🤖 AI-Ready**: Structured output perfect for LLM consumption

---

## ✨ Core Features

| Feature | Description | Status |
|---------|-------------|--------|
| 📄 **PDF Support** | Extract text from PDF documents | ✅ Supported |
| 📝 **Word Documents** | Parse DOCX files with formatting | ✅ Supported |
| 📊 **Excel Sheets** | Convert XLSX to structured data | ✅ Supported |
| 🎨 **PowerPoint** | Extract text from PPTX slides | ✅ Supported |
| 🌐 **HTML** | Clean extraction from web pages | ✅ Supported |
| 📑 **Markdown** | Native markdown processing | ✅ Supported |
| 📃 **Plain Text** | Basic text file handling | ✅ Supported |
| 🔄 **Batch Processing** | Convert entire directories | ✅ Supported |
| 📤 **Multi-Format Export** | MD, JSON, HTML, TXT output | ✅ Supported |

---

## 🚀 Quick Start

### Requirements

- Python 3.8 or higher
- No external dependencies required!

### Installation

```bash
# Clone the repository
git clone https://github.com/gitstq/docconvert-ai.git
cd docconvert-ai

# Or install via pip (when published)
pip install docconvert-ai
```

### Basic Usage

```bash
# Convert a single file to Markdown (default)
python docconvert.py document.docx

# Convert to specific format
python docconvert.py document.pdf -f json
python docconvert.py document.html -f html
python docconvert.py document.pptx -f text

# Specify output file
python docconvert.py input.docx -o output.md

# Batch convert entire directory
python docconvert.py ./input_dir -b -o ./output_dir -f markdown
```

---

## 📖 Detailed Usage Guide

### Command Line Options

```
usage: docconvert.py [-h] [-o OUTPUT] [-f {markdown,json,html,text}] [-b] [-v]
                     input

DocConvert-AI: Lightweight AI Document Intelligence Conversion Engine

positional arguments:
  input                 Input file or directory path

optional arguments:
  -h, --help            show this help message and exit
  -o, --output          Output file or directory path
  -f, --format          Output format: markdown, json, html, text (default: markdown)
  -b, --batch           Batch convert all files in directory
  -v, --version         show program's version number and exit
```

### Python API

```python
from docconvert import DocConvertAI, OutputFormat

# Initialize converter
converter = DocConvertAI()

# Convert single file
output = converter.convert_file(
    input_path="document.docx",
    output_path="output.md",
    output_format=OutputFormat.MARKDOWN
)

# Batch convert
files = converter.batch_convert(
    input_dir="./documents",
    output_dir="./converted",
    output_format=OutputFormat.JSON
)
```

### Output Formats

#### Markdown Output
```markdown
# Document Title

**Author:** John Doe  
**Created:** 2026-05-16T10:30:00

---

## Section 1

Content here...

- List item 1
- List item 2
```

#### JSON Output
```json
{
  "title": "Document Title",
  "author": "John Doe",
  "created_date": "2026-05-16T10:30:00",
  "metadata": {
    "source_file": "document.docx",
    "file_type": "docx",
    "element_count": 42
  },
  "elements": [
    {
      "type": "heading",
      "content": "Introduction",
      "level": 1
    }
  ]
}
```

---

## 💡 Design Philosophy

### Zero-Dependency Approach

Unlike other document conversion tools that require dozens of dependencies (PyPDF2, python-docx, pandas, etc.), DocConvert-AI leverages Python's powerful standard library:

- **`zipfile`**: For DOCX, XLSX, PPTX (all are ZIP archives)
- **`xml.etree.ElementTree`**: For parsing XML content
- **`re`**: For pattern matching and text extraction
- **`argparse`**: For CLI interface
- **`dataclasses`**: For structured data representation

### Performance Optimizations

- Streaming file processing for large documents
- Efficient regex patterns for text extraction
- Minimal memory footprint
- Fast batch processing

---

## 📦 Packaging & Deployment

### Standalone Script

The entire tool is contained in a single `docconvert.py` file:

```bash
# Just download and run
curl -O https://raw.githubusercontent.com/gitstq/docconvert-ai/main/docconvert.py
python docconvert.py your_document.docx
```

### Python Package

```bash
# Install from source
pip install -e .

# Use as module
python -m docconvert your_document.docx
```

---

## 🤝 Contributing

We welcome contributions! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'feat: add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Commit Message Convention

- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<a name="简体中文"></a>
## 🎉 项目介绍

**DocConvert-AI** 是一款轻量级、零依赖的文档转换引擎，能够将复杂文档转换为结构化的AI友好格式。采用纯Python实现，仅使用标准库，无需外部依赖，同时支持多种输入和输出格式。

### 💡 为什么选择 DocConvert-AI？

- **🚀 零依赖**: 纯Python实现，无需pip安装地狱
- **📦 轻量级**: 单文件设计，易于集成和部署
- **🔄 多格式支持**: PDF、DOCX、XLSX、PPTX、HTML、Markdown、TXT
- **📤 灵活导出**: Markdown、JSON、HTML、纯文本
- **⚡ 快速处理**: 针对速度和效率优化
- **🤖 AI就绪**: 结构化输出，完美适配大语言模型

---

## ✨ 核心特性

| 特性 | 描述 | 状态 |
|------|------|------|
| 📄 **PDF支持** | 从PDF文档提取文本 | ✅ 已支持 |
| 📝 **Word文档** | 解析带格式的DOCX文件 | ✅ 已支持 |
| 📊 **Excel表格** | 将XLSX转换为结构化数据 | ✅ 已支持 |
| 🎨 **PowerPoint** | 从PPTX幻灯片提取文本 | ✅ 已支持 |
| 🌐 **HTML** | 从网页清理提取内容 | ✅ 已支持 |
| 📑 **Markdown** | 原生Markdown处理 | ✅ 已支持 |
| 📃 **纯文本** | 基础文本文件处理 | ✅ 已支持 |
| 🔄 **批处理** | 转换整个目录 | ✅ 已支持 |
| 📤 **多格式导出** | MD、JSON、HTML、TXT输出 | ✅ 已支持 |

---

## 🚀 快速开始

### 环境要求

- Python 3.8 或更高版本
- 无需外部依赖！

### 安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/docconvert-ai.git
cd docconvert-ai

# 或通过pip安装（发布后）
pip install docconvert-ai
```

### 基本用法

```bash
# 将单个文件转换为Markdown（默认）
python docconvert.py document.docx

# 转换为特定格式
python docconvert.py document.pdf -f json
python docconvert.py document.html -f html
python docconvert.py document.pptx -f text

# 指定输出文件
python docconvert.py input.docx -o output.md

# 批量转换整个目录
python docconvert.py ./input_dir -b -o ./output_dir -f markdown
```

---

## 📖 详细使用指南

### 命令行选项

```
用法: docconvert.py [-h] [-o OUTPUT] [-f {markdown,json,html,text}] [-b] [-v]
                     input

DocConvert-AI: 轻量级AI文档智能转换引擎

位置参数:
  input                 输入文件或目录路径

可选参数:
  -h, --help            显示帮助信息并退出
  -o, --output          输出文件或目录路径
  -f, --format          输出格式: markdown, json, html, text (默认: markdown)
  -b, --batch           批量转换目录中的所有文件
  -v, --version         显示程序版本号并退出
```

### Python API

```python
from docconvert import DocConvertAI, OutputFormat

# 初始化转换器
converter = DocConvertAI()

# 转换单个文件
output = converter.convert_file(
    input_path="document.docx",
    output_path="output.md",
    output_format=OutputFormat.MARKDOWN
)

# 批量转换
files = converter.batch_convert(
    input_dir="./documents",
    output_dir="./converted",
    output_format=OutputFormat.JSON
)
```

---

## 💡 设计理念

### 零依赖方案

与其他需要几十个依赖项（PyPDF2、python-docx、pandas等）的文档转换工具不同，DocConvert-AI利用Python强大的标准库：

- **`zipfile`**: 用于DOCX、XLSX、PPTX（都是ZIP压缩包）
- **`xml.etree.ElementTree`**: 用于解析XML内容
- **`re`**: 用于模式匹配和文本提取
- **`argparse`**: 用于命令行界面
- **`dataclasses`**: 用于结构化数据表示

### 性能优化

- 大文档的流式文件处理
- 高效的正则表达式模式
- 最小内存占用
- 快速批处理

---

## 📦 打包与部署

### 独立脚本

整个工具包含在单个 `docconvert.py` 文件中：

```bash
# 下载并运行
curl -O https://raw.githubusercontent.com/gitstq/docconvert-ai/main/docconvert.py
python docconvert.py your_document.docx
```

### Python包

```bash
# 从源码安装
pip install -e .

# 作为模块使用
python -m docconvert your_document.docx
```

---

## 🤝 贡献指南

我们欢迎贡献！请遵循以下准则：

1. Fork 仓库
2. 创建功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 发起 Pull Request

### 提交信息规范

- `feat:` 新功能
- `fix:` Bug修复
- `docs:` 文档更改
- `refactor:` 代码重构
- `test:` 添加测试
- `chore:` 维护任务

---

## 📄 开源协议

本项目采用 MIT 协议 - 查看 [LICENSE](LICENSE) 文件了解详情。

---

<a name="繁體中文"></a>
## 🎉 專案介紹

**DocConvert-AI** 是一款輕量級、零依賴的文件轉換引擎，能夠將複雜文件轉換為結構化的AI友好格式。採用純Python實現，僅使用標準庫，無需外部依賴，同時支援多種輸入和輸出格式。

### 💡 為什麼選擇 DocConvert-AI？

- **🚀 零依賴**: 純Python實現，無需pip安裝地獄
- **📦 輕量級**: 單檔案設計，易於整合和部署
- **🔄 多格式支援**: PDF、DOCX、XLSX、PPTX、HTML、Markdown、TXT
- **📤 靈活匯出**: Markdown、JSON、HTML、純文字
- **⚡ 快速處理**: 針對速度和效率最佳化
- **🤖 AI就緒**: 結構化輸出，完美適配大語言模型

---

## ✨ 核心特性

| 特性 | 描述 | 狀態 |
|------|------|------|
| 📄 **PDF支援** | 從PDF文件提取文字 | ✅ 已支援 |
| 📝 **Word文件** | 解析帶格式的DOCX檔案 | ✅ 已支援 |
| 📊 **Excel表格** | 將XLSX轉換為結構化資料 | ✅ 已支援 |
| 🎨 **PowerPoint** | 從PPTX投影片提取文字 | ✅ 已支援 |
| 🌐 **HTML** | 從網頁清理提取內容 | ✅ 已支援 |
| 📑 **Markdown** | 原生Markdown處理 | ✅ 已支援 |
| 📃 **純文字** | 基礎文字檔案處理 | ✅ 已支援 |
| 🔄 **批次處理** | 轉換整個目錄 | ✅ 已支援 |
| 📤 **多格式匯出** | MD、JSON、HTML、TXT輸出 | ✅ 已支援 |

---

## 🚀 快速開始

### 環境要求

- Python 3.8 或更高版本
- 無需外部依賴！

### 安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/docconvert-ai.git
cd docconvert-ai

# 或透過pip安裝（釋出後）
pip install docconvert-ai
```

### 基本用法

```bash
# 將單個檔案轉換為Markdown（預設）
python docconvert.py document.docx

# 轉換為特定格式
python docconvert.py document.pdf -f json
python docconvert.py document.html -f html
python docconvert.py document.pptx -f text

# 指定輸出檔案
python docconvert.py input.docx -o output.md

# 批次轉換整個目錄
python docconvert.py ./input_dir -b -o ./output_dir -f markdown
```

---

## 📖 詳細使用指南

### 命令列選項

```
用法: docconvert.py [-h] [-o OUTPUT] [-f {markdown,json,html,text}] [-b] [-v]
                     input

DocConvert-AI: 輕量級AI文件智慧轉換引擎

位置參數:
  input                 輸入檔案或目錄路徑

可選參數:
  -h, --help            顯示幫助資訊並退出
  -o, --output          輸出檔案或目錄路徑
  -f, --format          輸出格式: markdown, json, html, text (預設: markdown)
  -b, --batch           批次轉換目錄中的所有檔案
  -v, --version         顯示程式版本號並退出
```

### Python API

```python
from docconvert import DocConvertAI, OutputFormat

# 初始化轉換器
converter = DocConvertAI()

# 轉換單個檔案
output = converter.convert_file(
    input_path="document.docx",
    output_path="output.md",
    output_format=OutputFormat.MARKDOWN
)

# 批次轉換
files = converter.batch_convert(
    input_dir="./documents",
    output_dir="./converted",
    output_format=OutputFormat.JSON
)
```

---

## 💡 設計理念

### 零依賴方案

與其他需要數十個依賴項（PyPDF2、python-docx、pandas等）的文件轉換工具不同，DocConvert-AI利用Python強大的標準庫：

- **`zipfile`**: 用於DOCX、XLSX、PPTX（都是ZIP壓縮包）
- **`xml.etree.ElementTree`**: 用於解析XML內容
- **`re`**: 用於模式匹配和文字提取
- **`argparse`**: 用於命令列介面
- **`dataclasses`**: 用於結構化資料表示

### 效能最佳化

- 大文件的流式檔案處理
- 高效的正規表示式模式
- 最小記憶體佔用
- 快速批次處理

---

## 📦 打包與部署

### 獨立指令碼

整個工具包含在單個 `docconvert.py` 檔案中：

```bash
# 下載並執行
curl -O https://raw.githubusercontent.com/gitstq/docconvert-ai/main/docconvert.py
python docconvert.py your_document.docx
```

### Python包

```bash
# 從原始碼安裝
pip install -e .

# 作為模組使用
python -m docconvert your_document.docx
```

---

## 🤝 貢獻指南

我們歡迎貢獻！請遵循以下準則：

1. Fork 倉庫
2. 建立功能分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 發起 Pull Request

### 提交資訊規範

- `feat:` 新功能
- `fix:` Bug修復
- `docs:` 文件更改
- `refactor:` 程式碼重構
- `test:` 新增測試
- `chore:` 維護任務

---

## 📄 開源協議

本專案採用 MIT 協議 - 檢視 [LICENSE](LICENSE) 檔案瞭解詳情。

---

<div align="center">

**Made with ❤️ by GitStq**

⭐ Star us on GitHub — it motivates us a lot!

</div>
