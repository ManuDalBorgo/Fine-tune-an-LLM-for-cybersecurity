import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict

# Configuration
INPUT_FILE = "synthetic_lanl_auth.csv"
TRAIN_DAYS = 25 # Train on first 25 days
TEST_DAYS = 5   # Test on last 5 days (where attacks are)

def calculate_time_score(timestamp_sec):
    """
    Simple heuristic: Scores 1.0 if time is 'weird' (e.g. 2am-5am), 0.0 otherwise.
    In prod, use Kernel Density Estimation (KDE) on training timestamps.
    """
    seconds_in_day = timestamp_sec % 86400
    hour = seconds_in_day / 3600
    # If between 1am and 5am -> Anomalous
    if 1 <= hour <= 5:
        return 1.0
    return 0.0

def main():
    print("--- Anomaly Scoring: Probabilistic Baselining ---")
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run 01 script first.")
        return

    df = pd.read_csv(INPUT_FILE)
    
    # 1. Split Train/Test by Time
    split_time = TRAIN_DAYS * 86400
    train_df = df[df["time"] < split_time]
    test_df = df[df["time"] >= split_time].copy()
    
    print(f"Train samples: {len(train_df)}")
    print(f"Test samples: {len(test_df)} (Includes Red Team events)")
    
    # 2. Build Profiles (Training)
    # P(Computer | User)
    user_pc_counts = defaultdict(lambda: defaultdict(int))
    user_total_counts = defaultdict(int)
    
    for _, row in train_df.iterrows():
        u = row['source_user']
        c = row['dest_computer']
        user_pc_counts[u][c] += 1
        user_total_counts[u] += 1
        
    # Convert to probabilities
    # We use a small epsilon for smoothing unseen events
    user_pc_probs = defaultdict(dict)
    for u, pcs in user_pc_counts.items():
        total = user_total_counts[u]
        for c, count in pcs.items():
            user_pc_probs[u][c] = count / total

    print("Baseline profiles built.")

    # 3. Score Test Data
    anomaly_scores = []
    
    for _, row in test_df.iterrows():
        u = row['source_user']
        c = row['dest_computer']
        t = row['time']
        
        # Feature A: Rare Path Score (New computer for user)
        # Low probability = High Anomaly Score
        # If user unseen, assume default low prob
        prob = user_pc_probs.get(u, {}).get(c, 0.0)
        path_score = 1.0 - prob # Simple inversion
        
        # Feature B: Time Score
        time_score = calculate_time_score(t)
        
        # Combined Score (Simple weighted average)
        # "Rare access at 3am is VERY bad"
        final_score = (path_score * 0.7) + (time_score * 0.3)
        anomaly_scores.append(final_score)
        
    test_df['anomaly_score'] = anomaly_scores
    
    # 4. Inspection
    print("\nTop 10 Anomalous Events in Test Set:")
    print(test_df.sort_values(by='anomaly_score', ascending=False).head(10)[['time', 'source_user', 'dest_computer', 'label', 'anomaly_score']])
    
    # Save for next steps
    test_df.to_csv("scored_test_data.csv", index=False)
    print("\nScored test data saved to 'scored_test_data.csv'.")

import os
if __name__ == "__main__":
    main()
