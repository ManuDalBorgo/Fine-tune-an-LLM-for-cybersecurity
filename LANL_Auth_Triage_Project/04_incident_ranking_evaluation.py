import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc, average_precision_score

# Configuration
ENRICHED_FILE = "enriched_test_data.csv"

def main():
    print("--- Evaluation: SOC Triage Metrics ---")
    if not os.path.exists(ENRICHED_FILE):
        print("Please run script 03 first.")
        return

    df = pd.read_csv(ENRICHED_FILE)
    
    # 1. Ensemble Scoring
    # Combine Baseline Anomaly Score + Graph Risk Score
    # Simple averaging or weighted sum. In stats we might learn this via Logistic Regression
    df['final_risk_score'] = (0.6 * df['anomaly_score']) + (0.4 * df['graph_risk_score'])
    
    # 2. Ranking
    # Sort by risk (High Risk at top)
    ranked_df = df.sort_values(by='final_risk_score', ascending=False).reset_index(drop=True)
    
    y_true = ranked_df['label'].values
    y_scores = ranked_df['final_risk_score'].values
    
    # 3. Precision @ K
    # "If the analyst checks the top K alerts, how many are real attacks?"
    ks = [10, 50, 100]
    print("\n>>> Precision @ K Results (Analyst Efficiency)")
    for k in ks:
        top_k = y_true[:k]
        hits = sum(top_k)
        prec_k = hits / k
        print(f"Precision @ {k}: {prec_k:.2f} \t({hits} attacks found in top {k})")
        
    # 4. Global Metrics (PR-AUC, ROC)
    ap = average_precision_score(y_true, y_scores)
    print(f"\nAverage Precision (PR-AUC): {ap:.4f}")
    
    fpr, tpr, thresholds = roc_curve(y_true, y_scores)
    roc_auc = auc(fpr, tpr)
    print(f"ROC AUC: {roc_auc:.4f}")
    
    # 5. Recall at Fixed False Positive Rate (e.g., 1% FPR)
    # Allows usage in a SOC with limited "false alarm" budget
    target_fpr = 0.01
    idx = np.where(fpr <= target_fpr)[0][-1]
    recall_at_low_fp = tpr[idx]
    print(f"Recall at <{target_fpr*100}% FPR: {recall_at_low_fp:.4f}")
    
    # 6. Conclusion
    print("\n--- Summary ---")
    print("This mini-project demonstrated a full Triage AI pipeline:")
    print("1. Ingested time-series logs.")
    print("2. Baselined path probabilities (Model 1).")
    print("3. Extracted graph centrality/degree (Model 2).")
    print("4. Ranked incidents for valid SOC consumption (Precision@K).")

import os
if __name__ == "__main__":
    main()
