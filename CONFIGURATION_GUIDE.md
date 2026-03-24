# ⚙️ Configuration & Customization Guide

## Overview

The integrated dashboard is designed to be highly customizable. This guide shows you how to modify behavior, add new clusters, change study parameters, and customize recommendations.

---

## 1. Cluster Configuration

### Location in Code
File: `integrated_dashboard.py`, Lines ~185-230

### Current Cluster Definitions
```python
CLUSTER_BEHAVIOR = {
    0: "High Focus Learners",
    1: "Low Focus Learners",
    2: "Distracted Learners",
    3: "Visual Learners"
}
```

### How to Modify

#### Example 1: Rename a Cluster
**Original:**
```python
CLUSTER_BEHAVIOR = {
    0: "High Focus Learners",
```

**Modified:**
```python
CLUSTER_BEHAVIOR = {
    0: "Achievers - High Focus",
```

#### Example 2: Change Number of Clusters
**Original:**
```python
CLUSTER_BEHAVIOR = {
    0: "High Focus Learners",
    1: "Low Focus Learners",
    2: "Distracted Learners",
    3: "Visual Learners"
}
```

**Modified (add 5th cluster):**
```python
CLUSTER_BEHAVIOR = {
    0: "High Focus Learners",
    1: "Low Focus Learners",
    2: "Distracted Learners",
    3: "Visual Learners",
    4: "Hybrid Learners"
}
```

**Important**: Also add entries to `CLUSTER_STUDY_PARAMS` and `BEHAVIOR_TOOLS` dictionaries!

---

## 2. Study Parameters Configuration

### Location
Lines ~196-230 in `integrated_dashboard.py`

### Current Parameters
```python
CLUSTER_STUDY_PARAMS = {
    0: {  # High focus
        "time_slots": ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM"],
        "duration": 25,  # minutes
        "breaks": "5 min every 25 min",
        "effectiveness": 85,  # percentage
        "method": "Focused deep work sessions"
    },
    1: {  # Low focus
        "time_slots": ["10:00 AM - 12:00 PM", "4:00 PM - 6:00 PM"],
        "duration": 20,
        "breaks": "10 min every 20 min",
        "effectiveness": 70,
        "method": "Short, frequent study sessions"
    },
    # ... more clusters
}
```

### How to Customize

#### Example 1: Change Optimal Study Times
**Before:**
```python
0: {
    "time_slots": ["8:00 AM - 10:00 AM", "2:00 PM - 4:00 PM"],
```

**After (evening focus):**
```python
0: {
    "time_slots": ["5:00 PM - 7:00 PM", "9:00 PM - 11:00 PM"],
```

#### Example 2: Adjust Study Duration
**Before:**
```python
"duration": 25,  # 25-minute Pomodoro sessions
```

**After (longer sessions):**
```python
"duration": 50,  # 50-minute extended sessions
```

#### Example 3: Modify Break Schedule
**Before:**
```python
"breaks": "5 min every 25 min",
```

**After (more frequent breaks):**
```python
"breaks": "10 min every 20 min",
```

#### Example 4: Update Effectiveness Score
**Before:**
```python
"effectiveness": 85,  # percentage improvement potential
```

**After:**
```python
"effectiveness": 90,  # updated based on research
```

#### Example 5: Change Study Method Description
**Before:**
```python
"method": "Focused deep work sessions"
```

**After:**
```python
"method": "Deep focus with minimal distractions - Ideal for complex problem-solving"
```

---

## 3. Recommended Tools Configuration

### Location
Lines ~235-242 in `integrated_dashboard.py`

### Current Tools
```python
BEHAVIOR_TOOLS = {
    "High Focus Learners": ["Mock test platforms", "Advanced study timers"],
    "Low Focus Learners": ["Pomodoro Timer", "Focus music apps"],
    "Distracted Learners": ["Site Blocker", "Noise-cancelling headphones"],
    "Visual Learners": ["Digital Notes", "Mind mapping tools"]
}
```

### How to Add/Modify Tools

#### Example 1: Add More Tools to a Cluster
**Before:**
```python
"High Focus Learners": ["Mock test platforms", "Advanced study timers"],
```

**After:**
```python
"High Focus Learners": [
    "Mock test platforms",
    "Advanced study timers",
    "Note-taking apps",
    "Focus music playlists"
],
```

#### Example 2: Change a Tool Name
**Before:**
```python
"Study timers" 
```

**After:**
```python
"Pomodoro Timer (Focus@Will edition)"
```

#### Example 3: Add a New Cluster's Tools
**After adding Cluster 4:**
```python
BEHAVIOR_TOOLS = {
    # ... existing clusters ...
    "Hybrid Learners": ["Adaptive learning platforms", "Interactive flashcards", "Video tutorials"]
}
```

---

## 4. Feature Selection for Clustering

### Location
Lines ~340-360 in `integrated_dashboard.py` (Tab 2)

