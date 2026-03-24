# 📊 Integrated Student Analytics & Study Dashboard

## Overview

This is a comprehensive integrated dashboard that combines all four modules into a single, unified Streamlit application. It provides complete student performance analysis, clustering, personalized study planning, and behavior tracking capabilities.

## Features

### 🔸 Tab 1: Data Analysis
- **Dataset Overview**: View shape, columns, and data types
- **Missing Values Analysis**: Identify and handle missing data
- **Statistical Summary**: Descriptive statistics for all numeric columns
- **Visualizations**:
  - Scatter plot: Study Hours vs Quiz Average (with trend line)
  - Correlation Heatmap
  - Grade Distribution (Donut chart)
  - Total Score Distribution (Histogram)
  - Grade vs Total Score (Box plot)
  - Study Hours by Grade
  - Key Feature Relationships

### 🔹 Tab 2: Student Clustering
- **Multiple Clustering Algorithms**:
  - K-Means Clustering
  - Hierarchical Agglomerative Clustering
  - DBSCAN Clustering
- **PCA Visualization**: 2D visualization of clusters
- **Quality Metrics**: Silhouette scores for each algorithm
- **Student-level Analysis**: Individual cluster membership and feature profiles
- **Cluster Profiles**: Mean feature values per cluster
- **Data Export**: Download and save clustered data

### 🔺 Tab 3: Personalized Study Plans
- **Student Selection**: Choose any student from the dataset
- **Behavior Classification**: Automatic assignment to study behavior type:
  - High Focus Learners
  - Low Focus Learners
  - Distracted Learners
  - Visual Learners
- **Customized Study Plans**:
  - Optimal study time slots
  - Recommended session duration
  - Break schedules
  - Expected effectiveness percentage
- **Performance Breakdown**: Visualize scores across components
- **Weekly Schedule**: Recommended study hours per day
- **Tool Recommendations**: Suggested tools based on learning style

### 📝 Tab 4: Study Tracker
- **Session Logging**: Record study sessions with:
  - Date and time
  - Duration and time of day
  - Subject studied
  - Distraction level
  - Quiz score
- **Automatic Clustering**: Predict learning profile based on performance
- **Real-time Recommendations**: Get personalized suggestions immediately
- **Session History**: View recent study sessions
- **Study Statistics**: Total hours, average score, session count

### 📊 Tab 5: Progress Analytics
- **Performance Metrics**:
  - Total study sessions
  - Total study hours
  - Average quiz score
  - Best score achieved
- **Progress Visualizations**:
  - Quiz score trend over time
  - Daily study hours
  - Study sessions by time of day
  - Distraction level distribution
- **Subject Analysis**: Per-subject statistics and performance

## Installation

### Prerequisites
- Python 3.8 or higher
- pip or conda

### Required Libraries
```bash
pip install streamlit pandas numpy scikit-learn plotly
```

### Complete Setup
```bash
# Navigate to project directory
cd "d:\Desktop\study habits project"

# Install all dependencies
pip install streamlit pandas numpy scikit-learn plotly

# Run the integrated dashboard
streamlit run integrated_dashboard.py
```

## Data Files

The dashboard expects the following CSV files in the project directory:

1. **Students Performance Dataset.csv** (or D:\Desktop\app\Students Performance Dataset.csv)
   - Main dataset with student performance metrics
   - Required columns: Student_ID, First_Name, Last_Name, Grade, Study_Hours_per_Week, 
     Quizzes_Avg, Total_Score, Attendance (%), Midterm_Score, Final_Score, 
     Assignments_Avg, Participation_Score, Projects_Score, Stress_Level (1-10), 
     Sleep_Hours_per_Night

2. **students_with_clusters.csv** (auto-generated)
   - Created after running clustering analysis
   - Contains cluster assignments from all three algorithms

3. **study_logs.csv** (auto-generated)
   - Created when logging study sessions
   - Contains tracking data for progress analytics

## Workflow

### First-Time Setup
1. Open the dashboard: `streamlit run integrated_dashboard.py`
2. Go to **Tab 1: Data Analysis** to explore the dataset
3. Go to **Tab 2: Student Clustering** to run clustering analysis
4. Configure clustering parameters in the sidebar
5. Click "Run Clustering Analysis"
6. Click "Save Clustered Data" to create students_with_clusters.csv

### Using the Dashboard
1. **View Analytics** - Tab 1: Analyze student performance data
2. **Run Clustering** - Tab 2: Generate student clusters
3. **Plan Studies** - Tab 3: Select students for personalized plans
4. **Log Sessions** - Tab 4: Track your study behavior
5. **Monitor Progress** - Tab 5: View analytics and progress

## Cluster Types

The system identifies four distinct student clusters:

