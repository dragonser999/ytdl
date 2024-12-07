#!/bin/bash

# Install FFmpeg
sudo apt install -y ffmpeg

# Exit script on error
set -e

# Function to handle cleanup
cleanup() {
    echo "Stopping processes..."
    kill $APP_PID || true
}
trap cleanup EXIT

# Step 1: Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Step 2: Run the Python application
echo "Starting the Python application..."
python3 app.py &

# Save the PID of the Python application
APP_PID=$!

# Step 3: Start Serveo tunnel with the subdomain "raganorkdownloader"
echo "Starting Serveo tunnel..."
ssh -R getsongragnork.serveo.net:80:localhost:5000 serveo.net &

# Wait for processes to run
echo "Application and Serveo tunnel are running. Access it at: https://getsongragnork.serveo.net"
echo "Press Ctrl+C to stop."
wait
