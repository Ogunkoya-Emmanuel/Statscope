"""
Data analysis functions - Handles all data processing and insight generation
"""

import pandas as pd
import textwrap
import matplotlib.pyplot as plt
import seaborn as sns
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO


def clean_numeric_series(series: pd.Series) -> pd.Series:
    """Convert common formats (currency, percentages, commas) to numeric values."""
    cleaned = (
        series.astype(str)
        .str.replace(r"[,%₦$€£]", "", regex=True)
        .str.strip()
    )
    return pd.to_numeric(cleaned, errors="coerce")


def identify_date_range(df: pd.DataFrame) -> str:
    for col in df.columns:
        if df[col].dtype == "object":
            dates = pd.to_datetime(df[col], errors="coerce")
            if dates.notna().mean() > 0.7:
                return f"{dates.min().date()} to {dates.max().date()}"
    return "No date column detected"


def get_dataset_overview(df: pd.DataFrame) -> dict:
    return {
        "total_rows": len(df),
        "total_columns": len(df.columns),
        "date_range": identify_date_range(df),
    }


def check_missing_data(df: pd.DataFrame) -> list:
    missing = df.isnull().sum()
    return [
        {
            "column": col,
            "count": int(missing[col]),
            "percentage": (missing[col] / len(df)) * 100
        }
        for col in missing[missing > 0].index
    ]


def generate_numeric_insight(column: str, series: pd.Series, beginner: bool = True) -> str:
    mean = series.mean()
    median = series.median()
    min_val = series.min()
    max_val = series.max()

    if beginner:
        insights = [f"For **{column}**, most values are centered around **{mean:.2f}**."]
        
        range_size = max_val - min_val
        if range_size == 0:
            insights.append("All values are the same.")
        elif range_size < mean:
            insights.append("Values stay fairly close together.")
        else:
            insights.append("Values vary quite a bit across the dataset.")
        
        if mean > median:
            insights.append("A few higher values pull the average upward.")
        elif mean < median:
            insights.append("A few lower values pull the average downward.")
        
        insights.append(f"Typical range: **{min_val:.2f}** to **{max_val:.2f}**.")
        return " ".join(insights)
    
    return f"Mean: {mean:.2f}, Median: {median:.2f}, Std: {series.std():.2f}"


def is_likely_identifier(series: pd.Series, column_name: str, df: pd.DataFrame) -> bool:
    name = column_name.lower()
    if any(x in name for x in ["id", "uuid", "index", "key"]):
        return True
    return series.nunique() / len(df) > 0.95


def analyze_numeric_columns(df: pd.DataFrame, max_columns: int = 3, beginner: bool = True) -> list:
    df_working = df.copy()
    results = []
    numeric_cols = list(df_working.select_dtypes(include="number").columns)

    for col in df_working.select_dtypes(include="object").columns:
        cleaned = clean_numeric_series(df_working[col])
        if cleaned.notna().mean() > 0.6:
            df_working[col] = cleaned
            numeric_cols.append(col)

    for col in numeric_cols:
        series = df_working[col].dropna()

        if series.empty or is_likely_identifier(series, col, df_working):
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = int(((series < lower) | (series > upper)).sum())

        results.append({
            "column": col,
            "mean": series.mean(),
            "median": series.median(),
            "min": series.min(),
            "max": series.max(),
            "std": series.std(),
            "outlier_count": outlier_count,
            "insight": generate_numeric_insight(col, series, beginner),
            "values": series.values
        })

        if len(results) >= max_columns:
            break

    return results


def find_correlations(df: pd.DataFrame, threshold: float = 0.5) -> list:
    numeric = df.select_dtypes(include="number")
    if numeric.shape[1] < 2:
        return []

    corr = numeric.corr()
    results = []

    for i in range(len(corr.columns)):
        for j in range(i + 1, len(corr.columns)):
            if abs(corr.iloc[i, j]) >= threshold:
                results.append({
                    "column1": corr.columns[i],
                    "column2": corr.columns[j],
                    "correlation": corr.iloc[i, j],
                    "direction": "positive" if corr.iloc[i, j] > 0 else "negative"
                })
    return results


def get_correlation_matrix(df: pd.DataFrame):
    numeric = df.select_dtypes(include="number")
    return numeric.corr() if numeric.shape[1] >= 2 else None


def analyze_categorical_columns(df: pd.DataFrame, max_columns: int = 2) -> list:
    results = []
    for col in df.select_dtypes(include="object").columns[:max_columns]:
        results.append({
            "column": col,
            "unique_count": df[col].nunique(),
            "top_values": df[col].value_counts().head(10)
        })
    return results


def generate_pdf_report(dataset_name: str, overview: dict, numeric: list, corr_matrix, categories: list):
    try:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        margin_x, y = 50, height - 50

        def new_page():
            nonlocal y
            c.showPage()
            y = height - 50
            c.setFont("Helvetica", 11)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(margin_x, y, "Statscope Report")
        y -= 25

        c.setFont("Helvetica-Oblique", 11)
        c.drawString(margin_x, y, f"Dataset: {dataset_name}")
        y -= 30

        c.setFont("Helvetica", 11)
        c.drawString(margin_x, y, f"Rows: {overview['total_rows']}")
        y -= 15
        c.drawString(margin_x, y, f"Columns: {overview['total_columns']}")
        y -= 15
        c.drawString(margin_x, y, f"Date range: {overview['date_range']}")
        y -= 30

        c.setFont("Helvetica-Bold", 13)
        c.drawString(margin_x, y, "Numeric Insights")
        y -= 20

        for stat in numeric:
            if y < 250:
                new_page()

            c.setFont("Helvetica-Bold", 12)
            c.drawString(margin_x, y, stat["column"])
            y -= 15

            for line in textwrap.wrap(stat["insight"], 90):
                c.setFont("Helvetica", 11)
                c.drawString(margin_x, y, line)
                y -= 14

            fig, ax = plt.subplots(figsize=(4, 2))
            ax.hist(stat["values"], bins=20, color="skyblue")
            ax.set_title(stat["column"])
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=150)
            plt.close(fig)
            buf.seek(0)

            c.drawImage(ImageReader(buf), margin_x, y - 120, 300, 120)
            y -= 150

        if corr_matrix is not None and not corr_matrix.empty:
            if y < 300:
                new_page()

            c.setFont("Helvetica-Bold", 13)
            c.drawString(margin_x, y, "Correlation Matrix")
            y -= 20

            fig, ax = plt.subplots(figsize=(4, 4))
            sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
            ax.set_title("Correlation Matrix")
            
            buf = BytesIO()
            fig.savefig(buf, format="png", dpi=150, bbox_inches="tight")
            plt.close(fig)
            buf.seek(0)
            
            c.drawImage(ImageReader(buf), margin_x, y - 260, width=300, height=260)
            y -= 280

        c.save()
        buffer.seek(0)
        return buffer
    
    except Exception as e:
        print(f"PDF generation error: {e}")
        return None