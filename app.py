"""
Main Streamlit application - Coordinates analysis and displays results
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from analyzer import (
    get_dataset_overview,
    check_missing_data,
    analyze_numeric_columns,
    find_correlations,
    analyze_categorical_columns,
    get_correlation_matrix,
    generate_pdf_report
)

from visualizer import (
    create_distribution_chart,
    create_correlation_heatmap,
    create_category_bar_chart
)


st.set_page_config(page_title="📊Statscope", page_icon="📊")

st.title("Statscope")
st.write("Upload a CSV or Excel file to get clear, human-friendly insights.")
st.caption("Supported formats: CSV, Excel (.xlsx, .xls)")

uploaded_file = st.file_uploader("Choose a data file", type=["csv", "xlsx", "xls"])

explain_like_new = st.toggle("Explain everything like I'm new", value=True)

use_sample = st.checkbox("Use sample dataset (no upload needed)")

if not use_sample and uploaded_file is None:
    st.info("Check the box above to explore Statscope with a sample dataset — no upload needed.")


df = None
dataset_name = None

if use_sample:
    df = pd.read_csv("data/sample_dataset.csv")
    dataset_name = "Sample Dataset"
    st.info("Using built-in sample dataset")

elif uploaded_file:
    file_name = uploaded_file.name.lower()
    dataset_name = uploaded_file.name

    try:
        if file_name.endswith(".csv"):
            try:
                df = pd.read_csv(uploaded_file)
            except UnicodeDecodeError:
                df = pd.read_csv(uploaded_file, encoding="latin-1")
                st.info("Loaded CSV using Latin-1 encoding")

        elif file_name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
            st.info("Loaded Excel file successfully")

    except Exception as e:
        st.error("Failed to read the uploaded file.")
        st.exception(e)
        st.stop()


if df is not None:

    st.success(f"Loaded {len(df):,} rows × {len(df.columns)} columns")

    with st.expander("Preview data"):
        st.dataframe(df.head())

    st.markdown("---")

    st.subheader("1. Dataset Overview")
    overview = get_dataset_overview(df)
    st.write(
        f"- Rows: **{overview['total_rows']:,}**\n"
        f"- Columns: **{overview['total_columns']}**\n"
        f"- Date range: **{overview['date_range']}**"
    )

    st.subheader("2. Data Quality")
    missing = check_missing_data(df)

    if missing:
        st.warning("Missing values detected:")
        for item in missing:
            st.write(f"- **{item['column']}**: {item['count']} missing ({item['percentage']:.1f}%)")
    else:
        st.success("No missing data found.")

    st.subheader("3. What the numbers are telling you")
    numeric_analysis = analyze_numeric_columns(df, beginner=explain_like_new)

    if numeric_analysis:
        for stats in numeric_analysis:
            st.markdown(f"### {stats['column']}")
            st.write(stats["insight"])

            fig = create_distribution_chart(stats["values"], stats["column"])
            st.pyplot(fig)
            plt.close()

            with st.expander("Technical details"):
                st.write(f"- Average: {stats['mean']:.2f}")
                st.write(f"- Median: {stats['median']:.2f}")
                st.write(f"- Range: {stats['min']:.2f} → {stats['max']:.2f}")
                st.write(f"- Outliers detected: {stats['outlier_count']}")
    else:
        st.info("No usable numeric columns found.")

    st.subheader("4. Relationships between numbers")
    correlations = find_correlations(df)

    if correlations:
        st.caption("Correlation shows association — not causation.")

        if explain_like_new:
            st.info(
                "Blue = values increase together | "
                "Red = one increases while the other decreases | "
                "Darker color = stronger relationship"
            )

        for corr in correlations:
            emoji = "+" if corr["direction"] == "positive" else "-"
            st.write(
                f"[{emoji}] **{corr['column1']}** vs **{corr['column2']}** "
                f"(strength: {abs(corr['correlation']):.2f})"
            )

        corr_matrix = get_correlation_matrix(df)
        if corr_matrix is not None:
            fig = create_correlation_heatmap(corr_matrix)
            st.pyplot(fig)
            plt.close()
            
            st.caption(
                "Values close to 1 = strong positive relationship | "
                "Values close to -1 = strong negative relationship | "
                "Values near 0 = little or no relationship"
            )
    else:
        st.info("No strong relationships detected.")

    st.subheader("5. Categories")
    categories = analyze_categorical_columns(df)

    for cat in categories:
        st.markdown(f"**{cat['column']}** ({cat['unique_count']} unique values)")
        if cat["top_values"] is not None:
            fig = create_category_bar_chart(cat["top_values"], cat["column"])
            st.pyplot(fig)
            plt.close()
        else:
            st.caption("Too many unique values to visualize.")

    st.markdown("---")

    corr_matrix = get_correlation_matrix(df)
    pdf = generate_pdf_report(dataset_name, overview, numeric_analysis, corr_matrix, categories)

    if pdf:
        st.download_button(
            "Download PDF report",
            data=pdf,
            file_name="statscope_report.pdf",
            mime="application/pdf",
        )

    st.success("Analysis complete")

else:
    st.info("Upload a data file or use the sample dataset to begin.")
