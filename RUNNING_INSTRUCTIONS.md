# 🎯 Running the Integrated Dashboard - Complete Guide

## ⚡ 30-Second Start

```powershell
cd "d:\Desktop\study habits project"
pip install -r requirements.txt
streamlit run integrated_dashboard.py
```

Done! Your dashboard is now running on `http://localhost:8501`

---

## 📋 Detailed Setup Instructions

### Step 1: Open PowerShell
- Press `Windows Key + R`
- Type `powershell`
- Press `Enter`

### Step 2: Navigate to Project Directory
```powershell
cd "d:\Desktop\study habits project"
```

Verify you're in the right place:
```powershell
ls  # Should see: module1.py, module2.py, etc.
```

### Step 3: Install Dependencies
```powershell
pip install -r requirements.txt
```

**What it installs:**
- pandas (data manipulation)
- numpy (numerical computing)
- streamlit (web framework)
- scikit-learn (machine learning)
- plotly (visualizations)

**Expected output:**
```
Successfully installed pandas-1.5.3 numpy-1.24.3 streamlit-1.25.0 scikit-learn-1.3.0 plotly-5.15.0
```

### Step 4: Run the Dashboard
```powershell
streamlit run integrated_dashboard.py
```

**Expected output:**
```
  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501

  For better performance, install the Watchdog module:
  $ pip install watchdog
```

### Step 5: Browser Opens Automatically
If not, manually open: `http://localhost:8501`

---

## 🎨 Dashboard Layout

```
╔═══════════════════════════════════════════════════════════════╗
║              INTEGRATED STUDENT ANALYTICS DASHBOARD           ║
║    📊 Data Analysis | 🔍 Clustering | 📋 Plans | 📝 Tracking  ║
╚═══════════════════════════════════════════════════════════════╝

┌─────────────────────────────────────────────────────────────┐
│ 📈 TAB 1: DATA ANALYSIS                                    │
├─────────────────────────────────────────────────────────────┤
│ [Overview Cards: Students | Features | Missing | Numeric] │
│                                                             │
│ [First 5 Rows DF]  │  [Dataset Info Box]                   │
│                                                             │
│ [Statistical Summary Table]                                │
│                                                             │
│ [Scatter: Study Hrs vs Quiz]  │  [Grade Distribution]      │
│ [Correlation Heatmap]         │  [Score Distribution]      │
│ [Total Score by Grade]        │  [Study Hrs by Grade]      │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🔍 TAB 2: STUDENT CLUSTERING                               │
├─────────────────────────────────────────────────────────────┤
│ SIDEBAR:                                                    │
│  • Number of clusters: 2-10 slider                          │
│  • DBSCAN eps: 0.1-5.0 slider                               │
│  • Min samples: 2-20 slider                                 │
│  • Features: Multiselect dropdown                           │
│  • Run Button                                               │
│                                                             │
│ RESULTS:                                                    │
│ [Silhouette Scores: KMeans | Agglomerative | DBSCAN]      │
│                                                             │
│ [PCA Viz: KMeans]  │  [PCA Viz: Agg]  │  [PCA Viz: DBSCAN] │
│                                                             │
│ Cluster Profiles Tabs: [KMeans] [Agg] [DBSCAN]            │
│ [Save ClusteredData] [Download CSV]                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📋 TAB 3: PERSONALIZED STUDY PLANS                         │
├─────────────────────────────────────────────────────────────┤
│ [Student Selection Dropdown]                                │
│                                                             │
│ [Student Profile] │ [Academic] │ [Well-being]              │
│                                                             │
│ [Recommended Study Method & Times]                          │
│ [Effectiveness Score]                                       │
│                                                             │
│ [Performance Bar Chart]                                     │
│ [Weekly Schedule Bar Chart]                                 │
│                                                             │
│ [Tool 1] [Tool 2] [Tool 3] [Tool 4]                        │
│ (Recommended tools)                                         │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📝 TAB 4: STUDY TRACKER                                    │
├─────────────────────────────────────────────────────────────┤
│ [Study Form]                   │  [Recent Sessions]         │
│  • Date Picker                 │  │ Session History       │
│  • Duration Slider             │  │ Table                 │
│  • Time Selection              │  │                       │
│  • Subject Input               │  │ [Statistics Cards]   │
│  • Distraction Level           │  │ • Total Hours        │
│  • Quiz Score                  │  │ • Avg Score          │
│  • [Submit Button]             │  │ • Session Count      │
│                                │                        │
│ [Recommendations Card]         │                        │
│  - Behavior Profile            │                        │
│  - Optimal Times               │                        │
│  - Study Method                │                        │
│  - Effectiveness               │                        │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📊 TAB 5: PROGRESS ANALYTICS                               │
├─────────────────────────────────────────────────────────────┤
│ [Summary Cards: Sessions | Hours | Avg Score | Best Score] │
│                                                             │
│ [Score Progress Line Chart]  │  [Daily Study Hours]        │
│                                                             │
│ [Time Distribution Pie]   │  [Distraction Level Bar]       │
│                                                             │
│ [Subject Analysis Table]                                    │
│  Subject | Sessions | Hours | Avg Score                    │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔄 Typical Workflow

### First Time Using Dashboard

```
1. EXPLORE DATA (Tab 1)
   ├─ View dataset overview
   ├─ Check for missing values
   ├─ Analyze distributions
   └─ Understand correlations
   
2. RUN CLUSTERING (Tab 2)
   ├─ Configure clustering parameters
   ├─ Select features to use
   ├─ Click "Run Clustering Analysis"
   ├─ View quality metrics
   ├─ Review cluster visualizations
   └─ Click "Save Clustered Data"
   
3. VIEW & CREATE PLANS (Tab 3)
   ├─ Select a student
   ├─ Review their profile
   ├─ Check assigned cluster
   ├─ Read recommended study plan
   ├─ View performance breakdown
   └─ Note recommended tools
```

### Regular Usage

```
DAILY:
  1. Log study session (Tab 4)
  2. Review recommendations
  3. Continue studying

WEEKLY:
  1. Check progress (Tab 5)
  2. Monitor trends
  3. Adjust study plan if needed

MONTHLY:
  1. Rerun clustering if major changes (Tab 2)
  2. Update study plans (Tab 3)
  3. Archive old logs if needed
```

---

## 📊 What Each Tab Shows

### TAB 1: DATA ANALYSIS
**Purpose**: Understand your dataset

**Key Visualizations**:
1. **Study Hours vs Quiz Average** - Correlation with trend line
2. **Grade Distribution** - How many students in each grade
3. **Correlation Heatmap** - Which variables are related
4. **Total Score Distribution** - Overall performance spread
5. **Score by Grade** - Performance varies by grade
6. **Study Hours by Grade** - Study effort by grade
7. **Feature Relationships** - Pairwise feature analysis

**When to Use**: First time setup, understanding your school's data

---

### TAB 2: STUDENT CLUSTERING
**Purpose**: Identify student groups with similar learning patterns

**Key Features**:
- **Algorithm Selection**: Choose between 3 clustering methods
- **Silhouette Scores**: See which algorithm works best
- **PCA Visualization**: 2D view of clusters
- **Cluster Profiles**: Average values for each cluster
- **Student Details**: Individual cluster assignments

**When to Use**: After initial data exploration, when ready to group students

---

### TAB 3: PERSONALIZED STUDY PLANS
**Purpose**: Generate custom study recommendations

**Key Information**:
- **Student Profile**: ID, Name, Cluster, Behavior Type
- **Academic Metrics**: Current scores and grades
- **Well-being**: Stress, sleep, study hours
- **Optimal Study Times**: When to study
- **Session Duration**: How long to study
- **Break Schedule**: When to rest
- **Recommended Tools**: Apps to help
- **Performance Breakdown**: Strengths and weaknesses

**When to Use**: When meeting with students to plan their studies

---

### TAB 4: STUDY TRACKER
**Purpose**: Log actual study sessions and get feedback

**Key Features**:
- **Session Form**: Record date, duration, subject, score
- **Auto-Clustering**: System identifies your study profile
- **Instant Recommendations**: Get personalized advice
- **Session History**: Recent 5-10 sessions displayed
- **Quick Stats**: Total hours, average score

**When to Use**: After each study session, track your behavior

---

### TAB 5: PROGRESS ANALYTICS
**Purpose**: Monitor long-term improvement

**Key Insights**:
- **Total Sessions**: How many times you studied
- **Total Hours**: Cumulative study time
- **Average Score**: Overall performance trend
- **Best Score**: Your highest achievement
- **Score Over Time**: Line chart showing improvement
- **Daily Hours**: How much you study each day
- **Study Time Distribution**: Morning vs afternoon vs evening
- **Subject Performance**: Which subjects need more work

**When to Use**: Weekly/monthly check-ins to track progress

---

## 🎮 Interactive Features

### In All Tabs

**Hover Effects**:
- Hover over charts to see exact values
- Point sizes show in data points

**Download Options**:
```
Click camera icon on any chart to:
  • Download as PNG image
  • Download as SVG vector
  • Open chart in new tab
