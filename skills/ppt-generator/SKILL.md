---
name: ppt-generator
description: AI-powered PPT creation from documents - PDF, DOCX, Markdown to native PPTX
triggers:
  - /ppt
  - /presentation
  - create ppt
  - create slides
  - presentation generation
metadata:
  tier: 1
  category: office
  visibility: public
---

# PPT Generator Skill

AI-powered PowerPoint generation from various document sources. Based on ppt-master.

## Features

- **Multi-source input**: PDF, DOCX, PPTX, XLSX, EPUB, HTML, LaTeX, Markdown, plain text, URLs
- **Native PPTX output**: Real PowerPoint shapes (DrawingML), not images
- **70+ chart templates**: Bar, line, pie, donut, area, scatter, radar, waterfall, Gantt, etc.
- **15+ layout templates**: Corporate, academic, government, medical, tech, consulting
- **Multi-canvas formats**: 16:9, 4:3,小红书(3:4), 抖音/快手(9:16), 微信朋友圈(1:1)
- **Animations**: 22+ entrance effects, page transitions
- **TTS narration**: Edge TTS, ElevenLabs, MiniMax, voice cloning support

## Pipeline

```
Source Document → Markdown → Strategist → Image Generation → Executor (SVG) → QC → Post-Process → PPTX
```

### Phases

1. **Source Ingestion**: Convert input to Markdown
2. **Strategist**: Analyze content, propose design spec ("Eight Confirmations")
3. **Image Generation**: Create AI images or search web images
4. **Executor**: Generate SVG pages with precise layouts
5. **Quality Check**: Validate SVG structure
6. **Post-Processing**: Convert SVG to DrawingML, embed media

## Usage Examples

### Generate from document
```
/ppt create from report.pdf style corporate
```

### Custom canvas
```
/ppt create from doc.md canvas 9:16 for tiktok
```

### With narration
```
/ppt create from content.md voice professional narration
```

## Design Executors

| Executor | Use Case |
|----------|----------|
| General | Training, tech talks |
| Consultant | Business reports, data viz |
| Consultant Top | MBB-level (McKinsey/Bain/BCG) |

## Canvas Formats

| Format | Dimensions | Use Case |
|--------|------------|----------|
| 16:9 | 1280x720 | Standard presentations |
| 4:3 | 1024x768 | Traditional projectors |
| 小红书 | 1242x1660 | Social sharing |
| 朋友圈/IG | 1080x1080 | Square posts |
| 抖音/Story | 1080x1920 | Vertical videos |
| 横版Banner | 1920x1080 | Web banners |
| 竖版海报 | 1080x1920 | Mobile screens |
| A4打印 | 1240x1754 | Print materials |

## Chart Templates

- Bar charts (vertical, horizontal, stacked, grouped)
- Line charts (single, multi, area)
- Pie & Donut charts
- Radar charts
- Waterfall charts
- Gantt charts
- Heatmaps
- Treemaps
- Funnel charts
- Sankey diagrams
- KPI cards
- Comparison tables
- Mind maps
- Process flows

## Requirements

- Python 3.10+
- python-pptx
- Pillow
- cairosvg
- edge-tts (for narration)

## Output

- Native editable `.pptx` file
- Fallback SVG-rendered `.pptx`
- Speaker notes per slide