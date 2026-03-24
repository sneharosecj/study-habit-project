# 🎴 Quick Reference Card - Integrated Dashboard

## ONE-LINE STARTUP
```powershell
pip install -r requirements.txt && streamlit run integrated_dashboard.py
```

---

## 5 TABS AT A GLANCE

### 📈 TAB 1: DATA ANALYSIS
**What**: Explore your dataset  
**Shows**: 8 visualizations + statistics  
**Do**: Understand patterns in your data

### 🔍 TAB 2: CLUSTERING
**What**: Group similar students  
**Shows**: 3 algorithms, PCA plots, quality scores  
**Do**: Click "Run Clustering" → "Save Clustered Data"

### 📋 TAB 3: STUDY PLANS
**What**: Get personalized recommendations  
**Shows**: Study times, duration, tools, schedule  
**Do**: Select student → view custom plan

### 📝 TAB 4: TRACKER
**What**: Log study sessions  
**Shows**: Form, history, recommendations  
**Do**: Fill form → submit → get instant advice

### 📊 TAB 5: ANALYTICS
**What**: Monitor progress  
**Shows**: Trends, patterns, statistics  
**Do**: Check weekly/monthly improvement

---

## THE 3-STEP WORKFLOW

### Step 1: Understand Data
```
Open Tab 1 → Explore charts → Understand patterns
```

### Step 2: Create Clusters
```
Go Tab 2 → Configure settings → Click "Run Clustering" 
→ Click "Save Clustered Data"
```

### Step 3: Use Insights
```
Tab 3: Create plans | Tab 4: Track sessions | Tab 5: Review trends
```

---

## KEYBOARD SHORTCUTS

| Action | Command |
|--------|---------|
| Run dashboard | `streamlit run integrated_dashboard.py` |
| Stop dashboard | `Ctrl + C` (in terminal) |
| Refresh app | `Ctrl + Shift + R` (in browser) |
| Clear cache | `Ctrl + Shift + Delete` |
| Go to Tab 1 | `Click "📈 Data Analysis"` |
| Go to Tab 2 | `Click "🔍 Clustering"` |
| Go to Tab 3 | `Click "📋 Study Plans"` |
| Go to Tab 4 | `Click "📝 Study Tracker"` |
| Go to Tab 5 | `Click "📊 Progress Analytics"` |

---

## FILE REFERENCE

| File | Purpose | When to Use |
|------|---------|-----------|
| integrated_dashboard.py | Main app | `streamlit run integrated_dashboard.py` |
| requirements.txt | Dependencies | `pip install -r requirements.txt` |
| Total of 8 .md files | Documentation | When you need help |
| .csv files | Data | Automatic saving |

---

## 4 CLUSTER TYPES

| Cluster | Behavior | Best Time | Duration | Tools |
|---------|----------|-----------|----------|-------|
| 0 | High Focus | 8 AM / 2 PM | 25 min | Test platforms |
| 1 | Low Focus | 10 AM / 4 PM | 20 min | Pomodoro timer |
| 2 | Distracted | 7 AM / 7 PM | 15 min | Site blocker |
| 3 | Visual | 9 AM / 3 PM | 30 min | Mind maps |

---

## WHAT'S IN EACH TAB

```
TAB 1                 TAB 2                TAB 3              TAB 4           TAB 5
─────                 ─────                ─────              ─────           ─────
• Data preview        • Sidebar controls   • Student select   • Study form    • Summary stats
• Statistics          • Run clustering     • Profile info     • Logging       • Score chart
• 8 charts            • Quality metrics    • Custom plan      • History       • Hours chart
• Heatmap             • PCA viz (3x)       • Performance      • Recent logs   • Distribution
• Distributions       • Cluster prof       • Weekly schedule  • Stats         • Subject table
• Correlations        • Export data        • Tool recs        • Recommend     • Trends
```

---

## SAMPLE QUESTIONS TO ANSWER

### In Tab 1
"What subjects are correlated?" → Check correlation heatmap  
"How many A/B/C students?" → Check grade distribution

### In Tab 2
"How many clusters?" → Try 3, 4, 5 (check silhouette score)  
"Which algorithm is best?" → Compare scores: KMeans > Agg > DBSCAN

### In Tab 3
"What should I study?" → Check performance breakdown  
"When should I study?" → Check optimal time slots

### In Tab 4
"Did I improve?" → Enter recent quiz score → See recommendation  
"How much should I study?" → See recommended duration

### In Tab 5
"Am I getting better?" → Check score trend line  
"Which subjects are weak?" → Check subject table

---

## COMMON SHORTCUTS

