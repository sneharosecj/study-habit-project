import streamlit as st
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
import plotly.express as px

st.set_page_config(layout="wide", page_title="Student Clustering Dashboard")

st.title("Student Performance — Clustering Dashboard")

# Default features (same as notebook)
DEFAULT_FEATURES = [
    "Attendance (%)",
    "Midterm_Score",
    "Final_Score",
    "Assignments_Avg",
    "Quizzes_Avg",
    "Participation_Score",
    "Projects_Score",
    "Total_Score",
    "Study_Hours_per_Week",
]

# Sidebar controls
st.sidebar.header("Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV (optional)", type=["csv"]) 

n_clusters = st.sidebar.slider("Number of clusters", 2, 10, 4)
eps = st.sidebar.slider("DBSCAN eps", 0.1, 5.0, 0.5, step=0.1)
min_samples = st.sidebar.slider("DBSCAN min samples", 2, 20, 5)
features = st.sidebar.multiselect("Select numerical features", DEFAULT_FEATURES, default=DEFAULT_FEATURES)
run_button = st.sidebar.button("Run clustering")

# Load data
@st.cache_data
def load_data(path=None, uploaded=None):
    if uploaded is not None:
        return pd.read_csv(uploaded)
    if path is not None:
        return pd.read_csv(path)
    return None

df = load_data(path="students_with_clusters.csv", uploaded=uploaded_file)

if df is None:
    st.info("No dataset available. Upload a CSV or place `Students Performance Dataset.csv` in the app folder.")
    st.stop()

st.subheader("Data preview")
st.dataframe(df.head())

# placeholder for post-clustering preview, will be filled when clusters computed

# Validate features
missing = [f for f in features if f not in df.columns]
if missing:
    st.error(f"These features are missing from the dataset: {missing}")
    st.stop()