| Cluster | Behavior Type | Characteristics | Recommendations |
|---------|---------------|-----------------|-----------------|
| 0 | High Focus | Consistent, disciplined | Deep work sessions (25 min), Mock tests |
| 1 | Low Focus | Inconsistent attention | Short sessions (20 min), Pomodoro timer |
| 2 | Distracted | Environmental sensitivity | Very short sessions (15 min), Site blockers |
| 3 | Visual | Spatial learners | Longer sessions (30 min), Mind maps |

## Study Parameters by Cluster

Each cluster has optimized study parameters:
- **Optimal time slots**: When to study based on performance patterns
- **Session duration**: Ideal focus period length
- **Break schedule**: When and how long to rest
- **Effectiveness score**: Expected improvement potential

## Sidebar Controls

### Clustering Sidebar (Tab 2)
- **Number of clusters**: 2-10 (default: 4)
- **DBSCAN eps**: 0.1-5.0 (default: 0.5)
- **DBSCAN min samples**: 2-20 (default: 5)
- **Feature selection**: Choose which features to use for clustering

### Student Selection (Tab 3 & 4)
- **Student dropdown**: Select from available students
- **Form inputs**: Log study sessions with details

## Output & Reports

### Generated Files
- **students_with_clusters.csv**: Contains all students with cluster assignments
- **study_logs.csv**: Contains all logged study sessions

### Downloadable Data
- Clustered datasets (CSV format)
- Charts can be saved as images (use Plotly's download button)
- Analysis reports (screenshot-friendly visualizations)

## Customization

### Modifying Clusters
To change cluster behavior mappings, edit these dictionaries in the code:
- `CLUSTER_BEHAVIOR`: Change cluster names/descriptions
- `CLUSTER_STUDY_PARAMS`: Adjust study times, duration, breaks, effectiveness
- `BEHAVIOR_TOOLS`: Add or change recommended tools

### Adding Features
To include additional features in clustering:
1. Ensure columns exist in your CSV
2. Add to `DEFAULT_FEATURES` list in Tab 2
3. Rerun clustering analysis

## Troubleshooting

### "Could not load Students Performance Dataset.csv"
- Ensure file exists in project directory or D:\Desktop\app\
- Check file name spelling (case-sensitive on some systems)

### No clusters appear after clicking "Run Clustering"
- Ensure students_with_clusters.csv exists
- Run clustering in Tab 2 first and save the results
- Check that CSV has at least one row with cluster assignments

### Study logs not saving
- Check write permissions for the project directory
- Ensure study_logs.csv is not corrupted
- Delete study_logs.csv and restart to recreate it

### Charts not displaying
- Check internet connection (Plotly requires CDN)
- Update Plotly: `pip install --upgrade plotly`
- Try a different browser if using Streamlit Cloud

## Performance Tips

- **Large datasets**: Clustering may be slow on 10,000+ students. Consider filtering data.
- **Many features**: Use feature selection in Tab 2 sidebar to reduce computation time
- **Real-time tracking**: Study logs will accumulate over time. Archive old logs periodically.

## File Structure

```
study habits project/
├── integrated_dashboard.py      # Main dashboard application
├── module1.py                   # Data Analysis (original)
├── module2.py                   # Clustering (original)
├── module3.py                   # Study Plans (original)
├── module4.py                   # Study Tracker (original)
├── Students Performance Dataset.csv
├── students_with_clusters.csv   # Generated after clustering
├── study_logs.csv              # Generated after tracking
└── README.md                    # This file
```

## Usage Examples

### Example 1: Student Performance Analysis
1. Open Tab 1 to explore the dataset
2. Check correlation heatmap to find related metrics
3. Identify high/low performers by grade

### Example 2: Identifying Student Clusters
1. Go to Tab 2
2. Adjust clustering parameters (try different numbers of clusters)
3. Compare silhouette scores for best clustering
4. Save the clustered data

### Example 3: Creating Study Plans
1. With clustered data saved, go to Tab 3
2. Select a student from dropdown
3. Review recommended study plan
4. Check performance breakdown and weekly schedule

### Example 4: Tracking Progress
1. Log study sessions in Tab 4
2. Monitor recommendations update based on performance
3. View long-term trends in Tab 5
4. Analyze subject-wise performance

## API & Integration

This dashboard is built with:
- **Streamlit**: Interactive web framework
- **Pandas**: Data manipulation
- **Scikit-learn**: Machine learning algorithms
- **Plotly**: Interactive visualizations

All data is stored in CSV format for easy integration with other tools.

## Support & Contribution

For issues or improvements:
1. Check troubleshooting section above
2. Review data format requirements
3. Ensure all CSV files are properly formatted
4. Test with sample data first

## License

This project is provided as-is for educational purposes.

---

**Last Updated**: March 2026
**Version**: 1.0
**Status**: Production Ready