### Get Started in 30 Seconds
```
cd "d:\Desktop\study habits project"
pip install -r requirements.txt
streamlit run integrated_dashboard.py
```

### Just Run It (Already Installed)
```
streamlit run integrated_dashboard.py
```

### Stop It
```
Ctrl + C
```

### Port Already in Use?
```
streamlit run integrated_dashboard.py --server.port 8502
```

---

## TROUBLESHOOTING QUICK FIX

| Problem | Fix |
|---------|-----|
| `pip: command not found` | Reinstall Python, restart terminal |
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `No CSV file found` | Check CSV is in project folder |
| `Tab 3 is empty` | Run Tab 2 clustering first, save data |
| `No charts showing` | Check internet (Plotly uses CDN) |
| `Slow performance` | Use fewer features/clusters in Tab 2 |
| `Port 8501 in use` | Kill process or use `--server.port 8502` |

---

## MUST-READ DOCS

| Need | Read This |
|------|-----------|
| 30-sec setup | RUNNING_INSTRUCTIONS.md |
| Full guide | README_INTEGRATED_DASHBOARD.md |
| Integration details | INTEGRATION_SUMMARY.md |
| How to customize | CONFIGURATION_GUIDE.md |
| Quick overview | QUICK_START_GUIDE.md |

---

## METRICS EXPLAINED

**Silhouette Score** (0-1):
- 0.8-1.0: Perfect clustering
- 0.5-0.8: Good clustering
- 0.0-0.5: Fair clustering
- <0: Bad clustering

**Effectiveness %** (per cluster):
- High Focus: 85%
- Visual: 80%
- Low Focus: 70%
- Distracted: 60%

---

## DAILY USAGE

```
MORNING:
1. Goal setting → Tab 3 (Review study plan)

DURING STUDY:
2. Follow recommendation → Tab 4 (Log session if completed)

WEEKLY:
3. Progress check → Tab 5 (Review trends)

MONTHLY:
4. Re-cluster → Tab 2 (Rerun if major changes)
```

---

## WHAT GETS SAVED

| File | Created By | When |
|------|-----------|------|
| students_with_clusters.csv | Tab 2 | After "Save Clustered Data" |
| study_logs.csv | Tab 4 | After logging session |

Both are automatic - no action needed!

---

## COMMANDS CHEATSHEET

```powershell
# Install dependencies
pip install -r requirements.txt

# Check installed packages
pip list | grep streamlit

# Run dashboard
streamlit run integrated_dashboard.py

# Run on different port
streamlit run integrated_dashboard.py --server.port 8502

# Stop dashboard
Ctrl + C

# Update streamlit
pip install --upgrade streamlit

# Clear cache
streamlit cache clear
```

---

## TIPS & TRICKS

💡 **Performance**: Use feature selection in Tab 2  
💡 **Customization**: Edit CLUSTER_BEHAVIOR in code  
💡 **Sharing**: Take screenshots of Tab 5 charts  
💡 **Backup**: Copy integrated_dashboard.py before editing  
💡 **Testing**: Try with fewer clusters (3) first  
💡 **Improving**: Log sessions consistently in Tab 4  

---

## LINKS

- **Dashboard URL**: http://localhost:8501
- **Streamlit Docs**: https://docs.streamlit.io
- **Scikit-learn**: https://scikit-learn.org
- **Plotly Charts**: https://plotly.com/python

---

## SUCCESS CHECKLIST

After starting dashboard:
- [ ] Page loads (you see 5 tabs)
- [ ] Tab 1 shows charts
- [ ] Tab 2 has sidebar controls
- [ ] Tab 3 has student dropdown
- [ ] Tab 4 has form
- [ ] Tab 5 shows "No data yet" (normal first time)

If all ✓: **You're good to go!** 🎉

---

## ⏱️ TIME ESTIMATES

| Task | Time |
|------|------|
| Installation | 2 min |
| First run | 30 sec |
| Exploring Tab 1 | 5 min |
| Running Tab 2 | 5-10 min |
| Creating plan (Tab 3) | 2 min |
| Logging session (Tab 4) | 1 min |
| Reviewing analytics (Tab 5) | 3 min |
| **Total first session** | **20-30 min** |

---

## SHEET REFERENCE

Keep this handy! Bookmark it. Print it. Share it.

```
Quick Start: streamlit run integrated_dashboard.py
5 Tabs: Analysis | Clustering | Plans | Tracker | Analytics
3 Steps: Explore → Cluster → Use insights
Get Help: Read .md files in project folder
```

---

**Print this card and keep it by your desk!** 📋

For detailed guides, see the 6 documentation files (.md) in your project folder.

Happy studying! 🎓
