#!/bin/bash
# Script to download LANL Cyber1 Data
# Generated presigned URL (valid for limited time)

# Base URL with Access Token
BASE_URL="https://csr.lanl.gov/data-fence/1769645088/11x6BIO4AETt1y3_y5OxeaRjFlY=/cyber1"

echo "Starting download of LANL dataset (~10.5 GB total)..."
echo "These files are large. The script uses 'curl -C -' to allow resuming if interrupted."

# 1. Auth Logs (7.2 GB)
echo "[1/3] Downloading auth.txt.gz..."
curl -C - -O "${BASE_URL}/auth.txt.gz"

# 2. Process Logs (2.2 GB)
echo "[2/3] Downloading proc.txt.gz..."
curl -C - -O "${BASE_URL}/proc.txt.gz"

# 3. Flow Logs (1.1 GB)
echo "[3/3] Downloading flows.txt.gz..."
curl -C - -O "${BASE_URL}/flows.txt.gz"

echo "All downloads complete."
