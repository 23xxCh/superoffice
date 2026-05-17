---
name: excel-analysis
description: AI-powered Excel data analysis, cleaning, visualization and reporting
triggers:
  - /excel
  - /analyze
  - data analysis
  - excel analysis
  - spreadsheet
metadata:
  tier: 1
  category: office
  visibility: public
---

# Excel Analysis Skill

AI-powered Excel data analysis, cleaning, and visualization. Based on SenseNova-Skills.

## Features

- **Multi-sheet reading**: Load and process multiple Excel sheets
- **Large file handling**: Auto-detect >=10k rows, switch to Parquet format
- **Data cleaning**: Remove duplicates, handle missing values, data type conversion
- **Conditional filtering**: Filter by conditions, search, sort
- **Cross-sheet aggregation**: Merge and aggregate data across sheets
- **Chart generation**: Create bar, line, pie, scatter, area charts
- **Export**: Excel (.xlsx, .xlsm), CSV, TSV formats

## Tools

### read_excel(file_path, sheet_name=None)
Read Excel file and return data as DataFrame.
- Returns: dict with 'data', 'columns', 'sheet_names'

### analyze_data(file_path, analysis_type='summary')
Perform data analysis.
- analysis_type: 'summary', 'statistics', 'correlation', 'outliers'

### clean_data(file_path, operations)
Clean data with specified operations.
- operations: 'remove_duplicates', 'fill_missing', 'normalize', 'convert_types'

### filter_data(file_path, conditions)
Filter data by conditions.
- conditions: dict of column -> value/condition pairs

### aggregate_data(file_path, group_by, agg_funcs)
Aggregate data by grouping columns.
- agg_funcs: 'sum', 'mean', 'count', 'min', 'max', etc.

### create_chart(file_path, chart_type, data_range, title)
Create a chart in the Excel file.
- chart_type: 'bar', 'line', 'pie', 'scatter', 'area', 'radar'

### export_data(data, output_path, format='xlsx')
Export data to file.
- format: 'xlsx', 'csv', 'tsv'

## Usage Examples

### Analyze sales data
```
/excel analyze sales_2024.xlsx summary
```

### Clean and filter
```
/excel clean data.xlsx remove_duplicates fill_missing
/excel filter data.xlsx region=East sales>10000
```

### Create chart
```
/excel chart data.xlsx bar A1:D10 "Monthly Sales"
```

### Aggregate by category
```
/excel aggregate sales.xlsx group_by=category agg_funcs=sum,mean
```

## Large File Handling

| Rows | Strategy |
|------|----------|
| < 10k | Standard pandas read |
| 10k-100k | Parquet conversion |
| > 100k | Streaming reader (openpyxl iter_rows) |

## Requirements

- Python 3.9+
- pandas
- openpyxl
- pyarrow (for Parquet)

## Output Formats

- `.xlsx` - Excel workbook
- `.xlsm` - Excel macro-enabled
- `.csv` - Comma-separated
- `.tsv` - Tab-separated