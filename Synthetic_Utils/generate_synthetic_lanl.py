import pandas as pd
import numpy as np
import os
import random

# Configuration
OUTPUT_FILE = "../processed_lanl_auth.csv" # Write to parent dir so other scripts can use it if chosen
NUM_USERS = 50
NUM_COMPUTERS = 100
NUM_DAYS = 30
EVENTS_PER_DAY = 500
RED_TEAM_EVENTS = 50 # Number of anomalies to inject

def generate_synthetic_data():
    """
    Generates a synthetic dataset mimicking the LANL Cyber1 auth.txt format.
    Fields: time, source_user, dest_user, source_computer, dest_computer, 
            auth_type, logon_type, auth_orientation, success
    """
    print(f"Generating synthetic LANL auth data ({NUM_DAYS} days)...")
    
    users = [f"U{i}" for i in range(1, NUM_USERS+1)]
    computers = [f"C{i}" for i in range(1, NUM_COMPUTERS+1)]
    
    data = []
    
    # 1. Generate Normal Traffic (Baseline)
    # Users tend to log into the same few computers (affinity)
    user_affinity = {u: random.choices(computers, k=3) for u in users}
    
    for day in range(NUM_DAYS):
        # Time in seconds (day * 86400)
        start_time = day * 86400
        
        for _ in range(EVENTS_PER_DAY):
            # Normal user behavior
            u = random.choice(users)
            # 80% chance to pick from affinity, 20% random
            if random.random() < 0.8:
                c = random.choice(user_affinity[u])
            else:
                c = random.choice(computers)
            
            # Timestamp: mostly work hours (28800 = 8am, 61200 = 5pm)
            time_offset = int(np.random.normal(43200, 10000)) #Centered noon
            time_offset = max(0, min(86399, time_offset))
            timestamp = start_time + time_offset
            
            data.append({
                "time": timestamp,
                "source_user": u,
                "dest_user": u, # usually self
                "source_computer": c, # mocking src=dst for simplicity often seen in local logs
                "dest_computer": c,
                "auth_type": "Kerberos",
                "logon_type": "Network",
                "auth_orientation": "LogOn",
                "success": "Success",
                "label": 0 # 0 = Normal
            })

    # 2. Inject Red Team Activity (Anomalies)
    # Lateral Movement: One compromised user accessing MANY computers rapidly
    # or accessing computers they never touch
    print("Injecting Red Team anomalies...")
    compromised_user = "U_COMPROMISED"
    
    # Inject in the last 5 days (Test set)
    attack_days = range(NUM_DAYS - 5, NUM_DAYS)
    
    for day in attack_days:
        start_time = day * 86400 + 10000 # 2:46 AM (unusual time)
        
        for i in range(10): # Rapid fire
            target_c = random.choice(computers)
            timestamp = start_time + i * 5 # every 5 seconds
            
            data.append({
                "time": timestamp,
                "source_user": compromised_user,
                "dest_user": compromised_user,
                "source_computer": "C_ATTACKER",
                "dest_computer": target_c,
                "auth_type": "?",
                "logon_type": "Network",
                "auth_orientation": "LogOn",
                "success": "Success", # Successful breach
                "label": 1 # 1 = Anomaly / Red Team
            })

    # Create DataFrame
    df = pd.DataFrame(data)
    df = df.sort_values(by="time").reset_index(drop=True)
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Data saved to {OUTPUT_FILE}. Shape: {df.shape}")
    print("Last 5 days contain 'Red Team' labels (label=1).")

if __name__ == "__main__":
    generate_synthetic_data()
