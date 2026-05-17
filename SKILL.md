---
name: superoffice
description: AI Office Automation Skills - PPT/Excel/Document generation with MiniMax & SenseNova
triggers:
  - superoffice
  - office automation
  - ppt generator
  - excel analysis
  - document handler
  - ai image
  - ai video
  - ai music
  - tts voice
  - deep research
metadata:
  tier: 0
  category: office
  visibility: public
---

# SuperOffice - AI Office Automation Skills

Unified AI Office skills combining the best of OfficeMCP, SenseNova-Skills, ppt-master, and MiniMax-AI/skills.

## Capabilities

- **Office Automation**: Control Microsoft Office apps via COM automation
- **PPT Generation**: AI-powered presentation creation from documents
- **Excel Analysis**: Data analysis, cleaning, visualization
- **Document Processing**: PDF, DOCX, XLSX generation and editing
- **AI Media Generation**: Image, video, music, TTS via MiniMax & SenseNova
- **Deep Research**: Multi-dimensional research and report synthesis

## Quick Start

1. Configure API keys in `.env` file (copy from `.env.example`)
2. Install dependencies: `pip install -r requirements.txt`
3. Install Node.js CLI for MiniMax: `npm install -g mmx-cli`
4. Authenticate: `mmx auth login --api-key YOUR_MINIMAX_KEY`

## Skills Overview

| Skill | Description | Trigger |
|-------|-------------|---------|
| office-automation | Windows Office COM control | /office, /word, /excel, /ppt |
| ppt-generator | AI PPT creation from documents | /ppt, /presentation |
| excel-analysis | Data analysis and visualization | /excel, /analyze |
| document-handler | PDF/DOCX/XLSX processing | /pdf, /docx |
| image-generation | AI image creation | /image, /draw |
| video-generation | AI video (Hailuo) | /video |
| music-generation | AI music creation | /music |
| tts-audio | Text-to-speech synthesis | /tts, /speak |
| deep-research | Research and report generation | /research |

## API Configuration

Required environment variables:
- `MINIMAX_API_KEY` - Your MiniMax API key
- `SENSENOVA_API_KEY` - Your SenseNova API key

Optional:
- `MINIMAX_API_BASE` - MiniMax API base URL
- `SENSENOVA_API_BASE` - SenseNova API base URL

## Supported IDEs

- Claude Code (.claude-plugin)
- Cursor (.cursor-plugin)
- Codex (.codex)
- OpenCode (.opencode)

---