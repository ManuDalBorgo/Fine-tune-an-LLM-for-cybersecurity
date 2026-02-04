import pandas as pd
import numpy as np
import os
import gzip
import shutil

# Configuration
REAL_DATA_PATH = "auth.txt.gz"
OUTPUT_FILE = "processed_lanl_auth.csv"
SAMPLE_SIZE = 1000000 # Sample 1M rows for rapid iteration (remove this limit for full run)

def process_real_data():
    """
    Parses the real LANL 'auth.txt.gz' file.
    Original Format: time, src_user@dom, dst_user@dom, src_comp, dst_comp, auth_type, logon_type, auth_orient, success
    """
    print(f"Processing real LANL data from {REAL_DATA_PATH}...")
    
    # Check if file exists (it is likely still downloading, so we handle partials or wait)
    if not os.path.exists(REAL_DATA_PATH):
        print(f"Error: {REAL_DATA_PATH} not found. Please wait for download_real_data.sh to finish.")
        return

    # Columns based on LANL documentation
    columns = [
        "time", "source_user", "dest_user", "source_computer", "dest_computer",
        "auth_type", "logon_type", "auth_orientation", "success"
    ]
    
    # Read in chunks or specific rows to likely get valid data even if gzipped partial
    # We'll read the first N rows
    print(f"Reading first {SAMPLE_SIZE} rows...")
    
    try:
        # Use 'error_bad_lines' or 'on_bad_lines' depending on pandas version, 
        # but standard CSV read usually works for this dataset.
        df = pd.read_csv(
            REAL_DATA_PATH, 
            compression='gzip', 
            names=columns, 
            header=None,
            nrows=SAMPLE_SIZE,
            quotechar='"'  # Just in case
        )
        
        # Preprocessing
        # 1. Clean '?' values -> NaN or "Unknown"
        df.replace('?', 'Unknown', inplace=True)
        
        # 2. Map label (Red Team events are in a separate file, so we initially label 0)
        # Note: In the real LANL dataset, "redteam.txt" contains the labels.
        # For this "Triage" exercise, if we don't parse redteam.txt, we treat 
        # the anomaly scoring as purely unsupervised.
        # We will add a placeholder for labels.
        df['label'] = 0 
        
        # 3. Specific LANL Cleaning
        # Users often have 'User123@DOM1'. We might want just 'User123' if domain is mostly constant.
        # But for now, we leave as is for fidelity.
        
        print("Data Loaded. Head:")
        print(df.head())
        
        # 4. Check for Red Team file to label known bads
        RED_TEAM_PATH = "redteam.txt.gz"
        if os.path.exists(RED_TEAM_PATH):
            print("Loading Red Team labels...")
            # format: time,user@domain,source computer,destination computer
            red_df = pd.read_csv(RED_TEAM_PATH, compression='gzip', header=None, names=["time", "user", "src_comp", "dst_comp"])
            
            # Create a set for fast lookup: (time, src_comp, dst_comp) -> Simplistic matching
            # Exact matching might be tricky due to time resolution, but let's try exact first.
            red_events = set(zip(red_df.time, red_df.src_comp, red_df.dst_comp))
            
            def check_label(row):
                if (row.time, row.source_computer, row.dest_computer) in red_events:
                    return 1
                return 0
            
            df['label'] = df.apply(check_label, axis=1)
            print(f"Red Team events found in sample: {df['label'].sum()}")

        # Save processed chunk
        df.to_csv(OUTPUT_FILE, index=False)
        print(f"Processed data saved to {OUTPUT_FILE}")

    except Exception as e:
        print(f"Failed to read data: {e}")
        print("Note: If the download is still in progress, gzip decompression will fail.")

def main():
    if os.path.exists(REAL_DATA_PATH):
        process_real_data()
    else:
        print(f"Real data {REAL_DATA_PATH} not found.")
        print("Falling back to synthetic generation for demonstration?")
        print("... No, user requested REAL data. Aborting synthesis.")
        print("Please ensure download_real_data.sh completes.")

if __name__ == "__main__":
    main()
