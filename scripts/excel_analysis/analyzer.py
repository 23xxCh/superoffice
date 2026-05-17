"""
Excel Analysis - Data processing and analysis for Excel files
Based on SenseNova-Skills project
"""

import os
import json
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Dict, List, Optional, Union, Any
from dataclasses import dataclass


@dataclass
class ExcelAnalysisConfig:
    """Configuration for Excel analysis"""
    large_file_threshold: int = 10000  # Rows to trigger Parquet
    streaming_threshold: int = 100000   # Rows for streaming mode
    chunk_size: int = 10000


class ExcelAnalyzer:
    """Excel data analysis and manipulation"""

    def __init__(self, config: Optional[ExcelAnalysisConfig] = None):
        self.config = config or ExcelAnalysisConfig()

    def read_excel(self, file_path: str, sheet_name: Optional[str] = None) -> Dict:
        """Read Excel file and return data as dict"""
        path = Path(file_path)
        if not path.exists():
            return {"error": f"File not found: {file_path}"}

        # Check file size for large file handling
        file_size = path.stat().st_size
        row_count = self._estimate_row_count(file_path, sheet_name)

        try:
            # Large file handling
            if row_count >= self.config.large_file_threshold:
                return self._read_large_file(file_path, sheet_name)

            # Standard read
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            return self._dataframe_to_dict(df, sheet_name)

        except Exception as e:
            return {"error": str(e)}

    def _estimate_row_count(self, file_path: str, sheet_name: Optional[str]) -> int:
        """Estimate row count without loading full file"""
        try:
            # Quick check using openpyxl
            from openpyxl import load_workbook
            wb = load_workbook(file_path, read_only=True, data_only=True)
            ws = wb.active if not sheet_name else wb[sheet_name]
            # Estimate from dimensions
            max_row = ws.max_row or 0
            wb.close()
            return max_row
        except:
            return 0

    def _read_large_file(self, file_path: str, sheet_name: Optional[str]) -> Dict:
        """Handle large Excel files with Parquet conversion"""
        if row_count >= self.config.streaming_threshold:
            return self._read_streaming(file_path, sheet_name)

        # Convert to Parquet for faster processing
        parquet_path = Path(file_path).with_suffix('.parquet')
        df = pd.read_excel(file_path, sheet_name=sheet_name)
        df.to_parquet(parquet_path, index=False)

        return {
            "data": df.to_dict(orient='records'),
            "columns": list(df.columns),
            "row_count": len(df),
            "sheet_names": pd.ExcelFile(file_path).sheet_names,
            "parquet_available": str(parquet_path),
            "format": "parquet_conversion"
        }

    def _read_streaming(self, file_path: str, sheet_name: Optional[str]) -> Dict:
        """Streaming read for very large files"""
        from openpyxl import load_workbook

        wb = load_workbook(file_path, read_only=True)
        ws = wb.active if not sheet_name else wb[sheet_name]

        rows = []
        headers = None

        for i, row in enumerate(ws.iter_rows(values_only=True)):
            if i == 0:
                headers = list(row)
                continue
            if row and any(cell is not None for cell in row):
                rows.append(dict(zip(headers, row)))

            if i >= self.config.streaming_threshold:
                break

        wb.close()
        return {
            "data": rows,
            "columns": headers,
            "row_count": len(rows),
            "truncated": True,
            "original_estimate": self._estimate_row_count(file_path, sheet_name)
        }

    def _dataframe_to_dict(self, df: pd.DataFrame, sheet_name: Optional[str]) -> Dict:
        """Convert DataFrame to dict response"""
        return {
            "data": df.to_dict(orient='records'),
            "columns": list(df.columns),
            "row_count": len(df),
            "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()},
            "sheet_names": [sheet_name] if sheet_name else []
        }

    def analyze_data(self, file_path: str, analysis_type: str = 'summary') -> Dict:
        """Perform data analysis"""
        result = self.read_excel(file_path)
        if "error" in result:
            return result

        df = pd.DataFrame(result["data"])

        if analysis_type == 'summary':
            return {
                "row_count": len(df),
                "column_count": len(df.columns),
                "columns": list(df.columns),
                "dtypes": result.get("dtypes", {}),
                "null_counts": df.isnull().sum().to_dict(),
                "memory_usage": df.memory_usage(deep=True).sum()
            }

        elif analysis_type == 'statistics':
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            return {
                "numeric_columns": list(numeric_cols),
                "statistics": df[numeric_cols].describe().to_dict()
            }

        elif analysis_type == 'correlation':
            numeric_df = df.select_dtypes(include=[np.number])
            return {
                "correlation_matrix": numeric_df.corr().to_dict()
            }

        elif analysis_type == 'outliers':
            numeric_df = df.select_dtypes(include=[np.number])
            outliers = {}
            for col in numeric_df.columns:
                Q1 = numeric_df[col].quantile(0.25)
                Q3 = numeric_df[col].quantile(0.75)
                IQR = Q3 - Q1
                outliers[col] = int(((numeric_df[col] < Q1 - 1.5*IQR) |
                                     (numeric_df[col] > Q3 + 1.5*IQR)).sum())
            return {"outliers": outliers}

        return {"error": f"Unknown analysis type: {analysis_type}"}

    def clean_data(self, file_path: str, operations: List[str],
                   output_path: Optional[str] = None) -> Dict:
        """Clean data with specified operations"""
        result = self.read_excel(file_path)
        if "error" in result:
            return result

        df = pd.DataFrame(result["data"])

        for op in operations:
            if op == 'remove_duplicates':
                df = df.drop_duplicates()
            elif op == 'fill_missing':
                df = df.fillna('')
            elif op == 'drop_missing':
                df = df.dropna()
            elif op == 'normalize':
                # Normalize string columns
                for col in df.select_dtypes(include=['object']).columns:
                    df[col] = df[col].str.strip().str.lower()

        output = output_path or file_path
        df.to_excel(output, index=False)

        return {
            "output": output,
            "operations_applied": operations,
            "row_count": len(df)
        }

    def filter_data(self, file_path: str, conditions: Dict[str, Any],
                    output_path: Optional[str] = None) -> Dict:
        """Filter data by conditions"""
        result = self.read_excel(file_path)
        if "error" in result:
            return result

        df = pd.DataFrame(result["data"])

        for col, condition in conditions.items():
            if col not in df.columns:
                continue

            if isinstance(condition, dict):
                # Complex condition: {">": 100, "<": 1000, "==": "value"}
                for op, value in condition.items():
                    if op == ">":
                        df = df[df[col] > value]
                    elif op == "<":
                        df = df[df[col] < value]
                    elif op == ">=":
                        df = df[df[col] >= value]
                    elif op == "<=":
                        df = df[df[col] <= value]
                    elif op == "==":
                        df = df[df[col] == value]
                    elif op == "!=":
                        df = df[df[col] != value]
                    elif op == "contains":
                        df = df[df[col].astype(str).str.contains(value, na=False)]
            else:
                # Simple equality
                df = df[df[col] == condition]

        output = output_path or file_path.replace('.xlsx', '_filtered.xlsx')
        df.to_excel(output, index=False)

        return {
            "output": output,
            "conditions": conditions,
            "row_count": len(df)
        }

    def aggregate_data(self, file_path: str, group_by: List[str],
                       agg_funcs: Dict[str, str],
                       output_path: Optional[str] = None) -> Dict:
        """Aggregate data by grouping columns"""
        result = self.read_excel(file_path)
        if "error" in result:
            return result

        df = pd.DataFrame(result["data"])

        if not all(col in df.columns for col in group_by):
            return {"error": "Invalid group_by columns"}

        # Convert agg_funcs to pandas format
        agg_dict = {}
        numeric_cols = df.select_dtypes(include=[np.number]).columns

        if not agg_funcs:
            # Default: sum all numeric columns
            agg_dict = {col: 'sum' for col in numeric_cols}
        else:
            agg_dict = agg_funcs

        grouped = df.groupby(group_by).agg(agg_dict).reset_index()

        output = output_path or file_path.replace('.xlsx', '_aggregated.xlsx')
        grouped.to_excel(output, index=False)

        return {
            "output": output,
            "group_by": group_by,
            "agg_funcs": agg_dict,
            "row_count": len(grouped)
        }

    def create_chart(self, file_path: str, chart_type: str,
                     data_range: str, title: str,
                     output_path: Optional[str] = None) -> Dict:
        """Create a chart in Excel"""
        from pptx import Presentation
        from pptx.chart.data import CategoryChartData
        from pptx.enum.chart import XL_CHART_TYPE
        from pptx.util import Inches

        # Parse data range (e.g., "A1:D10")
        # This is a simplified version - real implementation would parse Excel range
        result = self.read_excel(file_path)
        if "error" in result:
            return result

        # Create a new presentation with the chart
        prs = Presentation()
        slide = prs.slides.add_slide(prs.slide_layouts[5])  # Title only

        # Add chart to slide
        chart_data = CategoryChartData()
        chart_data.categories = result["data"][:10]  # First 10 rows
        chart_data.add_series('Series 1', [1, 2, 3, 4, 5])

        chart_type_map = {
            'bar': XL_CHART_TYPE.COLUMN_CLUSTERED,
            'line': XL_CHART_TYPE.LINE,
            'pie': XL_CHART_TYPE.PIE,
            'scatter': XL_CHART_TYPE.XY_SCATTER,
            'area': XL_CHART_TYPE.AREA,
        }

        x, y, cx, cy = Inches(1), Inches(2), Inches(8), Inches(4.5)
        slide.shapes.add_chart(
            chart_type_map.get(chart_type, XL_CHART_TYPE.COLUMN_CLUSTERED),
            x, y, cx, cy, chart_data
        )

        output = output_path or file_path.replace('.xlsx', '_chart.pptx')
        prs.save(output)

        return {"output": output, "chart_type": chart_type}

    def export_data(self, data: List[Dict], output_path: str,
                    format: str = 'xlsx') -> Dict:
        """Export data to file"""
        df = pd.DataFrame(data)

        if format == 'xlsx':
            df.to_excel(output_path, index=False)
        elif format == 'csv':
            df.to_csv(output_path, index=False)
        elif format == 'tsv':
            df.to_csv(output_path, sep='\t', index=False)
        else:
            return {"error": f"Unknown format: {format}"}

        return {"output": output_path, "row_count": len(df), "format": format}


# Singleton instance
_analyzer = None


def get_analyzer() -> ExcelAnalyzer:
    """Get singleton analyzer instance"""
    global _analyzer
    if _analyzer is None:
        _analyzer = ExcelAnalyzer()
    return _analyzer


# CLI entry point
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python excel_analysis.py <command> <file> [args...]")
        print("Commands: read, analyze, clean, filter, aggregate, chart, export")
        sys.exit(1)

    command = sys.argv[1]
    file_path = sys.argv[2]
    analyzer = get_analyzer()

    if command == "read":
        print(json.dumps(analyzer.read_excel(file_path), indent=2, default=str))
    elif command == "analyze":
        analysis_type = sys.argv[3] if len(sys.argv) > 3 else "summary"
        print(json.dumps(analyzer.analyze_data(file_path, analysis_type), indent=2, default=str))