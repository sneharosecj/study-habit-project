import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fpdf import FPDF

st.set_page_config(layout="wide", page_title="Personalized Study Plans")

st.title("Personalized Study Plans Dashboard")

st.markdown("""
<style>
/* Overall app styling */
.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* Title styling */
.stTitle h1 {
    color: #2c3e50;
    text-align: center;
    font-weight: bold;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

/* Sidebar styling */
.stSidebar {
    background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
    color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}

.stSidebar h2 {
    color: #ecf0f1;
    font-size: 1.2em;
}

.stSidebar .stSelectbox label {
    color: #ecf0f1 !important;
    font-weight: bold;
}

.stSidebar .stSelectbox div[data-baseweb="select"] {
    background-color: #ecf0f1 !important;
    border-radius: 5px;
}

/* Subheader styling */
.stSubheader h3 {
    color: #e74c3c;
    font-weight: bold;
    border-bottom: 2px solid #e74c3c;
    padding-bottom: 5px;
    margin-bottom: 15px;
}

/* Button styling */
.stButton button {
    background: linear-gradient(45deg, #3498db, #2980b9);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 10px 20px;
    font-weight: bold;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.2);
}

.stButton button:hover {
    background: linear-gradient(45deg, #2980b9, #21618c);
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0,0,0,0.3);
}

/* Text area styling */
.stTextArea textarea {
    background-color: #f0f8ff !important;
    border: 2px solid #4CAF50 !important;
    border-radius: 10px !important;
    color: #333 !important;
    font-size: 16px !important;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.1);
}

/* Success message styling */
.stSuccess {
    background-color: #d4edda !important;
    border-color: #c3e6cb !important;
    color: #155724 !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Chatbot header styling */
.chatbot-header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 15px;
    border-radius: 15px;
    color: white;
    text-align: center;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.2);
}

.chatbot-header h4 {
    margin: 0;
    font-size: 1.4em;
}

.chatbot-header p {
    margin: 5px 0 0 0;
    font-size: 1em;
}

/* Markdown styling */
.stMarkdown h3 {
    color: #27ae60;
    font-weight: bold;
}

/* Info message styling */
.stInfo {
    background-color: #d1ecf1 !important;
    border-color: #bee5eb !important;
    color: #0c5460 !important;
    border-radius: 10px !important;
}

/* Column styling for better layout */
.css-1lcbmhc {  /* This is the class for columns in Streamlit */
    background: rgba(255, 255, 255, 0.8);
    border-radius: 10px;
    padding: 15px;
    margin: 5px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

/* Plotly chart container */
.js-plotly-plot {
    border-radius: 10px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
</style>
""", unsafe_allow_html=True)

# Load clustered data
@st.cache_data
def load_clustered_data():
    try:
        df = pd.read_csv("students_with_clusters.csv")
        return df
    except FileNotFoundError:
        st.error("students_with_clusters.csv not found. Please run the clustering dashboard first.")
        return None

df = load_clustered_data()
if df is None:
    st.stop()

# Define cluster behavior mappings
cluster_behavior = {
    0: "High focus",
    1: "Low focus", 
    2: "Distracted learners",
    3: "Visual learners"
}

# Define tools based on behavior
behavior_tools = {
    "High focus": "Mock test platforms",
    "Low focus": "Pomodoro Timer",
    "Distracted learners": "Site Blocker",
    "Visual learners": "Digital Notes"
}

# Define study plan parameters based on cluster
cluster_study_params = {
    0: {  # High focus
        "time_slots": ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM"],
        "duration": 25,  # minutes
        "breaks": "5 min every 25 min",
        "effectiveness": 85
    },
    1: {  # Low focus
        "time_slots": ["10:00 AM - 12:00 PM", "4:00 PM - 6:00 PM"],
        "duration": 20,
        "breaks": "10 min every 20 min", 
        "effectiveness": 70
    },
    2: {  # Distracted
        "time_slots": ["7:00 AM - 9:00 AM", "7:00 PM - 9:00 PM"],
        "duration": 15,
        "breaks": "15 min every 15 min",
        "effectiveness": 60
    },
    3: {  # Visual
        "time_slots": ["9:00 AM - 11:00 AM", "3:00 PM - 5:00 PM"],
        "duration": 30,
        "breaks": "5 min every 30 min",
        "effectiveness": 80
    }
}

