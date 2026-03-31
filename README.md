# 📚 StudyTrack AI – Student Study Behavior Analysis

StudyTrack AI is a machine learning-based application that analyzes student study habits, clusters students based on behavior, predicts performance trends, and generates personalized study recommendations.

🔐 Secure Coding Vulnerability Lab

An interactive security learning lab designed to demonstrate common web application vulnerabilities and their secure coding practices.
This project helps developers and students understand how attacks work and how to prevent them using secure patterns.

📌 Project Overview

The Secure Coding Vulnerability Lab simulates real-world security flaws and demonstrates:

Vulnerable implementation
Attack patterns
Secure coding solutions
Best practices

The application is divided into multiple modules, each focusing on a specific vulnerability type.

🧪 Features
Interactive vulnerability demonstrations
Secure coding examples
Modular architecture
Easy to extend with new vulnerabilities
Educational security testing environment

# 🏗️ System Architecture

The system follows a modular pipeline:

```
Student Study Logs
        ↓
Module 1 – Data Collection & Preprocessing
        ↓
Module 2 – Study Behavior Clustering
        ↓
Module 3 – Performance Analysis
        ↓
Module 4 – Recommendation Engine
        ↓
Interactive Dashboard Output
```

### Architecture Diagram

(Add your architecture image in repo)

```
![System Architecture](images/system_architecture.png)
```

---

# 🧩 Module Overview

| Module | Focus                | Description                                          | Output                |
| ------ | -------------------- | ---------------------------------------------------- | --------------------- |
| M1     | Data Collection      | Collects student study logs and preprocesses dataset | Cleaned dataset       |
| M2     | Clustering           | Groups students based on study behavior              | Clustered students    |
| M3     | Performance Analysis | Evaluates performance trends and risk levels         | Performance insights  |
| M4     | Recommendation       | Generates personalized study plans                   | Study recommendations |

---

# 📊 Module Outputs

## 🔹 Module 1 – Data Collection & Preprocessing

**Description:**
This module loads the dataset, handles missing values, normalizes features, and prepares data for clustering.

**Output:**

* Clean dataset
* Preprocessed features

```
![Module 1 Output](images/module1_output.png)
```

---

## 🔹 Module 2 – Study Behavior Clustering

**Description:**
Applies clustering algorithms (K-Means/DBSCAN) to group students based on study habits like study hours and engagement.

**Output:**

* Cluster labels
* Cluster visualization
* Grouped students

```
![Module 2 Output](images/module2_output.png)
```

---

## 🔹 Module 3 – Performance Analysis

**Description:**
Analyzes clusters and identifies performance levels such as high-performing, average, and at-risk students.

**Output:**

* Performance charts
* Risk level classification
* Summary statistics

```
![Module 3 Output](images/module3_output.png)
```

---

## 🔹 Module 4 – Recommendation Engine

**Description:**
Generates personalized recommendations based on cluster behavior and performance insights.

**Output:**

* Recommended study hours
* Personalized learning strategies
* Improvement suggestions

```
![Module 4 Output](images/module4_output.png)
```

---

# 📈 Final Dashboard

This section displays integrated results from all modules including clusters, performance insights, and recommendations.

```
![Final Dashboard](images/final_dashboard.png)
```

---

# 🏗️ Project Structure

```
├── module1.py
├── module2.py
├── module3.py
├── module4.py
├── studytrackai.py
├── students_with_clusters.csv
├── study_logs.csv
├── styles.css
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### Clone Repository

```
git clone https://github.com/your-username/repository-name.git
cd repository-name
```

### Install Dependencies

```
pip install -r requirements.txt
```

### Run Project

```
streamlit run studytrackai.py
```

---

# 🎯 Objectives

* Analyze student study habits
* Cluster students based on behavior
* Predict academic performance
* Generate personalized recommendations
* Visualize learning insights

---

# 👩‍💻 Author

Sneha
StudyTrack AI Project
