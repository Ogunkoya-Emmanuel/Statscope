"""
Visualization functions - Creates all charts and graphs
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def create_distribution_chart(data: np.ndarray, column_name: str):
    """Create histogram showing distribution of numeric data."""
    data = data[~np.isnan(data)]
    
    if len(data) == 0:
        fig, ax = plt.subplots(figsize=(8, 3))
        ax.text(0.5, 0.5, 'No data available', ha='center', va='center', 
                transform=ax.transAxes)
        return fig
    
    bins = min(50, int(np.sqrt(len(data))))
    fig, ax = plt.subplots(figsize=(8, 3))
    ax.hist(data, bins=bins, color="skyblue", edgecolor="black")
    ax.set_title(f"Distribution of {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Count")
    plt.tight_layout()
    return fig


def create_correlation_heatmap(corr_matrix):
    """Create correlation heatmap for numeric columns."""
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(
        corr_matrix,
        annot=True,
        cmap="coolwarm",
        center=0,
        fmt='.2f',
        ax=ax
    )
    ax.set_title("How the numbers relate to each other")
    plt.tight_layout()
    return fig


def create_category_bar_chart(value_counts, column_name: str):
    """Create bar chart for categorical data."""
    fig, ax = plt.subplots(figsize=(8, 4))
    value_counts.plot(kind="bar", ax=ax, color="lightcoral")
    ax.set_title(f"Most common values in {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Count")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    return fig