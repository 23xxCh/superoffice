---
name: superoffice-core
description: Core entry for SuperOffice - loads all sub-skills and manages API configuration
triggers:
  - superoffice
  - office suite
  - ai office
metadata:
  tier: 0
  category: core
  visibility: public
---

# SuperOffice Core Skill

The central hub that loads and coordinates all SuperOffice sub-skills.

## Sub-Skills

This skill orchestrates the following sub-skills:

| Sub-Skill | Purpose |
|-----------|---------|
| office-automation | Windows Office COM control |
| ppt-generator | AI-powered PPT creation |
| excel-analysis | Data analysis and visualization |
| document-handler | PDF/DOCX/XLSX processing |
| image-generation | AI image generation (MiniMax) |
| video-generation | AI video generation (Hailuo) |
| music-generation | AI music generation |
| tts-audio | Text-to-speech synthesis |
| deep-research | Research and report generation |

## API Configuration

### MiniMax API
- **API Key**: Set via `MINIMAX_API_KEY` environment variable
- **Base URL**: `https://api.minimax.chat/v1` (default)
- **Models**: 
  - Text: `MiniMax-M2.7`
  - Image: `image-01`
  - Video: `MiniMax-Hailuo-2.3`
  - TTS: `speech-2.8-hd`
  - Music: `music-2.6-free`

### SenseNova API
- **API Key**: Set via `SENSENOVA_API_KEY` environment variable
- **Base URL**: `https://token.sensenova.cn/v1` (default)
- **Models**:
  - Text: `sensenova-6.7-flash-lite`
  - Image: `sensenova-u1-fast`

## Environment Setup

```bash
# Required
export MINIMAX_API_KEY="sk-..."
export SENSENOVA_API_KEY="sk-..."

# Optional
export MINIMAX_API_BASE="https://api.minimax.chat/v1"
export SENSENOVA_API_BASE="https://token.sensenova.cn/v1"
```

## Usage Patterns

### Office Automation
```
User: Create an Excel report
Agent: Load office-automation skill → control Excel via COM
```

### PPT Generation
```
User: Create a presentation from this document
Agent: Load ppt-generator skill → generate SVG pages → convert to PPTX
```

### AI Media Generation
```
User: Generate an image
Agent: Load image-generation skill → call MiniMax API → return image URL
```

## File Structure

```
superoffice/
├── skills/
│   ├── superoffice-core/     # This skill
│   ├── office-automation/    # COM automation
│   ├── ppt-generator/        # PPT creation
│   ├── excel-analysis/       # Data analysis
│   ├── document-handler/     # Document processing
│   ├── image-generation/     # AI images
│   ├── video-generation/     # AI videos
│   ├── music-generation/     # AI music
│   ├── tts-audio/            # TTS
│   └── deep-research/        # Research
├── scripts/                  # Shared Python scripts
├── templates/                # PPT templates, icons, charts
└── references/               # API docs, guides
```

## Error Handling

- Missing API keys → Prompt user to configure `.env`
- Office automation fails → Fallback to python-pptx for PPT generation
- API rate limits → Implement exponential backoff
- Network errors → Retry with timeout

## Dependencies

- Python 3.10+
- httpx (API calls)
- python-dotenv (env config)
- pywin32 (Windows COM, optional)