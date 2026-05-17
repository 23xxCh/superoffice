# SuperOffice - AI Office 自动化技能库

[English](README.md) | 中文

统一整合四大开源项目的AI Office技能库：
- **OfficeMCP** - Windows Office COM自动化
- **SenseNova-Skills** - 商汤日日新AI技能
- **ppt-master** - AI驱动PPT生成
- **MiniMax-AI/skills** - 文档处理和多媒体生成

## 功能特性

### 核心能力
- **Office自动化** - 通过Windows COM控制Word、Excel、PowerPoint、Outlook
- **PPT生成** - 从PDF/DOCX/MD文档AI生成演示文稿
- **Excel分析** - 数据清洗、分析、可视化
- **文档处理** - PDF生成、DOCX编辑、XLSX处理

### AI媒体 (MiniMax + SenseNova)
- AI图像生成 (MiniMax image-01)
- AI视频生成 (MiniMax Hailuo 2.3)
- AI音乐生成 (MiniMax music-2.6)
- 语音合成 (TTS)
- 深度研究与报告生成

## 快速开始

### 1. 克隆和安装

```bash
cd superoffice
pip install -r requirements.txt
```

### 2. 配置API密钥

复制 `.env.example` 到 `.env` 并添加密钥：

```bash
# MiniMax API
MINIMAX_API_KEY=YOUR_MINIMAX_API_KEY

# SenseNova API
SENSENOVA_API_KEY=YOUR_SENSENOVA_API_KEY
```

### 3. 安装MiniMax CLI (可选，用于媒体生成)

```bash
npm install -g mmx-cli
mmx auth login --api-key YOUR_MINIMAX_KEY
```

### 4. 支持的IDE

| IDE | 配置目录 |
|-----|----------|
| Claude Code | `.claude-plugin/` |
| Cursor | `.cursor-plugin/` |
| Codex | `.codex/` (符号链接) |
| OpenCode | `.opencode/` (符号链接) |

## 技能列表

| 技能 | 命令 | 说明 |
|------|------|------|
| office-automation | `/office` | 控制Office应用 |
| ppt-generator | `/ppt` | AI创建PPT |
| excel-analysis | `/excel` | 数据分析 |
| document-handler | `/doc` | PDF/DOCX/XLSX |
| image-generation | `/image` | AI图像生成 |
| video-generation | `/video` | AI视频(Hailuo) |
| music-generation | `/music` | AI音乐 |
| tts-audio | `/tts` | 语音合成 |
| deep-research | `/research` | 研究报告 |

## 使用示例

### 生成PPT
```
/ppt create from document.pdf style corporate
```

### 分析Excel数据
```
/excel analyze sales_data.xlsx chart bar
```

### AI生成图像
```
/image generate a futuristic city at sunset
```

### AI生成视频
```
/video generate a cat playing in a garden
```

## 技术栈

- **Python 3.10+** - 核心运行时
- **pywin32** - Windows COM自动化 (仅Windows)
- **python-pptx** - PPTX处理
- **pandas, openpyxl** - Excel处理
- **httpx** - API调用
- **Node.js + mmx-cli** - MiniMax CLI

## 许可证

MIT License

## 致谢

- [OfficeMCP](https://github.com/OfficeMCP/OfficeMCP)
- [SenseNova-Skills](https://github.com/OpenSenseNova/SenseNova-Skills)
- [ppt-master](https://github.com/hugohe3/ppt-master)
- [MiniMax-AI/skills](https://github.com/MiniMax-AI/skills)