# Sidebar for student selection
st.sidebar.header("Select Student")
if "Student_ID" in df.columns:
    student_options = [f"{row['Student_ID']} - Cluster {int(row['Cluster_KMeans'])}" for _, row in df.iterrows() if pd.notna(row['Student_ID'])]
    selected_student = st.sidebar.selectbox("Choose a student", student_options)
else:
    st.error("No Student_ID column found.")
    st.stop()

if selected_student:
    selected_id = selected_student.split(" - ")[0]
    student_data = df[df["Student_ID"] == selected_id].iloc[0]
    cluster = int(student_data["Cluster_KMeans"])
    behavior = cluster_behavior.get(cluster, "Unknown")
    tool = behavior_tools.get(behavior, "General study tools")
    params = cluster_study_params.get(cluster, {
        "time_slots": ["9:00 AM - 11:00 AM"],
        "duration": 25,
        "breaks": "5 min breaks",
        "effectiveness": 75
    })

    st.header(f"Study Plan for {student_data['First_Name']} {student_data['Last_Name']} (ID: {selected_id})")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Student Profile")
        st.write(f"**Cluster:** {cluster} - {behavior}")
        st.write(f"**Current Total Score:** {student_data['Total_Score']:.2f}")
        st.write(f"**Study Hours per Week:** {student_data['Study_Hours_per_Week']}")
        st.write(f"**Attendance:** {student_data['Attendance (%)']}%")
        st.write(f"**Stress Level:** {student_data['Stress_Level (1-10)']}/10")
        st.write(f"**Sleep Hours:** {student_data['Sleep_Hours_per_Night']}")
    
    with col2:
        st.subheader("Recommended Tool")
        st.write(f"**{tool}**")
        st.write("This tool is recommended based on your learning behavior pattern.")
    
    st.markdown("---")
    
    st.subheader("Personalized Study Plan")
    
    col3 = st.columns(1)[0]
    
    with col3:
        st.write("**Optimal Study Time Slots:**")
        for slot in params["time_slots"]:
            st.write(f"- {slot}")
        
        st.write(f"**Study Duration Pattern:** {params['duration']} minutes focused study")
        st.write(f"**Break Schedule:** {params['breaks']}")
        st.write(f"**Expected Effectiveness:** {params['effectiveness']}% improvement potential")
    
    st.markdown("---")
    
    # Performance Breakdown Chart
    st.subheader("Performance Breakdown by Component")
    
    components = ["Midterm_Score", "Final_Score", "Assignments_Avg", "Quizzes_Avg", "Participation_Score", "Projects_Score"]
    component_labels = ["Midterm", "Final", "Assignments", "Quizzes", "Participation", "Projects"]
    component_values = [student_data.get(comp, 0) for comp in components]
    
    fig_perf = px.bar(x=component_labels, y=component_values,
                      labels={"x": "Component", "y": "Score"},
                      title="Student Performance Across Components",
                      color=component_values,
                      color_continuous_scale="Viridis")
    st.plotly_chart(fig_perf, use_container_width=True)
    
    st.markdown("---")
    
    # Weekly Study Schedule Chart
    st.subheader("Weekly Study Schedule")
    
    # Assume hours per day based on cluster
    daily_hours = {
        0: [2, 2, 1.5, 2, 2, 1, 1],  # High focus: more on weekdays
        1: [1, 1, 1, 1, 1, 0.5, 0.5],  # Low focus: less consistent
        2: [1.5, 1, 1, 1.5, 1, 2, 1],  # Distracted: varied
        3: [2, 1.5, 2, 1.5, 2, 1, 1]   # Visual: balanced
    }.get(cluster, [1.5]*7)
    
    days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    
    fig = px.bar(x=days, y=daily_hours, labels={"x": "Day", "y": "Hours"},
                 title="Recommended Study Hours per Day")
    st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # Expected Performance Improvement
    st.subheader("Expected Performance Improvement")
    
    current_score = student_data["Total_Score"]
    improvement = params["effectiveness"] / 100 * (100 - current_score)  # Assume max 100
    predicted_score = min(100, current_score + improvement)
    
    weeks = list(range(5))  # 4 weeks + current
    scores = [current_score]
    for i in range(1, 5):
        scores.append(current_score + (predicted_score - current_score) * i / 4)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=weeks, y=scores, mode='lines+markers', name='Predicted Score'))
    fig2.add_hline(y=current_score, line_dash="dash", annotation_text="Current Score")
    fig2.update_layout(title="Score Improvement Over 4 Weeks",
                       xaxis_title="Weeks", yaxis_title="Score")
    st.plotly_chart(fig2, use_container_width=True)
    
    st.markdown("---")
    
    # Behavior Indicators Chart
    st.subheader("Student Behavior & Wellness Indicators")
    
    behavior_metrics = ["Stress_Level (1-10)", "Sleep_Hours_per_Night", "Attendance (%)"]
    behavior_labels = ["Stress Level", "Sleep Hours", "Attendance %"]
    behavior_values = [student_data.get(metric, 0) for metric in behavior_metrics]
    
    # Normalize for better visualization (stress on 0-10, sleep on 0-10, attendance on 0-100)
    behavior_values_normalized = [
        student_data.get("Stress_Level (1-10)", 0),
        student_data.get("Sleep_Hours_per_Night", 0) * 10,  # Convert to 0-100 scale
        student_data.get("Attendance (%)", 0)
    ]
    
    fig_behavior = go.Figure(data=[
        go.Bar(x=behavior_labels, y=[student_data.get("Stress_Level (1-10)", 0)], name="Stress Level (1-10)", marker_color="indianred"),
        go.Bar(x=behavior_labels, y=[student_data.get("Sleep_Hours_per_Night", 0)], name="Sleep Hours", marker_color="lightsalmon"),
        go.Bar(x=behavior_labels[2:], y=[student_data.get("Attendance (%)", 0)], name="Attendance %", marker_color="lightgreen")
    ])
    fig_behavior.update_layout(title="Behavior Indicators Overview", barmode="group", yaxis_title="Value")
    st.plotly_chart(fig_behavior, use_container_width=True)
    
    st.markdown("---")
    
    # Subject-wise recommendations
    st.subheader("Subject-wise Recommendations")
    
    subjects = ["Mathematics", "Business", "Engineering", "CS"]
    recommendations = {
        "Mathematics": "Focus on problem-solving practice and concept visualization",
        "Business": "Case study analysis and group discussions",
        "Engineering": "Hands-on projects and technical documentation",
        "CS": "Coding practice and algorithm implementation"
    }
    
    if "Department" in student_data.index:
        dept = student_data["Department"]
        if dept in recommendations:
            st.write(f"**{dept}:** {recommendations[dept]}")
        else:
            st.write(f"**{dept}:** General study techniques recommended")
    
    for subj in subjects:
        if subj != dept:
            st.write(f"**{subj}:** {recommendations[subj]}")
    
    st.markdown("---")
    
    # Additional features
    st.subheader("Additional Study Tools")
    
    col5, col6 = st.columns(2)
    
    with col5:
        st.write("**Exam Countdown Planner**")
        st.write("Set exam dates and get daily study reminders.")
        exam_date = st.date_input("Select exam date")
        if exam_date:
            days_left = (exam_date - datetime.now().date()).days
            st.write(f"Days until exam: {max(0, days_left)}")
    
    with col6:
         st.markdown('<div class="chatbot-header"><h4>AI Chatbot for Study Guidance</h4><p>Get instant help with study questions and concepts.</p></div>', unsafe_allow_html=True)

    question = st.text_area("Ask the AI chatbot:", placeholder="Type your question here...")

    if question:
        q = question.lower()

        if "focus" in q:
            response = "Try the Pomodoro technique: Study for 25 minutes and take a 5 minute break."

        elif "stress" in q:
            response = "Take short breaks, sleep at least 7 hours, and avoid studying continuously for long periods."

        elif "math" in q:
            response = "Practice problem solving daily and review formulas regularly."

        elif "exam" in q:
            response = "Start revising key topics, practice past papers, and review weak areas."

        elif "sleep" in q:
            response = "Students should ideally sleep 7-8 hours for better memory and focus."

        elif "study plan" in q:
            response = "Follow your personalized schedule and revise topics daily."

        else:
            response = "Focus on regular revision, active recall, and solving practice questions."

        st.success(response)
    
    st.write("**Adaptive Recommendations**")
    st.write("Based on your progress, recommendations will adapt over time.")
    
    # Download study plan
    st.markdown("---")
    st.subheader("Download Study Plan")
    
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=14)
    pdf.cell(200, 10, txt="Personalized Study Plan", ln=True, align='C')
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Student: {student_data['First_Name']} {student_data['Last_Name']} (ID: {selected_id})", ln=True)
    pdf.cell(200, 10, txt=f"Total Score: {student_data['Total_Score']:.2f}", ln=True)
    pdf.cell(200, 10, txt=f"Study Hours per Week: {student_data['Study_Hours_per_Week']}", ln=True)
    pdf.cell(200, 10, txt=f"Attendance: {student_data['Attendance (%)']}%", ln=True)
    pdf.cell(200, 10, txt=f"Stress Level: {student_data['Stress_Level (1-10)']}/10", ln=True)
    pdf.cell(200, 10, txt=f"Sleep Hours: {student_data['Sleep_Hours_per_Night']}", ln=True)
    pdf.cell(200, 10, txt="", ln=True)  # blank line
    pdf.cell(200, 10, txt=f"Cluster: {cluster} - {behavior}", ln=True)
    pdf.cell(200, 10, txt=f"Recommended Tool: {tool}", ln=True)
    pdf.cell(200, 10, txt="", ln=True)
    pdf.cell(200, 10, txt="Study Plan Details:", ln=True)
    pdf.cell(200, 10, txt=f"Time Slots: {', '.join(params['time_slots'])}", ln=True)
    pdf.cell(200, 10, txt=f"Duration: {params['duration']} minutes", ln=True)
    pdf.cell(200, 10, txt=f"Breaks: {params['breaks']}", ln=True)
    pdf.cell(200, 10, txt=f"Expected Effectiveness: {params['effectiveness']}%", ln=True)
    pdf.cell(200, 10, txt="", ln=True)
    pdf.cell(200, 10, txt="Weekly Schedule:", ln=True)
    for day, hours in zip(days, daily_hours):
        pdf.cell(200, 10, txt=f"{day}: {hours} hours", ln=True)
    pdf.cell(200, 10, txt="", ln=True)
    pdf.cell(200, 10, txt=f"Current Score: {current_score}", ln=True)
    pdf.cell(200, 10, txt=f"Predicted Score after 4 weeks: {predicted_score:.2f}", ln=True)
    
    pdf_bytes = pdf.output(dest='S').encode('latin-1')
    st.download_button("Download Study Plan (PDF)", data=pdf_bytes, file_name=f"study_plan_{selected_id}.pdf", mime="application/pdf")

else:
    st.info("Select a student from the sidebar to view their personalized study plan.")
