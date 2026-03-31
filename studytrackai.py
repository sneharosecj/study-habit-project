import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, DBSCAN, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from datetime import datetime, timedelta
import os
import warnings
warnings.filterwarnings('ignore')

# ========== PAGE CONFIGURATION ==========
st.set_page_config(
    page_title="Recommending Study Habits Based on Student Behavior",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("📊 Recommending Study Habits Based on Student Behavior")
st.markdown("### AI-Based Student Behavior Analysis & Personalized Study Recommendation System")
# ========== CUSTOM STYLING ==========
st.markdown("""
<style>

/* --------- GLOBAL LIGHT THEME --------- */
.stApp {
    background: #f5f7fb;
    font-family: 'Segoe UI', sans-serif;
}

/* Remove dark padding */
.main {
    padding-top: 1rem;
}

/* --------- HEADER --------- */
h1, h2, h3 {
    color: #1f2937;
}

/* --------- METRIC CARDS --------- */
.metric-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
    transition: 0.3s;
}

.metric-card:hover {
    transform: translateY(-3px);
}

/* --------- RECOMMENDATION CARD --------- */
.recommendation-card {
    background: white;
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    border-left: 6px solid #4f46e5;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}

/* --------- TOOL CARD --------- */
.tool-card {
    background: white;
    border-radius: 12px;
    padding: 15px;
    border: 1px solid #e5e7eb;
    text-align: center;
    transition: 0.2s;
}

.tool-card:hover {
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    transform: translateY(-2px);
}

/* --------- SIDEBAR --------- */
[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

/* --------- BUTTONS --------- */
.stButton>button {
    background: #4f46e5;
    color: white;
    border-radius: 8px;
    border: none;
    padding: 8px 16px;
    font-weight: 500;
}

.stButton>button:hover {
    background: #4338ca;
}

/* --------- TABS --------- */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
}

.stTabs [data-baseweb="tab"] {
    background: #ffffff;
    border-radius: 8px;
    padding: 10px 18px;
    border: 1px solid #e5e7eb;
}

.stTabs [aria-selected="true"] {
    background: #eef2ff;
    border: 1px solid #4f46e5;
}

/* --------- DATAFRAME --------- */
.stDataFrame {
    background: white;
    border-radius: 10px;
    border: 1px solid #e5e7eb;
}

/* --------- INPUT BOX --------- */
input, textarea {
    border-radius: 8px !important;
}

/* --------- FOOTER --------- */
.footer {
    text-align: center;
    color: #6b7280;
    font-size: 13px;
}

</style>
""", unsafe_allow_html=True)

# ========== DATA LOADING & CACHING ==========
@st.cache_data
def load_student_data():
    try:
        if os.path.exists("Students Performance Dataset.csv"):
            df = pd.read_csv("Students Performance Dataset.csv")
        else:
            df = pd.read_csv(r"D:\Desktop\app\Students Performance Dataset.csv")
        return df
    except:
        st.error("Could not load Students Performance Dataset.csv")
        return None

@st.cache_data
def load_clustered_data():
    try:
        df = pd.read_csv("students_with_clusters.csv")
        return df
    except:
        return None

@st.cache_data
def load_study_logs():
    if os.path.exists("study_logs.csv"):
        return pd.read_csv("study_logs.csv")
    else:
        return pd.DataFrame(columns=["date", "study_duration", "study_time", "subject", "distraction_level", "quiz_score", "predicted_cluster"])

def save_study_log(log_data):
    logs_df = load_study_logs()
    logs_df = pd.concat([logs_df, pd.DataFrame([log_data])], ignore_index=True)
    logs_df.to_csv("study_logs.csv", index=False)
    st.cache_data.clear()

# ========== HELPER FUNCTIONS ==========
def engineer_features(df):
    """Create numeric features from raw data for better clustering"""
    df_eng = df.copy()
    
    # Encode distraction_level (categorical to numeric)
    if 'distraction_level' in df_eng.columns:
        distraction_map = {'low': 1, 'medium': 2, 'high': 3}
        df_eng['distraction_level_numeric'] = df_eng['distraction_level'].map(distraction_map)
    
    # Encode subject (categorical to numeric)
    if 'subject' in df_eng.columns:
        subject_unique = df_eng['subject'].unique()
        subject_map = {subj: i for i, subj in enumerate(subject_unique)}
        df_eng['subject_encoded'] = df_eng['subject'].map(subject_map)
    
    # Extract hour from study_time (if format is HH:MM)
    if 'study_time' in df_eng.columns:
        try:
            df_eng['study_hour'] = pd.to_datetime(df_eng['study_time'], format='%H:%M', errors='coerce').dt.hour
        except:
            pass
    
    return df_eng

def prepare_clustering_data(df, selected_features):
    """Prepare data for clustering"""
    X = df[selected_features].copy()
    before_rows = X.shape[0]
    X = X.dropna()
    after_rows = X.shape[0]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    return X_scaled, scaler, before_rows - after_rows

def run_clustering(df, X_scaled, n_clusters, eps, min_samples, selected_features):
    """Run all clustering algorithms"""
    results = {}
    
    # KMeans
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels_km = kmeans.fit_predict(X_scaled)
    results['KMeans'] = {'labels': labels_km, 'silhouette': silhouette_score(X_scaled, labels_km)}
    
    # Agglomerative
    agg = AgglomerativeClustering(n_clusters=n_clusters)
    labels_ag = agg.fit_predict(X_scaled)
    results['Agglomerative'] = {'labels': labels_ag, 'silhouette': silhouette_score(X_scaled, labels_ag)}
    
    # DBSCAN
    dbscan = DBSCAN(eps=eps, min_samples=min_samples)
    labels_db = dbscan.fit_predict(X_scaled)
    sil_db = None
    if len(set(labels_db)) > 1 and not set(labels_db) == {-1}:
        mask = labels_db != -1
        sil_db = silhouette_score(X_scaled[mask], labels_db[mask])
    results['DBSCAN'] = {'labels': labels_db, 'silhouette': sil_db}
    
    return results

# ========== CLUSTER BEHAVIOR MAPPINGS ==========
CLUSTER_BEHAVIOR = {
    0: "High Focus Learners",
    1: "Low Focus Learners",
    2: "Distracted Learners",
    3: "Visual Learners"
}

CLUSTER_STUDY_PARAMS = {
    0: {
        "time_slots": ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM"],
        "duration": 25,
        "breaks": "5 min every 25 min",
        "effectiveness": 85,
        "method": "Focused deep work sessions"
    },
    1: {
        "time_slots": ["10:00 AM - 12:00 PM", "4:00 PM - 6:00 PM"],
        "duration": 20,
        "breaks": "10 min every 20 min",
        "effectiveness": 70,
        "method": "Short, frequent study sessions"
    },
    2: {
        "time_slots": ["7:00 AM - 9:00 AM", "7:00 PM - 9:00 PM"],
        "duration": 15,
        "breaks": "15 min every 15 min",
        "effectiveness": 60,
        "method": "Distraction-free environment setup"
    },
    3: {
        "time_slots": ["9:00 AM - 11:00 AM", "3:00 PM - 5:00 PM"],
        "duration": 30,
        "breaks": "5 min every 30 min",
        "effectiveness": 80,
        "method": "Visual aids and multimedia learning"
    }
}

BEHAVIOR_TOOLS = {
    "High Focus Learners": ["Mock test platforms", "Advanced study timers"],
    "Low Focus Learners": ["Pomodoro Timer", "Focus music apps"],
    "Distracted Learners": ["Site Blocker", "Noise-cancelling headphones"],
    "Visual Learners": ["Digital Notes", "Mind mapping tools"]
}

# ========== MAIN APPLICATION ==========
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user = None

st.title("📊 Integrated Student Analytics & Study Dashboard")
st.markdown("---")

# ========== STUDENT LOGIN ==========
if not st.session_state.logged_in:
    st.subheader("🔐 Student Login")

    login_df = load_clustered_data()
    if login_df is None:
        login_df = load_student_data()

    if login_df is None:
        st.warning("No student data found for login. Please add `students_with_clusters.csv` or `Students Performance Dataset.csv`.")
        st.stop()

    if 'Student_ID' not in login_df.columns or 'Email' not in login_df.columns:
        st.warning("Student login requires 'Student_ID' and 'Email' columns in the dataset.")
        st.stop()

    selected_id = st.selectbox("Select Student ID", login_df['Student_ID'].astype(str).tolist())
    email_input = st.text_input("Email", value="")

    if st.button("Login"):
        matched = login_df[(login_df['Student_ID'].astype(str) == selected_id) &
                           (login_df['Email'].astype(str).str.lower() == email_input.strip().lower())]
        if not matched.empty:
            st.session_state.logged_in = True
            st.session_state.user = matched.iloc[0].to_dict()
            st.success(f"Logged in as {st.session_state.user.get('First_Name', '')} {st.session_state.user.get('Last_Name', '')} ({selected_id})")
        else:
            st.error("Invalid Student ID / Email combination. Make sure both values are correct.")
    st.stop()

st.sidebar.success(f"Logged in as {st.session_state.user.get('First_Name', '')} {st.session_state.user.get('Last_Name', '')}")
if st.sidebar.button("Logout"):
    st.session_state.logged_in = False
    st.session_state.user = None

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Data Analysis",
    "🔍 Student Clustering",
    "📋 Personalized Study Plans",
    "📝 Study Tracker",
    "📊 Progress Analytics"
])

