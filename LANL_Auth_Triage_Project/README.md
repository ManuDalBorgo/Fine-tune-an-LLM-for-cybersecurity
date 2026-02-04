# LANL Authentication Triage Project

This project implements a machine learning pipeline for detecting **Lateral Movement** and anomalous authentication events using the Los Alamos National Laboratory (LANL) Comprehensive Cyber Events dataset.

The goal is to simulate a "Triage AI" that filters millions of raw logs into a prioritized list of high-risk alerts for a Security Operations Center (SOC) analyst.

## 📂 Project Structure

- **`01_data_ingestion_preprocessing.py`**: 
  - Ingests raw `auth.txt.gz` logs.
  - Cleans data (handling missing values, formatting).
  - Prepares the dataset for analysis.

- **`02_anomaly_scoring_baselining.py`**: 
  - Builds probabilistic baselines ($P(Computer | User)$) using training data.
  - Calculates anomaly scores based on rare paths and time-of-day heuristics.

- **`03_graph_features_lateral_movement.py`**: 
  - Constructs a NetworkX graph of User-Computer interactions.
  - Extracts graph features:
    - **Out-Degree**: Detects users accessing many unique machines (fan-out/lateral movement).
    - **PageRank**: Identifies connections to critical infrastructure.

- **`04_incident_ranking_evaluation.py`**: 
  - Ensembles the Anomaly Score (from step 02) and Graph Risk Score (from step 03).
  - Ranks incidents by final risk score.
  - Evaluates performance using **Precision@K** to measure SOC efficiency.

## 📂 Data Setup (Important)

**Note:** The raw data files are **not** included in this repository due to their size (>3GB).

### Automatic Download
The easiest way to get the data is to run the included script, which attempts to fetch from the LANL mirrors:
```bash
./download_real_data.sh
```

### Manual Download
If the script fails (link expiry), download the following files manually from the [LANL Cyber1 Data Source](https://csr.lanl.gov/data/cyber1/):
1.  `auth.txt.gz` (Authentication Logs)
2.  `proc.txt.gz` (Process Logs)
3.  `flows.txt.gz` (Flow Logs)

**Place these files directly into the `LANL_Auth_Triage_Project/` folder.**

## 🚀 Usage

1.  **Download Data**: (See above).
2.  **Run Pipeline**: Execute the scripts in order:
    ```bash
    python 01_data_ingestion_preprocessing.py
    python 02_anomaly_scoring_baselining.py
    python 03_graph_features_lateral_movement.py
    python 04_incident_ranking_evaluation.py
    ```

## 📊 Methodology

The pipeline uses a multi-stage approach to filter noise:
1.  **Probabilistic Baselining**: fast filtering of "normal" behavior.
2.  **Graph Analysis**: structural context for detecting lateral movement campaigns.
3.  **Ensemble Ranking**: prioritizing strictly the top K anomalies for human review.
