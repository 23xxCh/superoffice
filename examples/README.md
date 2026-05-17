# SuperOffice 示例项目

本目录包含使用 SuperOffice 技能的示例项目。

## 示例列表

### 1. Office 自动化示例
- **文件**: `office-demo/`
- **功能**: 创建Excel报表、生成Word文档
- **使用技能**: office-automation

### 2. PPT生成示例
- **文件**: `ppt-demo/`
- **功能**: 从Markdown生成演示文稿
- **使用技能**: ppt-generator

### 3. Excel数据分析示例
- **文件**: `excel-demo/`
- **功能**: 数据清洗、统计分析、图表生成
- **使用技能**: excel-analysis

### 4. AI媒体生成示例
- **文件**: `media-demo/`
- **功能**: 生成图像、视频、音乐
- **使用技能**: image-generation, video-generation, music-generation

### 5. 深度研究示例
- **文件**: `research-demo/`
- **功能**: 研究规划、证据收集、报告生成
- **使用技能**: deep-research

---

## 快速运行示例

### Office 自动化

```python
# 导入Office自动化模块
from scripts.office_automation import Officer

# 创建Officer实例
officer = Officer()

# 启动Excel
officer.launch_app("Excel", visible=True)

# 创建新工作簿
code = '''
wb = app.Workbooks.Add()
ws = wb.ActiveSheet
ws.Cells(1, 1).Value = "Hello SuperOffice!"
wb.SaveAs("demo.xlsx")
wb.Close()
output = "Excel文件已创建"
'''
result = officer.run_python(code)
print(result)
```

### PPT生成

```python
# 使用PPT生成器
from scripts.ppt_converter.svg_to_pptx import create_pptx_from_svg

# 将SVG文件转换为PPTX
create_pptx_from_svg(
    svg_dir="slides/",
    output_path="presentation.pptx",
    canvas_format="16:9"
)
```

### Excel分析

```python
# 使用Excel分析器
from scripts.excel_analysis.analyzer import get_analyzer

analyzer = get_analyzer()

# 读取Excel
result = analyzer.read_excel("data.xlsx")
print(f"行数: {result['row_count']}")

# 分析数据
analysis = analyzer.analyze_data("data.xlsx", "summary")
print(analysis)
```

### AI图像生成

```python
# 使用图像生成器
from scripts.api_clients.image_gen import SyncImageGenerator

generator = SyncImageGenerator()

# 生成图像
result = generator.generate(
    prompt="a beautiful sunset over mountains",
    provider="minimax"
)
print(result)
```

### AI视频生成

```python
# 使用视频生成器
from scripts.api_clients.video_gen import SyncVideoGenerator

generator = SyncVideoGenerator()

# 生成视频
result = generator.generate(
    prompt="a cat playing in a garden",
    model="MiniMax-Hailuo-2.3"
)
print(result)
```

---

## 下一步

1. 查看各技能的 `SKILL.md` 了解详细用法
2. 配置 `.env` 文件添加你的API密钥
3. 运行示例代码开始使用
4. 根据需要修改和扩展技能