# ========== TAB 1: DATA ANALYSIS ==========
with tab1:
    st.header("🔎 Data Preprocessing & Exploratory Data Analysis")
    
    df = load_study_logs()
    
    if df is not None:
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Students", df.shape[0])
        with col2:
            st.metric("Total Features", df.shape[1])
        with col3:
            st.metric("Missing Values", df.isnull().sum().sum())
        with col4:
            st.metric("Numeric Features", df.select_dtypes(include=[np.number]).shape[1])
        
        st.markdown("---")
        
        # Dataset Overview
        col_left, col_right = st.columns(2)
        
        with col_left:
            st.subheader("First 5 Rows")
            st.dataframe(df.head(), use_container_width=True)
        
        with col_right:
            st.subheader("Dataset Info")
            st.write(f"**Shape:** {df.shape}")
            st.write(f"**Missing Values:**")
            missing = df.isnull().sum()
            if missing.sum() > 0:
                st.dataframe(missing[missing > 0])
            else:
                st.write("No missing values!")
        
        st.markdown("---")
        
        # Statistical Summary
        st.subheader("Statistical Summary")
        st.dataframe(df.describe().T, use_container_width=True)
        
        st.markdown("---")
        
        # Visualizations
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Study Duration vs Quiz Score")
            scatter_fig = px.scatter(
                df,
                x="study_duration",
                y="quiz_score",
                color="subject",
                title="Study Duration vs Quiz Score",
                trendline="ols",
                hover_data=["distraction_level"]
            )
            st.plotly_chart(scatter_fig, use_container_width=True)
        
        with col2:
            st.subheader("Subject Distribution")
            subject_dist = df["subject"].value_counts()
            donut_fig = px.pie(
                values=subject_dist.values,
                names=subject_dist.index,
                title="Subject Distribution",
                hole=0.5
            )
            st.plotly_chart(donut_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
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
            heatmap_fig.update_layout(height=600)
            st.plotly_chart(heatmap_fig, use_container_width=True)
        
        with col2:
            st.subheader("Quiz Score Distribution")
            hist_fig = px.histogram(
                df,
                x="quiz_score",
                nbins=20,
                title="Quiz Score Distribution",
                color_discrete_sequence=["#636EFA"]
            )
            st.plotly_chart(hist_fig, use_container_width=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Cluster vs Quiz Score")
            bar_fig = px.box(
                df,
                x="predicted_cluster",
                y="quiz_score",
                color="predicted_cluster",
                title="Quiz Score by Cluster"
            )
            st.plotly_chart(bar_fig, use_container_width=True)
        
        with col2:
            st.subheader("Study Duration by Subject")
            box_fig = px.box(
                df,
                x="subject",
                y="study_duration",
                color="subject",
                title="Study Duration by Subject"
            )
            st.plotly_chart(box_fig, use_container_width=True)

# ========== TAB 2: STUDENT CLUSTERING ==========
with tab2:
    st.header("🔍 Student Performance Clustering Analysis")
    
    # Prefer fully featured dataset first
    df_clustered_data = load_clustered_data()
    df_raw = df_clustered_data if df_clustered_data is not None else load_student_data()

    if df_raw is None:
        st.error("No student dataset available for clustering. Upload/prepare `students_with_clusters.csv` or `Students Performance Dataset.csv`.")
    else:
        # If module2-style dataset is present, use its full numeric feature set
        module2_features = [
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

        if all(col in df_raw.columns for col in module2_features):
            df_clustered = df_raw.copy()
            DEFAULT_FEATURES = module2_features.copy()
        else:
            # fallback to study log data and engineered features
            df_clustered = engineer_features(df_raw)
            DEFAULT_FEATURES = [
                "study_duration",
                "distraction_level_numeric",
                "quiz_score",
                "subject_encoded",
            ]
            if 'study_hour' in df_clustered.columns and df_clustered['study_hour'].notna().any():
                DEFAULT_FEATURES.append("study_hour")

        # Sidebar controls
        st.sidebar.header("Clustering Controls")

        n_clusters = st.sidebar.slider("Number of clusters", 2, 10, 4)
        eps = st.sidebar.slider("DBSCAN eps", 0.1, 5.0, 0.5, step=0.1)
        min_samples = st.sidebar.slider("DBSCAN min samples", 2, 20, 5)

        available_features = [f for f in DEFAULT_FEATURES if f in df_clustered.columns]
        features = st.sidebar.multiselect("Select features", available_features, default=available_features)

        run_button = st.sidebar.button("Run Clustering Analysis")

        if run_button and features:
            # Prepare data
            X_scaled, scaler, dropped_rows = prepare_clustering_data(df_clustered, features)

            if dropped_rows > 0:
                st.warning(f"Dropped {dropped_rows} rows with missing values")

            # Run clustering
            results = run_clustering(df_clustered, X_scaled, n_clusters, eps, min_samples, features)
            
            # Display metrics
            st.markdown("### Clustering Quality Metrics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("KMeans Silhouette", f"{results['KMeans']['silhouette']:.3f}")
            with col2:
                st.metric("Agglomerative Silhouette", f"{results['Agglomerative']['silhouette']:.3f}")
            with col3:
                sil_db = results['DBSCAN']['silhouette']
                st.metric("DBSCAN Silhouette", f"{sil_db:.3f}" if sil_db else "N/A")
            
            st.markdown("---")
            
            # PCA Visualization
            pca = PCA(n_components=2)
            X_pca = pca.fit_transform(X_scaled)
            
            col1, col2, col3 = st.columns(3)
            
            methods = ['KMeans', 'Agglomerative', 'DBSCAN']
            fig_list = []
            
            for i, method in enumerate(methods):
                labels = results[method]['labels'].astype(str)
                fig = px.scatter(
                    x=X_pca[:, 0],
                    y=X_pca[:, 1],
                    color=labels,
                    title=f"PCA Visualization - {method}",
                    labels={"color": "Cluster"},
                    hover_data={"x": X_pca[:, 0], "y": X_pca[:, 1]}
                )
                fig.update_layout(height=400)
                fig_list.append(fig)
            
            with col1:
                st.plotly_chart(fig_list[0], use_container_width=True)
            with col2:
                st.plotly_chart(fig_list[1], use_container_width=True)
            with col3:
                st.plotly_chart(fig_list[2], use_container_width=True)
            
            st.markdown("---")
            
            # Store clusters in dataframe
            df_clustered = df_clustered.copy()
            df_clustered['Cluster_KMeans'] = results['KMeans']['labels']
            df_clustered['Cluster_Agglomerative'] = results['Agglomerative']['labels']
            df_clustered['Cluster_DBSCAN'] = results['DBSCAN']['labels']
            
            # Save clustered data
            if st.button("Save Clustered Data"):
                df_clustered.to_csv("students_with_clusters.csv", index=False)
                st.success("✅ Clustered data saved to students_with_clusters.csv")
            
            # Cluster Profiles
            st.subheader("Cluster Profiles (Mean Features)")
            
            profile_tabs = st.tabs(["KMeans", "Agglomerative", "DBSCAN"])
            
            for tab_idx, method in enumerate(['Cluster_KMeans', 'Cluster_Agglomerative', 'Cluster_DBSCAN']):
                with profile_tabs[tab_idx]:
                    if method in df_clustered.columns:
                        profile = df_clustered.groupby(method)[features].mean().round(3)
                        st.dataframe(profile, use_container_width=True)

# ========== TAB 3: PERSONALIZED STUDY PLANS ==========
with tab3:
    st.header("📋 Personalized Study Plans")
    
    clustered_df = load_clustered_data()
    
    if clustered_df is not None:
        # Student selection
        if "Student_ID" in clustered_df.columns:
            student_options = [f"{row['Student_ID']} - {row.get('First_Name', 'Unknown')} {row.get('Last_Name', '')}" 
                              for _, row in clustered_df.iterrows()]
            selected_student = st.selectbox("Select Student", student_options)
            
            if selected_student:
                student_id = selected_student.split(" - ")[0]
                student_data = clustered_df[clustered_df["Student_ID"] == student_id].iloc[0]
                cluster = int(student_data.get("Cluster_KMeans", 0))
                behavior = CLUSTER_BEHAVIOR.get(cluster, "Unknown")
                params = CLUSTER_STUDY_PARAMS.get(cluster, CLUSTER_STUDY_PARAMS[0])
                tools = BEHAVIOR_TOOLS.get(behavior, ["General tools"])
                
                # Student Profile
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown("### Student Profile")
                    st.write(f"**ID:** {student_id}")
                    st.write(f"**Cluster:** {cluster}")
                    st.write(f"**Behavior Type:** {behavior}")
                
                with col2:
                    st.markdown("### Academic Performance")
                    st.write(f"**Total Score:** {student_data.get('Total_Score', 0):.2f}")
                    st.write(f"**Grade:** {student_data.get('Grade', 'N/A')}")
                    st.write(f"**Attendance:** {student_data.get('Attendance (%)', 0):.1f}%")
                
                with col3:
                    st.markdown("### Well-being Metrics")
                    st.write(f"**Stress Level:** {student_data.get('Stress_Level (1-10)', 0)}/10")
                    st.write(f"**Sleep Hours:** {student_data.get('Sleep_Hours_per_Night', 0):.1f}")
                    st.write(f"**Study Hours/Week:** {student_data.get('Study_Hours_per_Week', 0):.1f}")
                
                st.markdown("---")
                
                # Study Plan
                st.markdown("### 📚 Recommended Study Plan")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"""
                    **Study Method:** {params['method']}
                    
                    **Optimal Study Time Slots:**
                    """)
                    for slot in params['time_slots']:
                        st.write(f"• {slot}")
                    
                    st.write(f"**Session Duration:** {params['duration']} minutes")
                    st.write(f"**Break Schedule:** {params['breaks']}")
                
                with col2:
                    st.markdown(f"""
                    ### Effectiveness Score
                    
                    **{params['effectiveness']}%**
                    
                    Improvement potential
                    """)
                
                st.markdown("---")
                
                # Performance Breakdown
                st.subheader("Performance Breakdown by Component")
                
                components = ["Midterm_Score", "Final_Score", "Assignments_Avg", "Quizzes_Avg", "Participation_Score", "Projects_Score"]
                component_labels = ["Midterm", "Final", "Assignments", "Quizzes", "Participation", "Projects"]
                component_values = [student_data.get(comp, 0) for comp in components]
                
                fig_perf = px.bar(
                    x=component_labels,
                    y=component_values,
                    title="Performance Across Components",
                    color=component_values,
                    color_continuous_scale="Viridis"
                )
                st.plotly_chart(fig_perf, use_container_width=True)
                
                st.markdown("---")
                
                # Weekly Schedule
                st.subheader("Weekly Study Schedule")
                
                daily_hours = {
                    0: [2, 2, 1.5, 2, 2, 1, 1],
                    1: [1, 1, 1, 1, 1, 0.5, 0.5],
                    2: [1.5, 1, 1, 1.5, 1, 2, 1],
                    3: [2, 1.5, 2, 1.5, 2, 1, 1]
                }.get(cluster, [1.5]*7)
                
                days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
                
                fig_weekly = px.bar(
                    x=days,
                    y=daily_hours,
                    title="Recommended Study Hours per Day",
                    labels={"y": "Hours", "x": "Day"}
                )
                st.plotly_chart(fig_weekly, use_container_width=True)
                
                st.markdown("---")
                
                # Recommended Tools
                st.subheader("🛠️ Recommended Study Tools")
                
                cols = st.columns(len(tools))
                for i, tool in enumerate(tools):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="tool-card">
                            <h4>🎯 {tool}</h4>
                            <p>Recommended for {behavior.lower()}</p>
                        </div>
                        """, unsafe_allow_html=True)

# ========== TAB 4: STUDY TRACKER ==========
with tab4:
    st.header("📝 Study Behavior Tracker")
    
    clustered_df = load_clustered_data()
    
    if clustered_df is not None:
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("Log Your Study Session")
            
            with st.form("study_form"):
                date = st.date_input("Date", datetime.now().date())
                study_duration = st.slider("Study Duration (minutes)", 15, 300, 60)
                study_time = st.selectbox("Study Time", ["Morning", "Afternoon", "Evening"])
                subject = st.text_input("Subject Studied", "")
                distraction_level = st.selectbox("Distraction Level", ["None", "Low", "Medium", "High"])
                quiz_score = st.slider("Recent Quiz Score (%)", 0, 100, 75)
                
                submitted = st.form_submit_button("Save & Get Recommendations")
                
                if submitted:
                    # Create log entry
                    log_data = {
                        "date": date,
                        "study_duration": study_duration,
                        "study_time": study_time,
                        "subject": subject,
                        "distraction_level": distraction_level,
                        "quiz_score": quiz_score,
                        "predicted_cluster": 0
                    }
                    
                    save_study_log(log_data)
                    st.success("✅ Study session logged successfully!")
                    
                    # Get cluster-based recommendations
                    if quiz_score >= 80:
                        cluster = 0  # High focus
                    elif quiz_score >= 60:
                        cluster = 3  # Visual
                    elif quiz_score >= 40:
                        cluster = 1  # Low focus
                    else:
                        cluster = 2  # Distracted
                    
                    behavior = CLUSTER_BEHAVIOR.get(cluster, "Unknown")
                    params = CLUSTER_STUDY_PARAMS.get(cluster, CLUSTER_STUDY_PARAMS[0])
                    
                    st.markdown("---")
                    st.subheader("📌 Your Personalized Recommendations")
                    
                    st.markdown(f"""
                    <div class="recommendation-card">
                        <h3>Study Profile: {behavior}</h3>
                        <p><strong>Optimal Study Times:</strong> {', '.join(params['time_slots'])}</p>
                        <p><strong>Recommended Duration:</strong> {params['duration']} minutes per session</p>
                        <p><strong>Break Schedule:</strong> {params['breaks']}</p>
                        <p><strong>Study Method:</strong> {params['method']}</p>
                        <p><strong>Expected Effectiveness:</strong> {params['effectiveness']}% improvement</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        with col2:
            st.subheader("Recent Study Sessions")
            logs_df = load_study_logs()
            
            if not logs_df.empty:
                # Convert date to datetime
                logs_df['date'] = pd.to_datetime(logs_df['date'])
                recent_logs = logs_df.sort_values('date', ascending=False).head(10)
                st.dataframe(recent_logs, use_container_width=True)
                
                # Summary stats
                st.markdown("---")
                st.write("**Study Statistics**")
                total_hours = recent_logs['study_duration'].sum() / 60
                avg_score = recent_logs['quiz_score'].mean()
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Study Hours", f"{total_hours:.1f}")
                col2.metric("Avg Quiz Score", f"{avg_score:.1f}%")
                col3.metric("Total Sessions", len(recent_logs))
            else:
                st.info("No study logs yet. Start logging your sessions!")
        
        st.markdown("---")
        
        # ========== ADMIN PANEL ==========
        with st.expander("🔧 Admin Panel", expanded=False):
            st.markdown("### System Administration & Data Management")
            
            admin_col1, admin_col2 = st.columns(2)
            
            with admin_col1:
                st.markdown("#### 📥 Data Export")
                
                # Export study logs
                logs_df = load_study_logs()
                if not logs_df.empty:
                    csv_logs = logs_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Study Logs (CSV)",
                        data=csv_logs,
                        file_name=f"study_logs_backup_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download all study session logs"
                    )
                
                # Export clustered data
                clustered_df = load_clustered_data()
                if clustered_df is not None:
                    csv_clusters = clustered_df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Cluster Data (CSV)",
                        data=csv_clusters,
                        file_name=f"students_clusters_backup_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download all student clustering data"
                    )
                
                # Export student dataset
                df = load_student_data()
                if df is not None:
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label="📥 Download Student Dataset (CSV)",
                        data=csv_data,
                        file_name=f"students_dataset_backup_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv",
                        help="Download original student performance data"
                    )
            
            with admin_col2:
                st.markdown("#### 🗑️ Data Management")
                
                # View system statistics
                st.markdown("**System Statistics:**")
                col_stat1, col_stat2, col_stat3 = st.columns(3)
                
                logs_df = load_study_logs()
                if not logs_df.empty:
                    col_stat1.metric("Study Logs", len(logs_df))
                else:
                    col_stat1.metric("Study Logs", 0)
                
                clustered_df = load_clustered_data()
                if clustered_df is not None:
                    col_stat2.metric("Clustered Students", len(clustered_df))
                else:
                    col_stat2.metric("Clustered Students", 0)
                
                df = load_student_data()
                if df is not None:
                    col_stat3.metric("Total Students", len(df))
                else:
                    col_stat3.metric("Total Students", 0)
                
                st.markdown("---")
                st.markdown("**Clear Data Actions:**")
                
                # Delete study logs
                if st.button("🗑️ Clear All Study Logs", help="Delete all recorded study sessions"):
                    try:
                        import os
                        if os.path.exists("study_logs.csv"):
                            os.remove("study_logs.csv")
                        st.cache_data.clear()
                        st.success("✅ All study logs cleared successfully")
                    except Exception as e:
                        st.error(f"❌ Error clearing logs: {e}")
                
                # Reset cluster data
                if st.button("🔄 Reset Cluster Data", help="Clear students_with_clusters.csv"):
                    try:
                        import os
                        if os.path.exists("students_with_clusters.csv"):
                            os.remove("students_with_clusters.csv")
                        st.cache_data.clear()
                        st.success("✅ Cluster data reset successfully")
                    except Exception as e:
                        st.error(f"❌ Error resetting clusters: {e}")
            
            st.markdown("---")
            st.markdown("#### ⚙️ Configuration Info")
            
            config_col1, config_col2 = st.columns(2)
            
            with config_col1:
                st.markdown("**Active Clusters:**")
                for cluster_id, cluster_name in CLUSTER_BEHAVIOR.items():
                    st.write(f"• Cluster {cluster_id}: {cluster_name}")
            
            with config_col2:
                st.markdown("**Applied Study Methods:**")
                for cluster_id, params in CLUSTER_STUDY_PARAMS.items():
                    st.write(f"• {CLUSTER_BEHAVIOR[cluster_id]}: {params['duration']}min sessions")
            
            st.markdown("---")
            st.info("ℹ️ **Admin Panel Info:** Use this section to manage data, download backups, and view system statistics. Always backup data before clearing.")