if run_button:
    X = df[features].copy()
    # Drop rows with NaNs in selected features for clustering
    before_rows = X.shape[0]
    X = X.dropna()
    after_rows = X.shape[0]
    if after_rows < before_rows:
        st.warning(f"Dropped {before_rows - after_rows} rows with missing values in selected features.")

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # compute several clustering methods
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels_km = kmeans.fit_predict(X_scaled)
    sil_km = silhouette_score(X_scaled, labels_km)
    df["Cluster_KMeans"] = labels_km

    agg = AgglomerativeClustering(n_clusters=n_clusters)
    labels_ag = agg.fit_predict(X_scaled)
    sil_ag = silhouette_score(X_scaled, labels_ag)
    df["Cluster_Agglomerative"] = labels_ag

    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels_db = dbscan.fit_predict(X_scaled)
    df["Cluster_DBSCAN"] = labels_db
    sil_db = None
    if len(set(labels_db)) > 1 and not set(labels_db) == {-1}:
        sil_db = silhouette_score(X_scaled[labels_db != -1], labels_db[labels_db != -1])

    # PCA transformation for visualize
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)
    df["PCA1"] = X_pca[:, 0]
    df["PCA2"] = X_pca[:, 1]

    # update preview now that we have cluster labels
    st.subheader("Labeled data preview")
    # show some identifying columns plus selected features, behavioral columns and cluster labels
    id_cols = [c for c in ["Student_ID","First_Name","Last_Name"] if c in df.columns]
    beh_cols = ["Stress_Level (1-10)", "Sleep_Hours_per_Night", "Attendance (%)"]
    beh_in_df = [c for c in beh_cols if c in df.columns and c not in features]
    display_cols = id_cols + features + beh_in_df + ["Cluster_KMeans","Cluster_Agglomerative","Cluster_DBSCAN"]
    st.dataframe(df[display_cols].head(50))

    # allow the user to inspect an individual student
    st.subheader("Student-level analysis")
    if "Student_ID" in df.columns:
        student_options = df["Student_ID"].dropna().unique().tolist()
        selected_student = st.selectbox("Select a student", student_options)
        if selected_student:
            student_row = df.loc[df["Student_ID"] == selected_student].iloc[0]
            st.write("### Basic information")
            st.write(student_row[id_cols].to_frame().T)
            # show cluster membership
            st.write("### Cluster membership")
            for method in ["Cluster_KMeans","Cluster_Agglomerative","Cluster_DBSCAN"]:
                if method in student_row.index:
                    st.write(f"{method}: {student_row[method]}")
            # chart of student's feature values
            st.write("### Feature values chart")
            student_values = student_row[features]
            fig = px.bar(x=features, y=student_values, labels={"x":"Feature","y":"Value"},
                         title=f"Feature profile for {selected_student}")
            st.plotly_chart(fig, use_container_width=True)
            # behavior analysis: compare to cluster means for kmeans
            if "Cluster_KMeans" in student_row.index:
                cl = student_row["Cluster_KMeans"]
                st.write("### Behavior analysis (relative to cluster average)")
                profile = df.groupby("Cluster_KMeans")[features].mean()
                if cl in profile.index:
                    cluster_mean = profile.loc[cl]
                    diff = student_values - cluster_mean
                    fig2 = px.bar(x=features, y=diff,
                                  labels={"x":"Feature","y":"Difference"},
                                  title=f"Difference from KMeans cluster {cl} average")
                    st.plotly_chart(fig2, use_container_width=True)
                    # textual commentary
                    st.write("Observations:")
                    for feat in features:
                        if diff[feat] > 0:
                            st.write(f"- Higher than cluster average in {feat}.")
                        elif diff[feat] < 0:
                            st.write(f"- Lower than cluster average in {feat}.")
                        else:
                            st.write(f"- At cluster average for {feat}.")
            # additional behavioral columns if available
            beh_cols = ["Stress_Level (1-10)", "Sleep_Hours_per_Night", "Attendance (%)"]
            cols_available = [c for c in beh_cols if c in df.columns]
            if cols_available:
                st.write("### Other behavioral indicators")
                st.write(student_row[cols_available].to_frame().T)
                # compare these to cluster mean as well
                if "Cluster_KMeans" in student_row.index:
                    profile_beh = df.groupby("Cluster_KMeans")[cols_available].mean()
                    if cl in profile_beh.index:
                        beh_mean = profile_beh.loc[cl]
                        beh_diff = student_row[cols_available] - beh_mean
                        fig3 = px.bar(x=cols_available, y=beh_diff,
                                      labels={"x":"Indicator","y":"Difference"},
                                      title="Behavior indicators diff from cluster mean")
                        st.plotly_chart(fig3, use_container_width=True)
                        st.write("Behavior observations:")
                        for bc in cols_available:
                            if beh_diff[bc] > 0:
                                st.write(f"- Higher than cluster average in {bc}.")
                            elif beh_diff[bc] < 0:
                                st.write(f"- Lower than cluster average in {bc}.")
                            else:
                                st.write(f"- At cluster average for {bc}.")

    else:
        st.warning("Dataset does not contain a Student_ID column, individual analysis unavailable.")

    # show silhouette metrics
    st.subheader("Silhouette scores")
    col1, col2, col3 = st.columns(3)
    col1.metric("KMeans", f"{sil_km:.3f}")
    col2.metric("Agglomerative", f"{sil_ag:.3f}")
    col3.metric("DBSCAN", f"{sil_db:.3f}" if sil_db is not None else "n/a")

    st.markdown("---")

    # scatter plots side by side
    methods = ["Cluster_KMeans", "Cluster_Agglomerative", "Cluster_DBSCAN"]
    cols = st.columns(3)
    for c, method in zip(cols, methods):
        with c:
            st.subheader(f"PCA scatter ({method})")
            fig = px.scatter(df, x="PCA1", y="PCA2", color=df[method].astype(str),
                             color_discrete_sequence=px.colors.qualitative.Set2,
                             labels={"color": method},
                             hover_data=features)
            st.plotly_chart(fig, use_container_width=True)

    st.markdown("---")

    st.subheader("Cluster distributions")
    for method in methods:
        dist = df[method].value_counts().sort_index()
        st.write(f"**{method} distribution**")
        st.bar_chart(dist)

    st.markdown("---")

    st.subheader("Cluster profiles (mean features)")
    for method in methods:
        st.write(f"**{method}**")
        profile = df.groupby(method)[features].mean().round(3)
        st.dataframe(profile)

    st.markdown("---")

    # Download and save
    df_out = df.copy()
    csv = df_out.to_csv(index=False)
    st.download_button("Download CSV with clusters", data=csv, file_name="students_with_clusters.csv", mime='text/csv')

    if st.button("Save CSV on server as students_with_clusters.csv"):
        try:
            df_out.to_csv("students_with_clusters.csv", index=False)
            st.success("students_with_clusters.csv saved successfully.")
        except Exception as e:
            st.error(f"Failed to save file: {e}")

    st.info("Note: Only rows with complete values in the selected features receive a cluster label; other rows are left blank.")
else:
    st.info("Adjust settings in the sidebar and click 'Run clustering' to compute clusters.")
