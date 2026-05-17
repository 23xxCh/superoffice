# SuperOffice - AI Office Automation Skills

[English](README.md) | [中文](README_CN.md)

Unified AI Office skills library combining:
- **OfficeMCP** - Windows Office COM automation
- **SenseNova-Skills** - AI skills (image, PPT, data analysis, research)
- **ppt-master** - AI-driven PPT generation
- **MiniMax-AI/skills** - Document processing and multimedia generation

## Features

### Core Capabilities
- **Office Automation** - Control Word, Excel, PowerPoint, Outlook via Windows COM
- **PPT Generation** - Create presentations from PDF/DOCX/MD with AI
- **Excel Analysis** - Data cleaning, analysis, visualization
- **Document Processing** - PDF generation, DOCX editing, XLSX handling

### AI Media (MiniMax + SenseNova)
- Image Generation (MiniMax image-01)
- Video Generation (MiniMax Hailuo 2.3)
- Music Generation (MiniMax music-2.6)
- Text-to-Speech (TTS)
- Deep Research & Report Synthesis

## Quick Start

### 1. Clone and Setup

```bash
cd superoffice
pip install -r requirements.txt
```

### 2. Configure API Keys

Copy `.env.example` to `.env` and add your keys:

```bash
# MiniMax API (your key)
MINIMAX_API_KEY=sk-cp-2_EEt5pGYO_3Hi-RnszXjWaLysv7XBdfBKkKM0_LseLcy273su4m7mwir1Eci_V3WxlDQeCKAvzK9DU0wdQN1zcsJLyTpwIY7FibhbZALCP5MAn04WumveY

# SenseNova API (your key)
SENSENOVA_API_KEY=sk-rOIzAlaxzLhpxS2nqHqXNEuNQSnQDs4q
```

### 3. Install MiniMax CLI (Optional for media generation)

```bash
npm install -g mmx-cli
mmx auth login --api-key YOUR_MINIMAX_KEY
```

### 4. Supported IDEs

| IDE | Configuration |
|-----|---------------|
| Claude Code | `.claude-plugin/` |
| Cursor | `.cursor-plugin/` |
| Codex | `.codex/` (symlink) |
| OpenCode | `.opencode/` (symlink) |

## Skills

| Skill | Command | Description |
|-------|---------|-------------|
| office-automation | `/office` | Control Office apps |
| ppt-generator | `/ppt` | AI PPT creation |
| excel-analysis | `/excel` | Data analysis |
| document-handler | `/doc` | PDF/DOCX/XLSX |
| image-generation | `/image` | AI image creation |
| video-generation | `/video` | AI video (Hailuo) |
| music-generation | `/music` | AI music |
| tts-audio | `/tts` | Text-to-speech |
| deep-research | `/research` | Research reports |

## Usage Examples

### Generate a PPT from document
```
/ppt create from document.pdf style corporate
```

### Analyze Excel data
```
/excel analyze sales_data.xlsx chart bar
```

### Generate AI image
```
/image generate a futuristic city at sunset
```

### Create AI video
```
/video generate a cat playing in a garden
```

## Tech Stack

- **Python 3.10+** - Core runtime
- **pywin32** - Windows COM automation (Windows only)
- **python-pptx** - PPTX manipulation
- **pandas, openpyxl** - Excel processing
- **httpx** - API calls
- **Node.js + mmx-cli** - MiniMax CLI

## License

MIT License

## Credits

- [OfficeMCP](https://github.com/OfficeMCP/OfficeMCP)
- [SenseNova-Skills](https://github.com/OpenSenseNova/SenseNova-Skills)
- [ppt-master](https://github.com/hugohe3/ppt-master)
- [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills)