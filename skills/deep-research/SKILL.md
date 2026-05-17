---
name: deep-research
description: AI-powered deep research with multi-dimensional evidence gathering and synthesis
triggers:
  - /research
  - /deep-research
  - research topic
  - generate report
  - investigation
metadata:
  tier: 1
  category: ai-media
  visibility: public
---

# Deep Research Skill

AI-powered deep research with multi-dimensional evidence gathering and synthesis. Based on SenseNova-Skills.

## Features

- **Research Planning**: Create structured research plans
- **Multi-source Search**: Academic, code, social media, news
- **Evidence Gathering**: Per-dimension research with filtering
- **Cross-validation**: Validate evidence across sources
- **Synthesis**: Combine findings into coherent analysis
- **Report Generation**: Markdown/HTML report with citations

## Pipeline

```
User Request → Planning → Per-Dimension Research → Synthesis → Final Report
```

### Phases

1. **Planning**: Analyze request, create research plan with dimensions
2. **Dimension Research**: Execute search for each dimension
3. **Evidence Filtering**: Filter, cross-validate evidence
4. **Synthesis**: Combine findings, identify consensus/conflicts
5. **Report**: Generate final report with citations

## Tools

### plan_research(request, output_dir)
Create research plan.
- request: research topic/question
- output_dir: where to save plan
- Returns: plan.json with dimensions, search strategies

### research_dimension(dimension, plan_path)
Execute research for one dimension.
- dimension: dimension name from plan
- plan_path: path to plan.json
- Returns: dimension report with evidence

### synthesize_findings(dimension_reports)
Synthesize findings across dimensions.
- dimension_reports: list of dimension report paths
- Returns: synthesis report with consensus, conflicts, uncertainties

### generate_report(synthesis, format='markdown')
Generate final report.
- synthesis: synthesis report path
- format: 'markdown', 'html', 'pdf'
- Returns: final report path

### search_academic(query, max_results=10)
Search academic sources.
- Sources: ArXiv, Semantic Scholar, PubMed, Wikipedia

### search_code(query, max_results=10)
Search code/programming sources.
- Sources: GitHub, Stack Overflow, Hacker News, HuggingFace

### search_social(query, platform='all', max_results=10)
Search social media.
- Platforms: Bilibili, Zhihu, Douyin (CN) or Reddit, Twitter, YouTube (EN)

## Usage Examples

### Start research
```
/research start on "impact of AI on software development"
```

### With dimensions
```
/research plan topic="AI trends 2025" dimensions="technology,market,ethics"
```

### Generate report
```
/research generate report from research_data format html
```

## Search Capabilities

### Academic Search
- ArXiv (papers with abstract)
- Semantic Scholar (with citations)
- PubMed (with PMC full text)
- Wikipedia

### Code Search
- GitHub (repo, code, issues)
- Stack Overflow
- Hacker News
- HuggingFace (models, datasets)

### Social Search
- Chinese: Bilibili, Zhihu, Douyin
- English: Reddit, Twitter/X, YouTube

## Requirements

- Python 3.9+
- httpx
- beautifulsoup4 (for web scraping)
- python-dotenv

## Output

- `plan.json` - Research plan
- `dimension_*.md` - Per-dimension reports
- `synthesis.md` - Synthesis report
- `report.md` / `report.html` - Final report