### Current Default Features
```python
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
```

### How to Modify

#### Example 1: Add a New Feature
```python
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
    "Stress_Level (1-10)",  # NEW
    "Sleep_Hours_per_Night",  # NEW
]
```

#### Example 2: Remove a Feature
**Before:**
```python
"Participation_Score",
"Projects_Score",
```

**After (less features):**
```python
"Participation_Score",
# "Projects_Score",  # Commented out
```

#### Example 3: Reorder Features
```python
# Priority order:
DEFAULT_FEATURES = [
    "Total_Score",              # Most important
    "Study_Hours_per_Week",
    "Attendance (%)",
    "Final_Score",
    "Midterm_Score",
    "Quizzes_Avg",
    "Assignments_Avg",
    "Participation_Score",
    "Projects_Score",
]
```

---

## 5. Performance Metrics Scoring

### Location
Lines ~550-575 in `integrated_dashboard.py` (Tab 4)

### Current Score-to-Cluster Mapping
```python
if quiz_score >= 80:
    cluster = 0  # High focus
elif quiz_score >= 60:
    cluster = 3  # Visual
elif quiz_score >= 40:
    cluster = 1  # Low focus
else:
    cluster = 2  # Distracted
```

### How to Customize

#### Example 1: Adjust Score Thresholds
**Before:**
```python
if quiz_score >= 80:
    cluster = 0
elif quiz_score >= 60:
    cluster = 3
elif quiz_score >= 40:
    cluster = 1
else:
    cluster = 2
```

**After (stricter thresholds):**
```python
if quiz_score >= 90:      # More strict for high focus
    cluster = 0
elif quiz_score >= 70:    # Shifted up
    cluster = 3
elif quiz_score >= 50:    # Shifted up
    cluster = 1
else:
    cluster = 2
```

#### Example 2: Add More Conditions
**Original (4 clusters):**
```python
if quiz_score >= 80:
    cluster = 0
elif quiz_score >= 60:
    cluster = 3
elif quiz_score >= 40:
    cluster = 1
else:
    cluster = 2
```

**Extended (6 clusters):**
```python
if quiz_score >= 95:
    cluster = 0  # Exceptional
elif quiz_score >= 80:
    cluster = 1  # High focus
elif quiz_score >= 65:
    cluster = 4  # Hybrid
elif quiz_score >= 50:
    cluster = 3  # Visual
elif quiz_score >= 35:
    cluster = 2  # Low focus
else:
    cluster = 5  # Needs help
```

---

## 6. Styling & Visual Customization

### Location
Lines ~15-85 in `integrated_dashboard.py` (CSS section)

### Current Color Scheme
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

### How to Change Colors

#### Example 1: Different Background Gradient
**Before:**
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

**After (warm palette):**
```css
background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
```

#### Example 2: Card Styling
**Before:**
```css
.recommendation-card {
    border-left: 5px solid #3498db;
}
```

**After (green accent):**
```css
.recommendation-card {
    border-left: 5px solid #27ae60;
}
```

#### Example 3: Change Sidebar Color
**Before:**
```css
background: linear-gradient(180deg, #34495e 0%, #2c3e50 100%);
```

**After (blue sidebar):**
```css
background: linear-gradient(180deg, #2c3e50 0%, #3498db 100%);
```

---

## 7. Adding New Features to Tabs

### Add a New Visualization (Tab 1 - Data Analysis)

**Location**: After line ~605 in Tab 1 section

**Template:**
```python
# Add this new visualization
st.subheader("New Chart Title")

new_fig = px.scatter(
    df,
    x="Column_Name_1",
    y="Column_Name_2",
    color="Column_Name_3",
    title="New Chart Title",
    hover_data=["Column_Name_4"]
)
st.plotly_chart(new_fig, use_container_width=True)
```

### Add a New Metric to Tab 5 - Progress Analytics

**Location**: After line ~920 in Tab 5 section

**Template:**
```python
# Add metric in the 4-column layout
with col4:
    new_metric_value = logs_df['column_name'].mean()
    st.metric("New Metric Label", f"{new_metric_value:.1f}")
```

---

## 8. Data Source Configuration

### Location
Lines ~100-120 in `integrated_dashboard.py`

### Current Data Paths
```python
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
```

### How to Change Data Source

#### Example 1: Add Alternative Path
**Before:**
```python
if os.path.exists("Students Performance Dataset.csv"):
    df = pd.read_csv("Students Performance Dataset.csv")
else:
    df = pd.read_csv(r"D:\Desktop\app\Students Performance Dataset.csv")
```

**After (add third fallback):**
```python
if os.path.exists("Students Performance Dataset.csv"):
    df = pd.read_csv("Students Performance Dataset.csv")
elif os.path.exists(r"D:\Desktop\app\Students Performance Dataset.csv"):
    df = pd.read_csv(r"D:\Desktop\app\Students Performance Dataset.csv")
else:
    df = pd.read_csv(r"C:\Data\students.csv")  # New fallback
```