```

**Sidebar Controls**:
- Adjust clustering parameters in Tab 2
- Select students in Tab 3
- Switch between tabs at top

---

## ⚠️ Common Questions

### Q: I see "No student clusters appearing in Tab 3"
**A**: You need to:
1. Go to Tab 2
2. Configure clustering settings
3. Click "Run Clustering Analysis"
4. Wait for results
5. Click "Save Clustered Data"
6. Now Tab 3 will work

### Q: Study logs not saving
**A**: This can happen if:
- folder lacks write permissions
- study_logs.csv is corrupted
- Try: Delete study_logs.csv and try again

### Q: Charts showing blank/not loading
**A**: 
- Check internet (Plotly uses CDN)
- Refresh page (F5)
- Update packages: `pip install --upgrade plotly`

### Q: Dashboard runs slow
**A**: For large datasets:
- Use feature selection in Tab 2
- Reduce number of clusters
- Try different algorithm (KMeans fastest)

### Q: "Could not load dataset"
**A**: Check:
- CSV exists in project folder
- File name spelling correct
- No permission issues
- CSV not corrupted

---

## 🛑 To Stop the Dashboard

In PowerShell where it's running:
```powershell
Ctrl + C
```

This stops the server cleanly.

---

## 🚀 Performance Tips

### For Faster Loading
```powershell
# Update Streamlit to latest
pip install --upgrade streamlit

# Update Plotly for faster charts
pip install --upgrade plotly
```

### For Large Datasets
- Filter data in Tab 1 before clustering
- Use fewer features in Tab 2
- Archive old logs in study_logs.csv

### For Multiple Users
- Each user runs their own instance
- Data files are shared (CSV-based)
- Perfect for school or study groups

---

## 📁 File Organization After Running

```
study habits project/
├── integrated_dashboard.py          (Main app)
├── module1.py - module4.py         (Original modules)
├── students_with_clusters.csv      (Created after Tab 2)
├── study_logs.csv                  (Created after Tab 4)
├── requirements.txt                (Dependencies)
├── README_INTEGRATED_DASHBOARD.md  (Full docs)
├── QUICK_START_GUIDE.md           (This style)
├── INTEGRATION_SUMMARY.md          (What was integrated)
├── CONFIGURATION_GUIDE.md          (How to customize)
└── This file
```

---

## 🔗 Quick Links (In Documentation)

- **Full Documentation**: README_INTEGRATED_DASHBOARD.md
- **Quick Start**: QUICK_START_GUIDE.md
- **Integration Details**: INTEGRATION_SUMMARY.md
- **Customization**: CONFIGURATION_GUIDE.md
- **This Guide**: RUNNING_INSTRUCTIONS.md

---

## 🎯 Success Checklist

After starting dashboard, verify:
- [ ] Dashboard loads in browser
- [ ] All 5 tabs are visible at top
- [ ] Tab 1 shows charts and data
- [ ] Tab 2 has sidebar controls
- [ ] Colors are consistent
- [ ] Text is readable
- [ ] Charts are interactive
- [ ] No error messages visible

If all ✓, you're ready to use!

---

## 💡 Pro Tips

1. **Bookmark the URL**: `http://localhost:8501`
2. **Keep terminal window open**: Dashboard needs it running
3. **Use multiselect**: In Tab 2, select all features first time
4. **Log regularly**: More logs = better analytics in Tab 5
5. **Check progress**: Weekly review of Tab 5 shows improvement
6. **Share results**: Take screenshots of charts to share with others
7. **Experiment**: Try different clustering parameters to see effects

---

## 🆘 Troubleshooting Flowchart

```
Dashboard won't start?
├─ Did you install requirements? → pip install -r requirements.txt
├─ Is PowerShell in right directory? → cd "d:\Desktop\study habits project"
└─ Port 8501 in use? → streamlit run integrated_dashboard.py --server.port 8502

Tab shows error?
├─ Missing CSV file? → Check file is in project folder
├─ Column not found? → Ensure CSV has correct headers
└─ Date format issue? → Check study_logs.csv format

Charts not showing?
├─ Internet connection? → Charts use CDN
├─ Browser cache? → Ctrl+Shift+Delete to clear
└─ Streamlit cache? → Ctrl+R to rerun

Performance slow?
├─ Large dataset? → Filter in Tab 1 first
├─ Many clusters? → Try 3-5 instead of 10
└─ Too many features? → Unselect unused features in Tab 2
```

---

## 📞 Need More Help?

1. Check QUICK_START_GUIDE.md for overview
2. Check README_INTEGRATED_DASHBOARD.md for features
3. Check CONFIGURATION_GUIDE.md to customize
4. Check INTEGRATION_SUMMARY.md for tech details
5. All four files are in your project folder

---

**You're all set! Start exploring your data!** 🎓

Questions? Check the documentation files. Happy studying! 📚
