---
name: document-handler
description: Document processing - PDF generation, DOCX editing, XLSX manipulation
triggers:
  - /pdf
  - /docx
  - /document
  - create pdf
  - edit docx
metadata:
  tier: 1
  category: office
  visibility: public
---

# Document Handler Skill

Process and generate PDF, DOCX, and XLSX documents. Based on MiniMax-AI/skills.

## Features

### PDF
- Generate PDF from HTML, Markdown, text
- Fill PDF forms
- Reformat existing PDFs
- 15+ cover styles
- Token-based design system

### DOCX
- Create new documents
- Edit existing documents
- Format with styles
- Add tables, images, headers/footers
- XSD validation support

### XLSX
- Create new spreadsheets
- Read and analyze data
- Format cells, rows, columns
- Add charts and formulas
- Multiple sheets support

## Tools

### pdf_create(content, output_path, style='default')
Create PDF from content.
- content: HTML, Markdown, or plain text
- style: 'modern', 'classic', 'report', 'invoice', etc.

### pdf_fill_form(pdf_path, data, output_path)
Fill PDF form fields with data.
- data: dict of field_name -> value

### docx_create(content, output_path)
Create new DOCX document.
- content: text or HTML

### docx_edit(input_path, operations, output_path)
Edit existing DOCX.
- operations: insert_text, replace_text, add_table, add_image, etc.

### docx_format(input_path, styles, output_path)
Apply formatting to DOCX.
- styles: font, size, color, alignment, spacing

### xlsx_create(data, output_path, sheet_name='Sheet1')
Create new XLSX from data.
- data: list of dicts or DataFrame

### xlsx_read(file_path, sheet_name=None)
Read XLSX file.

### xlsx_format(input_path, formats, output_path)
Apply formatting to XLSX.

## Usage Examples

### Create PDF report
```
/pdf create from data.html style report output report.pdf
```

### Fill PDF form
```
/pdf fill form.pdf data.json output filled.pdf
```

### Create DOCX
```
/docx create content.md output document.docx
```

### Edit DOCX
```
/docx edit document.docx operations=replace:old:new output updated.docx
```

### Create XLSX
```
/xlsx create data.csv output spreadsheet.xlsx
```

## Requirements

- Python 3.10+
- python-docx
- pypdf / PyPDF2
- reportlab
- openpyxl

## Output Formats

- PDF: .pdf
- DOCX: .docx, .docm
- XLSX: .xlsx, .xlsm