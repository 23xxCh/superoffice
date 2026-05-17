---
name: office-automation
description: Windows Office COM automation - control Word, Excel, PowerPoint via Python
triggers:
  - /office
  - /word
  - /excel
  - /powerpoint
  - office automation
  - control office
metadata:
  tier: 1
  category: office
  visibility: public
---

# Office Automation Skill

Control Microsoft Office applications via Windows COM automation. Based on OfficeMCP.

## Supported Applications

- Microsoft Word
- Microsoft Excel
- Microsoft PowerPoint
- Microsoft Access
- Microsoft Outlook
- Microsoft OneNote
- Microsoft Visio
- Microsoft Project
- Microsoft Publisher
- WPS Office (Writer, Spreadsheet, Presentation)

## Tools

### AvailableApps
Returns a list of all Microsoft Office applications installed on the system.

### RunningApps
Returns a list of currently running Office application instances.

### IsAppAvailable(app_name: str)
Check if a specific Office application is installed.
- Default: "Word"

### Launch(app_name: str, visible: bool)
Launch a new Office application or attach to existing instance.

### Visible(app_name: str, visible: bool)
Get or set visibility of an Office application window.

### Quit(app_name: str, force: bool)
Quit a specific Office application. Force terminates if needed.

### RunPython(code: str, data: str)
Execute arbitrary Python code on the server. This is the primary tool for fine-grained Office automation.

**Parameters:**
- `code`: Python source code to execute
- `data`: String data passed into execution namespace

**Namespace available:**
- `Officer` - Access to all Office application COM objects
- `output` - Variable for returning results
- `data` - Input data passed in

### Speak(text: str, volume: int, rate: int)
Speak text through Windows SAPI speech synthesis.
- volume: 0-100 (default: 100)
- rate: -10 to 10 (default: 0)

### ScreenShot(save_path: str)
Capture full-screen screenshot.

### DownloadImage(url: str, save_path: str)
Download an image from URL.

## Usage Examples

### Create Excel Workbook
```python
# Create new workbook, set cell value, format
app = Officer.Excel
wb = app.Workbooks.Add()
ws = wb.ActiveSheet
ws.Cells(1, 1).Value = "Hello"
ws.Cells(1, 1).Font.Bold = True
wb.SaveAs("report.xlsx")
wb.Close()
output = "Excel file created"
```

### Create PowerPoint Slide
```python
# Add slide with title and content
app = Officer.PowerPoint
pres = app.Presentations.Add()
slide = pres.Slides.Add(1, 1)  # ppLayoutTitle
slide.Shapes.Title.TextFrame.TextRange.Text = "My Title"
pres.SaveAs("presentation.pptx")
pres.Close()
output = "PowerPoint created"
```

### Create Word Document
```python
# Add paragraph
app = Officer.Word
doc = app.Documents.Add()
para = doc.Content.Paragraphs.Add()
para.Range.Text = "Hello from Office Automation!"
doc.SaveAs("document.docx")
doc.Close()
output = "Word document created"
```

## Requirements

- Windows operating system
- Microsoft Office or WPS Office installed
- Python 3.12+
- pywin32 package

## Security Warning

The `RunPython` tool executes arbitrary Python code. Only use with trusted AI models.

## Error Handling

- Application not installed → Return error with available apps list
- COM connection failed → Retry or suggest restarting Office
- File save failed → Check file permissions and path