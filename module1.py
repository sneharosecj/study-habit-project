import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Page config
st.set_page_config(page_title="Student Behavior Dashboard", layout="wide")

st.title("📊 Student Behavior Analysis Dashboard")

# ------------------ Load Dataset ------------------
df = pd.read_csv(r"D:\Desktop\app\Students Performance Dataset.csv")

# =========================================================
# 🔹 DATA PREPROCESSING & EDA SECTION (TOP OF DASHBOARD)
# =========================================================

st.header("🔎 Data Preprocessing & Exploratory Data Analysis")

# Dataset Shape
st.subheader("Dataset Overview")
st.write("Shape of Dataset:", df.shape)

# Show first 5 rows
st.subheader("First 5 Rows")
st.dataframe(df.head())

# Missing Values
st.subheader("Missing Values")
missing = df.isnull().sum()
st.write(missing)

# Fill Missing Values (if any)
df.fillna(df.mean(numeric_only=True), inplace=True)

# Summary Statistics
st.subheader("Statistical Summary")
st.write(df.describe())

# Correlation Matrix Table
st.subheader("Correlation Matrix")
st.dataframe(df.corr(numeric_only=True))

st.markdown("---")

# =========================================================
# 🔹 VISUALIZATIONS
# =========================================================

# ------------------ Scatter Plot ------------------
st.subheader("Study Hours per Week vs Quiz Average")

scatter_fig = px.scatter(
    df,
    x="Study_Hours_per_Week",
    y="Quizzes_Avg",
    title="Study Hours per Week vs Quiz Average",
    trendline="ols"
)

st.plotly_chart(scatter_fig, use_container_width=True)

# ------------------ Correlation Heatmap ------------------
st.subheader("Correlation Heatmap")

corr = df.corr(numeric_only=True)

heatmap_fig = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns,
        colorscale="Blues"
    )
)

heatmap_fig.update_layout(title="Correlation Heatmap")

st.plotly_chart(heatmap_fig, use_container_width=True)

# ------------------ Bar Chart ------------------
st.subheader("Grade vs Total Score")

bar_fig = px.bar(
    df,
    x="Grade",
    y="Total_Score",
    color="Grade",
    title="Grade vs Total Score"
)

st.plotly_chart(bar_fig, use_container_width=True)

# ------------------ Donut Chart ------------------
st.subheader("Grade Distribution")

donut_fig = px.pie(
    df,
    names="Grade",
    title="Grade Distribution",
    hole=0.5
)

st.plotly_chart(donut_fig, use_container_width=True)

# =========================================================
# 🔹 ADDITIONAL CHARTS
# =========================================================

# Histogram
st.subheader("Distribution of Total Scores")

hist_fig = px.histogram(
    df,
    x="Total_Score",
    nbins=20,
    title="Total Score Distribution"
)

st.plotly_chart(hist_fig, use_container_width=True)

# Box Plot
st.subheader("Study Hours Distribution by Grade")

box_fig = px.box(
    df,
    x="Grade",
    y="Study_Hours_per_Week",
    title="Study Hours per Week by Grade"
)

st.plotly_chart(box_fig, use_container_width=True)

# Line Chart
st.subheader("Study Hours vs Total Score Trend")

line_fig = px.line(
    df.sort_values("Study_Hours_per_Week"),
    x="Study_Hours_per_Week",
    y="Total_Score",
    title="Trend of Study Hours vs Total Score"
)

st.plotly_chart(line_fig, use_container_width=True)

# Scatter Matrix (Pair Plot Style)
st.subheader("Feature Relationships (Scatter Matrix)")

scatter_matrix = px.scatter_matrix(
    df,
    dimensions=["Study_Hours_per_Week", "Quizzes_Avg", "Total_Score"],
    color="Grade",
    title="Scatter Matrix of Key Features"
)

st.plotly_chart(scatter_matrix, use_container_width=True)