#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DocConvert-AI: Lightweight AI Document Intelligence Conversion & Knowledge Extraction Engine
轻量级AI文档智能转换与知识提取引擎

A zero-dependency, pure Python implementation for converting various document formats
to structured Markdown/JSON with AI-powered content understanding.
"""

import os
import sys
import re
import json
import base64
import argparse
import zipfile
from io import BytesIO
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum
import xml.etree.ElementTree as ET


class OutputFormat(Enum):
    """Supported output formats"""
    MARKDOWN = "markdown"
    JSON = "json"
    HTML = "html"
    TEXT = "text"


class DocumentType(Enum):
    """Supported document types"""
    PDF = "pdf"
    WORD = "docx"
    EXCEL = "xlsx"
    POWERPOINT = "pptx"
    MARKDOWN = "md"
    HTML = "html"
    TEXT = "txt"
    IMAGE = "image"


@dataclass
class DocumentElement:
    """Represents a document element"""
    type: str  # heading, paragraph, list, table, image, code, quote
    content: str
    level: int = 0  # for headings
    metadata: Dict[str, Any] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}


@dataclass
class ExtractedDocument:
    """Represents an extracted document"""
    title: str
    author: str
    created_date: str
    elements: List[DocumentElement]
    metadata: Dict[str, Any]
    raw_text: str

    def to_dict(self) -> Dict:
        return {
            "title": self.title,
            "author": self.author,
            "created_date": self.created_date,
            "metadata": self.metadata,
            "raw_text": self.raw_text,
            "elements": [
                {
                    "type": e.type,
                    "content": e.content,
                    "level": e.level,
                    "metadata": e.metadata
                }
                for e in self.elements
            ]
        }


class TextExtractor:
    """Extract text from various document formats"""

    @staticmethod
    def extract_from_txt(file_path: str) -> str:
        """Extract text from plain text file"""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()

    @staticmethod
    def extract_from_md(file_path: str) -> str:
        """Extract text from Markdown file"""
        return TextExtractor.extract_from_txt(file_path)

    @staticmethod
    def extract_from_html(file_path: str) -> str:
        """Extract text from HTML file"""
        content = TextExtractor.extract_from_txt(file_path)
        # Simple HTML tag removal
        text = re.sub(r'<script[^>]*>.*?</script>', '', content, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    @staticmethod
    def extract_from_docx(file_path: str) -> str:
        """Extract text from Word document"""
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                xml_content = z.read('word/document.xml')
                tree = ET.fromstring(xml_content)

                # Define namespace
                ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

                texts = []
                for elem in tree.iter():
                    if elem.tag == '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t':
                        if elem.text:
                            texts.append(elem.text)

                return ' '.join(texts)
        except Exception as e:
            return f"[Error extracting DOCX: {str(e)}]"

    @staticmethod
    def extract_from_xlsx(file_path: str) -> str:
        """Extract text from Excel spreadsheet"""
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                # Read shared strings
                shared_strings = []
                try:
                    ss_xml = z.read('xl/sharedStrings.xml')
                    ss_tree = ET.fromstring(ss_xml)
                    for elem in ss_tree.iter():
                        if elem.tag == '{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t':
                            shared_strings.append(elem.text or '')
                except:
                    pass

                # Read sheet data
                sheet_xml = z.read('xl/worksheets/sheet1.xml')
                sheet_tree = ET.fromstring(sheet_xml)

                ns = {'s': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}

                rows = []
                for row in sheet_tree.findall('.//s:row', ns):
                    row_data = []
                    for cell in row.findall('.//s:c', ns):
                        # Get cell value
                        v_elem = cell.find('.//s:v', ns)
                        if v_elem is not None and v_elem.text:
                            val = v_elem.text
                            # Check if it's a shared string
                            t_attr = cell.get('{http://schemas.openxmlformats.org/spreadsheetml/2006/main}t')
                            if t_attr == 's':
                                try:
                                    idx = int(val)
                                    if idx < len(shared_strings):
                                        val = shared_strings[idx]
                                except:
                                    pass
                            row_data.append(val)
                    if row_data:
                        rows.append(' | '.join(row_data))

                return '\n'.join(rows)
        except Exception as e:
            return f"[Error extracting XLSX: {str(e)}]"

    @staticmethod
    def extract_from_pptx(file_path: str) -> str:
        """Extract text from PowerPoint presentation"""
        try:
            with zipfile.ZipFile(file_path, 'r') as z:
                texts = []
                slide_files = [f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')]

                for slide_file in sorted(slide_files):
                    try:
                        slide_xml = z.read(slide_file)
                        tree = ET.fromstring(slide_xml)

                        ns = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main'}

                        for elem in tree.iter():
                            if elem.tag == '{http://schemas.openxmlformats.org/drawingml/2006/main}t':
                                if elem.text:
                                    texts.append(elem.text)
                    except:
                        continue

                return '\n'.join(texts)
        except Exception as e:
            return f"[Error extracting PPTX: {str(e)}]"

    @staticmethod
    def extract_from_pdf_simple(file_path: str) -> str:
        """Simple PDF text extraction (basic implementation)"""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()

            # Try to extract text from PDF
            text_parts = []

            # Find text streams in PDF
            # This is a simplified approach - for production, use PyPDF2 or pdfplumber
            content_str = content.decode('latin-1', errors='ignore')

            # Extract text between BT (Begin Text) and ET (End Text) operators
            import re
            text_blocks = re.findall(r'BT\s*(.*?)\s*ET', content_str, re.DOTALL)

            for block in text_blocks:
                # Extract text from TJ and Tj operators
                text_parts.extend(re.findall(r'\(([^)]+)\)', block))

            if text_parts:
                return '\n'.join(text_parts)

            # Fallback: try to extract any readable text
            readable = re.findall(r'\(([A-Za-z0-9\s.,;:!?-]+)\)', content_str)
            return '\n'.join(readable[:1000])  # Limit output

        except Exception as e:
            return f"[Error extracting PDF: {str(e)}]"


class DocumentParser:
    """Parse documents into structured elements"""

    def __init__(self):
        self.extractor = TextExtractor()

    def parse(self, file_path: str) -> ExtractedDocument:
        """Parse a document and return structured content"""
        file_path = Path(file_path)
        ext = file_path.suffix.lower()

        # Extract raw text based on file type
        if ext == '.txt':
            raw_text = self.extractor.extract_from_txt(str(file_path))
            doc_type = DocumentType.TEXT
        elif ext in ['.md', '.markdown']:
            raw_text = self.extractor.extract_from_md(str(file_path))
            doc_type = DocumentType.MARKDOWN
        elif ext in ['.html', '.htm']:
            raw_text = self.extractor.extract_from_html(str(file_path))
            doc_type = DocumentType.HTML
        elif ext == '.docx':
            raw_text = self.extractor.extract_from_docx(str(file_path))
            doc_type = DocumentType.WORD
        elif ext == '.xlsx':
            raw_text = self.extractor.extract_from_xlsx(str(file_path))
            doc_type = DocumentType.EXCEL
        elif ext == '.pptx':
            raw_text = self.extractor.extract_from_pptx(str(file_path))
            doc_type = DocumentType.POWERPOINT
        elif ext == '.pdf':
            raw_text = self.extractor.extract_from_pdf_simple(str(file_path))
            doc_type = DocumentType.PDF
        else:
            raise ValueError(f"Unsupported file format: {ext}")

        # Parse into elements
        elements = self._parse_elements(raw_text, doc_type)

        # Extract metadata
        title = self._extract_title(raw_text, file_path.stem)
        author = self._extract_author(raw_text)

        return ExtractedDocument(
            title=title,
            author=author,
            created_date=datetime.now().isoformat(),
            elements=elements,
            metadata={
                "source_file": str(file_path),
                "file_type": doc_type.value,
                "file_size": file_path.stat().st_size,
                "element_count": len(elements)
            },
            raw_text=raw_text
        )

    def _parse_elements(self, text: str, doc_type: DocumentType) -> List[DocumentElement]:
        """Parse text into structured elements"""
        elements = []
        lines = text.split('\n')

        in_code_block = False
        code_content = []
        list_items = []

        for line in lines:
            stripped = line.strip()

            # Code block detection
            if stripped.startswith('```') or stripped.startswith('~~~'):
                if in_code_block:
                    # End code block
                    elements.append(DocumentElement(
                        type="code",
                        content='\n'.join(code_content),
                        metadata={"language": ""}
                    ))
                    code_content = []
                    in_code_block = False
                else:
                    in_code_block = True
                continue

            if in_code_block:
                code_content.append(line)
                continue

            # Empty line handling
            if not stripped:
                if list_items:
                    elements.append(DocumentElement(
                        type="list",
                        content='\n'.join(list_items),
                        metadata={"list_type": "unordered"}
                    ))
                    list_items = []
                continue

            # Heading detection (Markdown style)
            heading_match = re.match(r'^(#{1,6})\s+(.+)$', stripped)
            if heading_match:
                level = len(heading_match.group(1))
                elements.append(DocumentElement(
                    type="heading",
                    content=heading_match.group(2),
                    level=level
                ))
                continue

            # Alternative heading detection (underlined)
            if stripped and len(elements) > 0:
                prev_element = elements[-1]
                if prev_element.type == "paragraph" and re.match(r'^[=\-]+$', stripped):
                    prev_element.type = "heading"
                    prev_element.level = 1 if stripped[0] == '=' else 2
                    continue

            # List item detection
            list_match = re.match(r'^[\*\-\+]\s+(.+)$', stripped)
            if list_match:
                list_items.append(list_match.group(1))
                continue

            numbered_list_match = re.match(r'^\d+[.\)]\s+(.+)$', stripped)
            if numbered_list_match:
                list_items.append(numbered_list_match.group(1))
                continue

            # Quote detection
            if stripped.startswith('>'):
                elements.append(DocumentElement(
                    type="quote",
                    content=stripped[1:].strip()
                ))
                continue

            # Table detection (simple)
            if '|' in stripped:
                elements.append(DocumentElement(
                    type="table",
                    content=stripped
                ))
                continue

            # Default: paragraph
            elements.append(DocumentElement(
                type="paragraph",
                content=stripped
            ))

        # Handle remaining list items
        if list_items:
            elements.append(DocumentElement(
                type="list",
                content='\n'.join(list_items),
                metadata={"list_type": "unordered"}
            ))

        # Handle remaining code block
        if code_content:
            elements.append(DocumentElement(
                type="code",
                content='\n'.join(code_content),
                metadata={"language": ""}
            ))

        return elements

    def _extract_title(self, text: str, filename: str) -> str:
        """Extract document title"""
        # Try to find first heading
        lines = text.split('\n')
        for line in lines[:20]:  # Check first 20 lines
            stripped = line.strip()
            # Markdown heading
            match = re.match(r'^#\s+(.+)$', stripped)
            if match:
                return match.group(1)
            # Alternative: first non-empty line that's not too long
            if stripped and len(stripped) < 100 and not stripped.startswith('#'):
                return stripped
        return filename

    def _extract_author(self, text: str) -> str:
        """Extract document author"""
        # Look for common author patterns
        patterns = [
            r'[Aa]uthor[:\s]+([^\n]+)',
            r'[Bb]y[:\s]+([^\n]+)',
            r'[Cc]reated by[:\s]+([^\n]+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text[:1000])
            if match:
                return match.group(1).strip()
        return "Unknown"


class MarkdownConverter:
    """Convert extracted documents to Markdown"""

    @staticmethod
    def convert(document: ExtractedDocument) -> str:
        """Convert document to Markdown format"""
        lines = []

        # Title
        lines.append(f"# {document.title}\n")

        # Metadata
        if document.author != "Unknown":
            lines.append(f"**Author:** {document.author}  ")
        lines.append(f"**Created:** {document.created_date}  ")
        lines.append(f"**Source:** {document.metadata.get('source_file', 'Unknown')}\n")

        lines.append("---\n")

        # Content
        for element in document.elements:
            if element.type == "heading":
                prefix = "#" * element.level
                lines.append(f"{prefix} {element.content}\n")

            elif element.type == "paragraph":
                lines.append(f"{element.content}\n")

            elif element.type == "list":
                list_type = element.metadata.get("list_type", "unordered")
                for item in element.content.split('\n'):
                    if list_type == "unordered":
                        lines.append(f"- {item}")
                    else:
                        lines.append(f"1. {item}")
                lines.append("")

            elif element.type == "code":
                lang = element.metadata.get("language", "")
                lines.append(f"```{lang}")
                lines.append(element.content)
                lines.append("```\n")

            elif element.type == "quote":
                lines.append(f"> {element.content}\n")

            elif element.type == "table":
                lines.append(f"{element.content}\n")

        return '\n'.join(lines)


class JSONConverter:
    """Convert extracted documents to JSON"""

    @staticmethod
    def convert(document: ExtractedDocument) -> str:
        """Convert document to JSON format"""
        return json.dumps(document.to_dict(), ensure_ascii=False, indent=2)


class HTMLConverter:
    """Convert extracted documents to HTML"""

    @staticmethod
    def convert(document: ExtractedDocument) -> str:
        """Convert document to HTML format"""
        html_parts = [
            "<!DOCTYPE html>",
            "<html>",
            "<head>",
            f"<title>{document.title}</title>",
            "<style>",
            "body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }",
            "h1 { color: #333; }",
            "h2 { color: #555; }",
            "h3 { color: #666; }",
            "code { background: #f4f4f4; padding: 2px 5px; border-radius: 3px; }",
            "pre { background: #f4f4f4; padding: 15px; overflow-x: auto; }",
            "blockquote { border-left: 4px solid #ddd; margin: 0; padding-left: 15px; color: #666; }",
            ".metadata { color: #888; font-size: 0.9em; margin-bottom: 20px; }",
            "</style>",
            "</head>",
            "<body>",
            f"<h1>{document.title}</h1>",
            "<div class='metadata'>",
        ]

        if document.author != "Unknown":
            html_parts.append(f"<p><strong>Author:</strong> {document.author}</p>")
        html_parts.append(f"<p><strong>Created:</strong> {document.created_date}</p>")
        html_parts.append("</div>")
        html_parts.append("<hr>")

        for element in document.elements:
            if element.type == "heading":
                tag = f"h{element.level}"
                html_parts.append(f"<{tag}>{element.content}</{tag}>")

            elif element.type == "paragraph":
                html_parts.append(f"<p>{element.content}</p>")

            elif element.type == "list":
                html_parts.append("<ul>")
                for item in element.content.split('\n'):
                    html_parts.append(f"<li>{item}</li>")
                html_parts.append("</ul>")

            elif element.type == "code":
                html_parts.append(f"<pre><code>{element.content}</code></pre>")

            elif element.type == "quote":
                html_parts.append(f"<blockquote>{element.content}</blockquote>")

            elif element.type == "table":
                html_parts.append(f"<p>{element.content}</p>")

        html_parts.extend(["</body>", "</html>"])

        return '\n'.join(html_parts)


class DocConvertAI:
    """Main class for DocConvert-AI"""

    def __init__(self):
        self.parser = DocumentParser()

    def convert_file(self, input_path: str, output_path: str, output_format: OutputFormat = OutputFormat.MARKDOWN) -> str:
        """Convert a single file"""
        # Parse document
        document = self.parser.parse(input_path)

        # Convert to desired format
        if output_format == OutputFormat.MARKDOWN:
            content = MarkdownConverter.convert(document)
            ext = ".md"
        elif output_format == OutputFormat.JSON:
            content = JSONConverter.convert(document)
            ext = ".json"
        elif output_format == OutputFormat.HTML:
            content = HTMLConverter.convert(document)
            ext = ".html"
        elif output_format == OutputFormat.TEXT:
            content = document.raw_text
            ext = ".txt"
        else:
            raise ValueError(f"Unsupported output format: {output_format}")

        # Write output
        if output_path:
            output_file = Path(output_path)
            if output_file.is_dir():
                output_file = output_file / (Path(input_path).stem + ext)
        else:
            output_file = Path(input_path).with_suffix(ext)

        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)

        return str(output_file)

    def batch_convert(self, input_dir: str, output_dir: str, output_format: OutputFormat = OutputFormat.MARKDOWN) -> List[str]:
        """Batch convert all supported files in a directory"""
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        supported_exts = ['.txt', '.md', '.markdown', '.html', '.htm', '.docx', '.xlsx', '.pptx', '.pdf']

        converted_files = []
        for file_path in input_path.iterdir():
            if file_path.is_file() and file_path.suffix.lower() in supported_exts:
                try:
                    output_file = self.convert_file(str(file_path), str(output_path), output_format)
                    converted_files.append(output_file)
                    print(f"✓ Converted: {file_path.name} -> {Path(output_file).name}")
                except Exception as e:
                    print(f"✗ Failed: {file_path.name} - {str(e)}")

        return converted_files


def create_cli():
    """Create command-line interface"""
    parser = argparse.ArgumentParser(
        description="DocConvert-AI: Lightweight AI Document Intelligence Conversion Engine",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.docx                    # Convert to markdown (default)
  %(prog)s document.docx -o output.md       # Specify output file
  %(prog)s document.pdf -f json             # Convert to JSON format
  %(prog)s ./input_dir -b ./output_dir      # Batch convert directory
        """
    )

    parser.add_argument('input', help='Input file or directory path')
    parser.add_argument('-o', '--output', help='Output file or directory path')
    parser.add_argument('-f', '--format', choices=['markdown', 'json', 'html', 'text'],
                        default='markdown', help='Output format (default: markdown)')
    parser.add_argument('-b', '--batch', action='store_true',
                        help='Batch convert all files in directory')
    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')

    return parser


def main():
    """Main entry point"""
    parser = create_cli()
    args = parser.parse_args()

    converter = DocConvertAI()

    # Map format string to enum
    format_map = {
        'markdown': OutputFormat.MARKDOWN,
        'json': OutputFormat.JSON,
        'html': OutputFormat.HTML,
        'text': OutputFormat.TEXT
    }
    output_format = format_map[args.format]

    try:
        if args.batch:
            # Batch conversion
            if not args.output:
                print("Error: Output directory required for batch conversion")
                sys.exit(1)
            converted = converter.batch_convert(args.input, args.output, output_format)
            print(f"\n✓ Successfully converted {len(converted)} files")
        else:
            # Single file conversion
            output_file = converter.convert_file(args.input, args.output, output_format)
            print(f"✓ Converted: {args.input} -> {output_file}")

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == '__main__':
    main()
