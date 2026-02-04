import pandas as pd
import networkx as nx
import numpy as np

# Configuration
INPUT_FILE = "synthetic_lanl_auth.csv" # Read full data to build daily graphs
SCORED_FILE = "scored_test_data.csv"

def main():
    print("--- Graph Feature Extraction: Lateral Movement Detection ---")
    
    if not os.path.exists(SCORED_FILE):
        print("Please run script 02 first.")
        return

    # Load test data that needs graph features
    test_df = pd.read_csv(SCORED_FILE)
    
    # We will build a graph for the TIME WINDOW of the test set
    # In streaming, you'd update this incrementally or have sliding windows.
    # Here, we build one graph of all Test activity to find the structural anomalies.
    
    G = nx.DiGraph()
    
    print("Building interaction graph (User -> Computer)...")
    edges = []
    for _, row in test_df.iterrows():
        u = row['source_user']
        c = row['dest_computer']
        # Weight could be number oflogins, measuring just existence for now
        edges.append((u, c))
        
    G.add_edges_from(edges)
    
    print(f"Graph stats: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges.")
    
    # 1. Out-Degree Centrality
    # High out-degree for a USER means they are accessing many machines -> Lateral Movement
    out_degrees = dict(G.out_degree())
    
    # 2. PageRank
    # High PageRank for a COMPUTER means it's a critical asset (DC, File Server)
    # Accessing a high PR node might be higher risk
    try:
        pagerank = nx.pagerank(G, alpha=0.85)
    except:
        # Fallback for unconnected graphs or simple demo
        pagerank = {n: 0 for n in G.nodes()}
        
    # 3. Enrich DataFrame
    graph_scores = []
    
    for _, row in test_df.iterrows():
        u = row['source_user']
        c = row['dest_computer']
        
        # Feature: User Fan-out (Normalized)
        u_degree = out_degrees.get(u, 0)
        # Simple normalization (e.g. log scale)
        # If user hits 50 PCs, log(50) ~ 3.9. If user hits 1, log(1)=0
        degree_score = np.log1p(u_degree)
        
        # Feature: Destination Importance
        dest_importance = pagerank.get(c, 0)
        
        # Combined Graph Risk Score
        # "High fan-out user accessing important machine"
        risk_val = degree_score * (1 + dest_importance) 
        graph_scores.append(risk_val)
        
    test_df['graph_risk_score'] = graph_scores
    
    # Normalize graph score to 0-1 roughly for combining later
    max_g = max(graph_scores) if graph_scores else 1
    test_df['graph_risk_score'] /= max_g
    
    # Save enriched
    test_df.to_csv("enriched_test_data.csv", index=False)
    print("Graph features added. top lateral movement suspects:")
    print(test_df.sort_values(by='graph_risk_score', ascending=False).head(5)[['source_user', 'dest_computer', 'graph_risk_score', 'label']])

import os
if __name__ == "__main__":
    main()
