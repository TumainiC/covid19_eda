
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# Configure the page
st.set_page_config(
    page_title="CORD-19 Data Explorer",
    page_icon="🦠",
    layout="wide"
)

@st.cache_data
def load_data():
    """Load and cache the dataset"""
    try:
        df = pd.read_csv('metadata.csv', low_memory=False)
        # Basic cleaning
        df_clean = df.dropna(subset=['title']) if 'title' in df.columns else df
        if 'journal' in df_clean.columns:
            df_clean['journal'] = df_clean['journal'].fillna('Unknown')
        if 'abstract' in df_clean.columns:
            df_clean['abstract'] = df_clean['abstract'].fillna('')

        # Date processing
        if 'publish_time' in df_clean.columns:
            df_clean['publish_date'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
            df_clean['publish_year'] = df_clean['publish_date'].dt.year

        # Feature engineering
        if 'title' in df_clean.columns:
            df_clean['title_length'] = df_clean['title'].str.len()
        if 'abstract' in df_clean.columns:
            df_clean['abstract_word_count'] = df_clean['abstract'].str.split().str.len()
            df_clean['abstract_word_count'] = df_clean['abstract_word_count'].fillna(0)

        return df_clean
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def main():
    """Main Streamlit application"""

    # Title and description
    st.title("🦠 CORD-19 Data Explorer")
    st.write("Interactive exploration of COVID-19 research papers")
    st.markdown("---")

    # Load data
    with st.spinner("Loading data..."):
        df = load_data()

    if df is None:
        st.error("Failed to load data. Please ensure metadata.csv is available.")
        return

    # Sidebar controls
    st.sidebar.header(" Data Filters")

    # Year range filter
    if 'publish_year' in df.columns:
        valid_years = df['publish_year'].dropna()
        if len(valid_years) > 0:
            min_year, max_year = int(valid_years.min()), int(valid_years.max())
            year_range = st.sidebar.slider(
                "Select Year Range",
                min_value=min_year,
                max_value=max_year,
                value=(max(2019, min_year), max_year),
                step=1
            )

            # Filter data by year
            df_filtered = df[df['publish_year'].between(year_range[0], year_range[1])]
        else:
            df_filtered = df
            year_range = None
    else:
        df_filtered = df
        year_range = None

    # Sample size control
    max_sample = min(10000, len(df_filtered))
    sample_size = st.sidebar.slider(
        "Sample Size (for performance)",
        min_value=1000,
        max_value=max_sample,
        value=min(5000, max_sample),
        step=1000
    )

    # Sample the data
    if len(df_filtered) > sample_size:
        df_display = df_filtered.sample(n=sample_size, random_state=42)
    else:
        df_display = df_filtered

    # Main content area
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Dataset Overview")
        st.metric("Total Papers", f"{len(df):,}")
        st.metric("Filtered Papers", f"{len(df_filtered):,}")
        st.metric("Display Sample", f"{len(df_display):,}")

        if year_range:
            st.metric("Year Range", f"{year_range[0]} - {year_range[1]}")

    with col2:
        st.subheader(" Quick Stats")
        if 'journal' in df_display.columns:
            st.metric("Unique Journals", df_display['journal'].nunique())
        if 'title_length' in df_display.columns:
            st.metric("Avg Title Length", f"{df_display['title_length'].mean():.0f} chars")
        if 'abstract_word_count' in df_display.columns:
            avg_abstract = df_display['abstract_word_count'].mean()
            st.metric("Avg Abstract Length", f"{avg_abstract:.0f} words")

    st.markdown("---")

    # Visualizations
    st.header(" Data Visualizations")

    # Publication trends
    if 'publish_year' in df_display.columns:
        st.subheader("Publications Over Time")
        yearly_counts = df_display['publish_year'].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(yearly_counts.index, yearly_counts.values, marker='o', linewidth=2)
        ax.set_title('Number of Publications by Year')
        ax.set_xlabel('Year')
        ax.set_ylabel('Number of Papers')
        ax.grid(True, alpha=0.3)
        st.pyplot(fig)

    # Top journals
    if 'journal' in df_display.columns:
        st.subheader("Top Publishing Journals")
        journal_counts = df_display['journal'].value_counts().head(10)

        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(journal_counts)), journal_counts.values)
        ax.set_title('Top 10 Journals by Paper Count')
        ax.set_xlabel('Journals')
        ax.set_ylabel('Number of Papers')
        ax.set_xticks(range(len(journal_counts)))
        ax.set_xticklabels([j[:30] + '...' if len(j) > 30 else j for j in journal_counts.index], 
                          rotation=45, ha='right')

        # Add value labels
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}', ha='center', va='bottom')

        st.pyplot(fig)

    # Title word analysis
    if 'title' in df_display.columns:
        st.subheader("Most Common Words in Titles")

        # Process titles
        all_titles = df_display['title'].dropna().str.lower()
        all_words = []
        stop_words = {'the', 'and', 'of', 'a', 'an', 'in', 'on', 'at', 'to', 'for', 'with', 'by', 'from', 'as', 'is', 'are', 'was', 'were'}

        for title in all_titles:
            words = title.replace(',', ' ').replace('.', ' ').replace(':', ' ').split()
            words = [word.strip('.,!?:;()[]{}') for word in words if len(word) > 2 and word not in stop_words]
            all_words.extend(words)

        word_counts = Counter(all_words)
        top_words = dict(word_counts.most_common(15))

        fig, ax = plt.subplots(figsize=(10, 6))
        words = list(top_words.keys())
        counts = list(top_words.values())
        bars = ax.barh(range(len(words)), counts)
        ax.set_title('Top 15 Words in Paper Titles')
        ax.set_xlabel('Frequency')
        ax.set_yticks(range(len(words)))
        ax.set_yticklabels(words)
        ax.invert_yaxis()

        # Add value labels
        for i, bar in enumerate(bars):
            width = bar.get_width()
            ax.text(width + width*0.01, bar.get_y() + bar.get_height()/2,
                   f'{int(width)}', ha='left', va='center')

        st.pyplot(fig)

    st.markdown("---")

    # Data sample
    st.header(" Data Sample")
    st.subheader("Sample of Papers")

    # Select columns to display
    display_cols = ['title', 'journal', 'publish_year']
    if 'abstract' in df_display.columns:
        display_cols.append('abstract')

    available_cols = [col for col in display_cols if col in df_display.columns]

    if available_cols:
        sample_df = df_display[available_cols].head(20)
        st.dataframe(sample_df, use_container_width=True)
    else:
        st.write("No suitable columns found for display")

    # Footer
    st.markdown("---")
    st.markdown("**Data Source:** CORD-19 Dataset")
    st.markdown("**Built with:** Streamlit, Pandas, Matplotlib")

if __name__ == "__main__":
    main()
