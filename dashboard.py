import streamlit as st
import pandas as pd
import plotly.express as px
import os
from datetime import datetime

st.set_page_config(page_title="Web Scraper Dashboard", layout="wide", page_icon="📊")

st.title("📊 Ethical Web Scraper + Interactive Dashboard")
st.markdown("**Project 2 Portfolio** — Scrapes public data and visualizes it instantly.")

# Sidebar
st.sidebar.header("Controls")
data_files = [f for f in os.listdir("data") if f.endswith('.csv')]
selected_file = st.sidebar.selectbox("Choose scraped dataset", data_files)

if selected_file:
    df = pd.read_csv(os.path.join("data", selected_file))

    st.subheader(f"Dataset: {selected_file} ({len(df)} records)")

    # Filters
    col1, col2 = st.columns(2)
    with col1:
        authors = st.multiselect("Filter by Author", options=df['Author'].unique())
    with col2:
        search = st.text_input("Search in Quote")

    # Apply filters
    filtered_df = df.copy()
    if authors:
        filtered_df = filtered_df[filtered_df['Author'].isin(authors)]
    if search:
        filtered_df = filtered_df[filtered_df['Quote'].str.contains(search, case=False)]

    # Display data
    st.dataframe(filtered_df, use_container_width=True)

    # Visualizations
    col1, col2 = st.columns(2)

    with col1:
        st.plotly_chart(
            px.bar(filtered_df['Author'].value_counts().head(10),
                   title="Top Authors by Number of Quotes",
                   labels={'value': 'Count', 'index': 'Author'}),
            use_container_width=True
        )

    with col2:
        # Simple tag analysis (split and count)
        all_tags = []
        for tags in filtered_df['Tags'].dropna():
            all_tags.extend([t.strip() for t in tags.split(',') if t.strip()])
        tag_df = pd.Series(all_tags).value_counts().head(10)
        st.plotly_chart(
            px.pie(values=tag_df.values, names=tag_df.index,
                   title="Top Tags Distribution"),
            use_container_width=True
        )

    # Export buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        csv = filtered_df.to_csv(index=False).encode()
        st.download_button("📥 Download CSV", csv, f"filtered_data_{datetime.now().strftime('%Y%m%d')}.csv", "text/csv")
    with col2:
        excel_buffer = pd.ExcelWriter("filtered_data.xlsx", engine='openpyxl')
        filtered_df.to_excel(excel_buffer, index=False)
        excel_buffer.close()
        with open("filtered_data.xlsx", "rb") as f:
            st.download_button("📥 Download Excel", f.read(), "filtered_data.xlsx",
                               "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    st.success("Dashboard ready! This can be deployed live for clients.")

else:
    st.info("Run scraper.py first to generate data files.")