# ========== TAB 5: PROGRESS ANALYTICS ==========
with tab5:
    st.header("📊 Progress Analytics Dashboard")
    
    clustered_df = load_clustered_data()
    logs_df = load_study_logs()
    
    if clustered_df is not None and not logs_df.empty:
        # Convert date
        logs_df['date'] = pd.to_datetime(logs_df['date'])
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Sessions", len(logs_df))
        with col2:
            total_hours = logs_df['study_duration'].sum() / 60
            st.metric("Total Study Hours", f"{total_hours:.1f}")
        with col3:
            avg_score = logs_df['quiz_score'].mean()
            st.metric("Avg Quiz Score", f"{avg_score:.1f}%")
        with col4:
            max_score = logs_df['quiz_score'].max()
            st.metric("Best Score", f"{max_score:.0f}%")
        
        st.markdown("---")
        
        # Study Progress Over Time
        st.subheader("Study Progress Over Time")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_score = px.line(
                logs_df.sort_values('date'),
                x='date',
                y='quiz_score',
                title='Quiz Score Progress',
                markers=True
            )
            st.plotly_chart(fig_score, use_container_width=True)
        
        with col2:
            daily_study = logs_df.groupby('date')['study_duration'].sum() / 60
            fig_study = px.bar(
                x=daily_study.index,
                y=daily_study.values,
                title='Daily Study Hours',
                labels={"x": "Date", "y": "Hours"}
            )
            st.plotly_chart(fig_study, use_container_width=True)
        
        st.markdown("---")
        
        # Study Distribution
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Study Sessions by Time of Day")
            time_dist = logs_df['study_time'].value_counts()
            fig_time = px.pie(
                values=time_dist.values,
                names=time_dist.index,
                title="Study Sessions by Time"
            )
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            st.subheader("Distraction Level Distribution")
            distract_dist = logs_df['distraction_level'].value_counts()
            fig_distract = px.bar(
                x=distract_dist.index,
                y=distract_dist.values,
                title="Distraction Levels",
                labels={"x": "Distraction Level", "y": "Count"}
            )
            st.plotly_chart(fig_distract, use_container_width=True)
        
        st.markdown("---")
        
        # Subject-wise Analysis
        st.subheader("Subject-wise Analysis")
        
        subjects = logs_df[logs_df['subject'].notna()]['subject'].unique()
        
        if len(subjects) > 0:
            subject_data = []
            for subject in subjects:
                subject_logs = logs_df[logs_df['subject'] == subject]
                subject_data.append({
                    'Subject': subject,
                    'Sessions': len(subject_logs),
                    'Total Hours': subject_logs['study_duration'].sum() / 60,
                    'Avg Score': subject_logs['quiz_score'].mean()
                })
            
            subject_df = pd.DataFrame(subject_data)
            st.dataframe(subject_df, use_container_width=True)
    else:
        st.info("📊 No progress data available yet. Start logging study sessions to see analytics!")

# ========== FOOTER ==========
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #888; font-size: 0.9em;'>
    <p>🎓 Integrated Student Analytics & Study Dashboard | Powered by Streamlit & Machine Learning</p>
    <p>Monitor your performance, get personalized study plans, and achieve your academic goals!</p>
</div>
""", unsafe_allow_html=True)