#### Example 2: Use Different Filename
**Before:**
```python
df = pd.read_csv("Students Performance Dataset.csv")
```

**After:**
```python
df = pd.read_csv("student_data_2024.csv")  # Different name
```

---

## 9. Common Customization Scenarios

### Scenario 1: More Aggressive Study Times
Replace all time slots with earlier hours:
```python
CLUSTER_STUDY_PARAMS = {
    0: {
        "time_slots": ["6:00 AM - 8:00 AM", "1:00 PM - 3:00 PM"],
        "duration": 45,  # Longer sessions
        "breaks": "10 min every 45 min",  # Less frequent
        "effectiveness": 95,  # Higher effectiveness
        "method": "Early morning deep focus"
    },
    # ... rest of clusters
}
```

### Scenario 2: Add More Tools/Resources
Expand tools for all clusters:
```python
BEHAVIOR_TOOLS = {
    "High Focus Learners": [
        "Mock test platforms",
        "Advanced study timers",
        "Focus ambient sounds",
        "Note-taking apps",
        "Interactive flashcards"
    ],
    # ... etc for other clusters
}
```

### Scenario 3: Customize for Different Languages
Modify cluster names and descriptions:
```python
CLUSTER_BEHAVIOR = {
    0: "फोकस्ड लर्नर्स (Focused Learners)",  # Add translations
    1: "कम फोकस (Low Focus)",
    # etc...
}
```

### Scenario 4: Adjust for Different Student Levels
Modify thresholds based on grade level:
```python
# For high school students - lower thresholds
if quiz_score >= 75:
    cluster = 0
elif quiz_score >= 55:
    cluster = 3
# ... etc

# For university students - higher expectations
if quiz_score >= 85:
    cluster = 0
elif quiz_score >= 70:
    cluster = 3
# ... etc
```

---

## 10. Testing Your Changes

### Checklist After Making Changes

- [ ] No Python syntax errors (test with `python -m py_compile integrated_dashboard.py`)
- [ ] All cluster entries have corresponding study params
- [ ] All clusters have tool recommendations
- [ ] All new features reference correct column names
- [ ] CSV paths are correct for your system
- [ ] Dashboard loads without errors: `streamlit run integrated_dashboard.py`
- [ ] Tab 1 visualizations display correctly
- [ ] Tab 2 clustering runs without errors
- [ ] Tab 3 shows updated cluster names
- [ ] Tab 4 form works and saves logs
- [ ] Tab 5 analytics display correctly

### Quick Syntax Check
```powershell
python -m py_compile integrated_dashboard.py
```
If no output, syntax is correct!

---

## 11. Backup Best Practices

### Before Making Changes
```powershell
# Create a backup
Copy-Item integrated_dashboard.py integrated_dashboard_backup.py
```

### Version Control
```powershell
# If using Git
git commit -am "Configuration changes: Updated cluster params"
```

---

## 12. Configuration Template

Create a separate config file for future use:

**Create file: `config.py`**
```python
# Cluster Configuration
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
    # ... rest of config
}

# Import in dashboard:
# from config import CLUSTER_BEHAVIOR, CLUSTER_STUDY_PARAMS
```

Then use in dashboard:
```python
# Add this at top of integrated_dashboard.py
try:
    from config import CLUSTER_BEHAVIOR, CLUSTER_STUDY_PARAMS, BEHAVIOR_TOOLS
except ImportError:
    # Use defaults if config not found
    pass
```

---

## 13. Getting Help

### Common Issues When Customizing

**Issue**: "KeyError: cluster number"
- **Cause**: Missing cluster entry in dictionaries
- **Fix**: Add all 4 dictionaries (BEHAVIOR, PARAMS, TOOLS) with same cluster numbers

**Issue**: "Column not found"
- **Cause**: Typo in column name
- **Fix**: Check exact spelling against CSV headers

**Issue**: "Dashboard won't load"
- **Cause**: Python syntax error
- **Fix**: Run syntax check, look for missing colons/quotes

---

## Quick Reference: What to Edit

| To Change | Edit This | Type |
|-----------|-----------|------|
| Cluster names | CLUSTER_BEHAVIOR | Dictionary |
| Study times | CLUSTER_STUDY_PARAMS | Dictionary |
| Recommended tools | BEHAVIOR_TOOLS | Dictionary |
| Colors/styling | CSS section | CSS |
| Data source path | load_student_data() | Function |
| Features used | DEFAULT_FEATURES | List |
| Score thresholds | Tab 4 cluster logic | If/elif |
| New visualization | Add after existing chart | Code |

---

**Happy customizing!** 🎨

For more help, see QUICK_START_GUIDE.md and README_INTEGRATED_DASHBOARD.md
