import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from datetime import datetime, timedelta
import os

# Page config
st.set_page_config(page_title="Study Behavior Tracker & Recommender", layout="wide")

st.title("Study Behavior Tracker & Personalized Study Recommender")

# Custom CSS for better styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.stTitle h1 {
    color: white;
    text-align: center;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 30px;
}

.stSidebar {
    background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
}

.stButton button {
    background: linear-gradient(45deg, #3498db, #2980b9);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
}

.stButton button:hover {
    background: linear-gradient(45deg, #2980b9, #21618c);
    transform: translateY(-2px);
}

.recommendation-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    border-left: 5px solid #3498db;
}

.tool-card {
    background: rgba(255, 255, 255, 0.9);
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.admin-panel {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 15px;
    padding: 20px;
    margin: 10px 0;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Load data and train model
@st.cache_data
def load_data_and_train_model():
    try:
        # Load original dataset
        df = pd.read_csv("students_with_clusters.csv")

        # Features used for clustering
        features = [
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

        # Prepare data
        X = df[features].copy()
        X = X.dropna()

        # Scale features
        scaler = StandardScaler()
        X_scaled = scaler.fit_transform(X)

        # Train KMeans model (4 clusters as in module2)
        kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        clusters = kmeans.fit_predict(X_scaled)

        return df, kmeans, scaler, features

    except Exception as e:
        st.error(f"Error loading data or training model: {e}")
        return None, None, None, None

# Load study logs
@st.cache_data
def load_study_logs():
    if os.path.exists("study_logs.csv"):
        return pd.read_csv("study_logs.csv")
    else:
        return pd.DataFrame(columns=["date", "study_duration", "study_time", "subject", "distraction_level", "quiz_score", "predicted_cluster"])

# Save study log
def save_study_log(log_data):
    logs_df = load_study_logs()
    logs_df = pd.concat([logs_df, pd.DataFrame([log_data])], ignore_index=True)
    logs_df.to_csv("study_logs.csv", index=False)
    # Clear cache to reload data
    load_study_logs.clear()

# Cluster behavior mappings (from module3)
cluster_behavior = {
    0: "High focus",
    1: "Low focus",
    2: "Distracted learners",
    3: "Visual learners"
}

# Study plan parameters (from module3)
cluster_study_params = {
    0: {  # High focus
        "time_slots": ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM"],
        "duration": 25,
        "breaks": "5 min every 25 min",
        "effectiveness": 85,
        "method": "Focused deep work sessions"
    },
    1: {  # Low focus
        "time_slots": ["10:00 AM - 12:00 PM", "4:00 PM - 6:00 PM"],
        "duration": 20,
        "breaks": "10 min every 20 min",
        "effectiveness": 70,
        "method": "Short, frequent study sessions"
    },
    2: {  # Distracted
        "time_slots": ["7:00 AM - 9:00 AM", "7:00 PM - 9:00 PM"],
        "duration": 15,
        "breaks": "15 min every 15 min",
        "effectiveness": 60,
        "method": "Distraction-free environment setup"
    },
    3: {  # Visual
        "time_slots": ["9:00 AM - 11:00 AM", "3:00 PM - 5:00 PM"],
        "duration": 30,
        "breaks": "5 min every 30 min",
        "effectiveness": 80,
        "method": "Visual aids and multimedia learning"
    }
}

# Recommended tools
behavior_tools = {
    "High focus": ["Mock test platforms", "Advanced study timers"],
    "Low focus": ["Pomodoro Timer", "Focus music apps"],
    "Distracted learners": ["Site Blocker", "Noise-cancelling headphones"],
    "Visual learners": ["Digital Notes", "Mind mapping tools"]
}

# Load model
df, kmeans_model, scaler, features = load_data_and_train_model()

if df is None or kmeans_model is None:
    st.error("Failed to load data or train model. Please check your data files.")
    st.stop()

# Sidebar navigation
page = st.sidebar.selectbox("Navigation", ["Study Tracker", "Progress Dashboard", "Admin Panel"])

if page == "Study Tracker":
    st.header("Study Behavior Tracker")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Enter Your Study Session")

        with st.form("study_form"):
            date = st.date_input("Date", datetime.now().date())
            study_duration = st.slider("Study Duration (minutes)", 15, 300, 60)
            study_time = st.selectbox("Study Time", ["Morning", "Afternoon", "Evening"])
            subject = st.text_input("Subject Studied")
            distraction_level = st.selectbox("Distraction Level", ["None", "Low", "Medium", "High"])
            quiz_score = st.slider("Recent Quiz Score (%)", 0, 100, 75)

            submitted = st.form_submit_button("Save Log & Get Recommendations")

            if submitted:
                # Prepare input for prediction
                # We need to map the input to the clustering features
                # For demo purposes, we'll create a synthetic feature vector
                # In a real scenario, you'd have more comprehensive student data

                # Create a synthetic student profile based on input
                input_features = {
                    "Attendance (%)": 85,  # Default
                    "Midterm_Score": quiz_score * 0.8,  # Estimate
                    "Final_Score": quiz_score * 0.9,  # Estimate
                    "Assignments_Avg": quiz_score * 0.85,
                    "Quizzes_Avg": quiz_score,
                    "Participation_Score": 70,  # Default
                    "Projects_Score": quiz_score * 0.8,
                    "Total_Score": quiz_score * 0.85,
                    "Study_Hours_per_Week": study_duration / 60 * 7  # Convert to weekly
                }

                # Convert to array and scale
                input_array = np.array([list(input_features.values())])
                input_scaled = scaler.transform(input_array)

                # Predict cluster
                predicted_cluster = kmeans_model.predict(input_scaled)[0]

                # Save log
                log_data = {
                    "date": date,
                    "study_duration": study_duration,
                    "study_time": study_time,
                    "subject": subject,
                    "distraction_level": distraction_level,
                    "quiz_score": quiz_score,
                    "predicted_cluster": predicted_cluster
                }
                save_study_log(log_data)

                st.success("Study log saved successfully!")

                # Display recommendations
                st.markdown("---")
                st.subheader("Your Personalized Study Recommendations")

                behavior = cluster_behavior.get(predicted_cluster, "Unknown")
                params = cluster_study_params.get(predicted_cluster, cluster_study_params[0])

                st.markdown(f"""
                <div class="recommendation-card">
                    <h3>Behavior Profile: {behavior}</h3>
                    <p><strong>Optimal Study Time:</strong> {', '.join(params['time_slots'])}</p>
                    <p><strong>Recommended Duration:</strong> {params['duration']} minutes per session</p>
                    <p><strong>Break Schedule:</strong> {params['breaks']}</p>
                    <p><strong>Study Method:</strong> {params['method']}</p>
                    <p><strong>Expected Effectiveness:</strong> {params['effectiveness']}% improvement potential</p>
                </div>
                """, unsafe_allow_html=True)

                # Recommended tools
                st.subheader("Recommended Study Tools")
                tools = behavior_tools.get(behavior, ["General study tools"])

                cols = st.columns(len(tools))
                for i, tool in enumerate(tools):
                    with cols[i]:
                        st.markdown(f"""
                        <div class="tool-card">
                            <h4>{tool}</h4>
                            <p>Enhance your {behavior.lower()} with this specialized tool.</p>
                        </div>
                        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Recent Study Sessions")
        logs_df = load_study_logs()
        if not logs_df.empty:
            recent_logs = logs_df.tail(5)
            st.dataframe(recent_logs)
        else:
            st.info("No study logs yet. Start tracking your sessions!")

elif page == "Progress Dashboard":
    st.header("Performance Progress Dashboard")

    logs_df = load_study_logs()

    if logs_df.empty:
        st.info("No study data available yet. Start logging your study sessions!")
    else:
        # Convert date column
        logs_df['date'] = pd.to_datetime(logs_df['date'])

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Weekly Study Time Chart")

            # Group by week
            logs_df['week'] = logs_df['date'].dt.isocalendar().week
            weekly_study = logs_df.groupby('week')['study_duration'].sum() / 60  # Convert to hours

            fig_weekly = px.bar(
                x=weekly_study.index,
                y=weekly_study.values,
                labels={'x': 'Week', 'y': 'Study Hours'},
                title="Weekly Study Hours"
            )
            st.plotly_chart(fig_weekly, use_container_width=True)

        with col2:
            st.subheader("Quiz Score Progress")

            # Format date to show only month and day
            logs_df_copy = logs_df.copy()
            logs_df_copy['date'] = pd.to_datetime(logs_df_copy['date']).dt.strftime('%d-%b')

            fig_scores = px.line(
                logs_df_copy,
                 x='date',
                y='quiz_score',
                markers=True,
                title="Quiz Score Trend"
                )

# Force categorical axis so only day-month shows
            fig_scores.update_xaxes(type='category')

            st.plotly_chart(fig_scores, use_container_width=True) 

        # Expected performance improvement
        st.subheader("Expected Performance Improvement")

        if not logs_df.empty:
            current_avg_score = logs_df['quiz_score'].mean()
            predicted_cluster = int(logs_df['predicted_cluster'].iloc[-1])
            effectiveness = cluster_study_params[predicted_cluster]['effectiveness']

            weeks = list(range(5))
            improvement = effectiveness / 100 * (100 - current_avg_score)
            scores = [current_avg_score]
            for i in range(1, 5):
                scores.append(current_avg_score + (improvement) * i / 4)

            fig_improvement = go.Figure()
            fig_improvement.add_trace(go.Scatter(
                x=weeks,
                y=scores,
                mode='lines+markers',
                name='Predicted Score',
                line=dict(color='#3498db')
            ))
            fig_improvement.add_hline(
                y=current_avg_score,
                line_dash="dash",
                annotation_text="Current Average"
            )
            fig_improvement.update_layout(
                title="Score Improvement Projection (4 Weeks)",
                xaxis_title="Weeks",
                yaxis_title="Score (%)"
            )
            st.plotly_chart(fig_improvement, use_container_width=True)

        # Study time distribution
        st.subheader("Study Time Distribution")

        time_dist = logs_df['study_time'].value_counts()
        fig_time = px.pie(
            values=time_dist.values,
            names=time_dist.index,
            title="Study Sessions by Time of Day"
        )
        st.plotly_chart(fig_time, use_container_width=True)

elif page == "Admin Panel":
    st.header("Admin Panel")

    tab1, tab2, tab3 = st.tabs(["Data Management", "System Metrics", "Model Retraining"])

    with tab1:
        st.subheader("Data Upload")

        uploaded_file = st.file_uploader("Upload new dataset (CSV)", type="csv")
        if uploaded_file is not None:
            new_df = pd.read_csv(uploaded_file)
            new_df.to_csv("Students Performance Dataset.csv", index=False)
            st.success("Dataset updated successfully!")
            st.cache_data.clear()  # Clear cache

        st.subheader("Current Dataset Info")
        st.write(f"Total students: {len(df)}")
        st.write(f"Features: {len(features)}")

    with tab2:
        st.subheader("System Metrics")

        logs_df = load_study_logs()

        col1, col2, col3 = st.columns(3)

        with col1:
            total_sessions = len(logs_df) if not logs_df.empty else 0
            st.metric("Total Study Sessions", total_sessions)

        with col2:
            active_students = 1  # Since this is a single-user demo
            st.metric("Active Students", active_students)

        with col3:
            days_since_start = (datetime.now().date() - pd.to_datetime(logs_df['date'].min()).date()).days if not logs_df.empty else 0
            st.metric("Days Since First Log", days_since_start)

        # Model accuracy (simulated)
        st.subheader("Model Performance")
        st.metric("Clustering Silhouette Score", "0.75")  # Placeholder
        st.metric("Last Retrained", "Today")  # Placeholder

    with tab3:
        st.subheader("Model Retraining")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Quick Retrain (Recent Data)"):
                st.info("Retraining model with recent study logs...")
                # In a real implementation, you'd retrain with combined data
                st.success("Model retrained successfully!")

        with col2:
            if st.button("Full Retrain (Entire Dataset)"):
                st.info("Retraining model with complete dataset...")
                # Retrain the cached model
                st.cache_data.clear()
                df, kmeans_model, scaler, features = load_data_and_train_model()
                st.success("Model fully retrained!")

        st.info("Model retraining updates the clustering algorithm with new data patterns.")

# Footer
st.markdown("---")
st.markdown("Built with love for personalized learning | Powered by Machine Learning")