#!/bin/bash
cd "/Applications/My Apps/Bid Opt App Aug 17, 2025"

echo "BidOptimizer Starting..."

# Function to kill processes using port 8501
kill_port_processes() {
    local pids=$(lsof -t -i:8501 2>/dev/null)
    if [ -n "$pids" ]; then
        echo "Killing processes using port 8501: $pids"
        kill -TERM $pids 2>/dev/null
        sleep 2
        # Force kill if still running
        pids=$(lsof -t -i:8501 2>/dev/null)
        if [ -n "$pids" ]; then
            echo "Force killing remaining processes: $pids"
            kill -9 $pids 2>/dev/null
        fi
    fi
}

# Function to kill streamlit processes
kill_streamlit_processes() {
    pkill -f "streamlit run"
    pkill -f "streamlit"
    sleep 1
}

# Check if already running
if lsof -i:8501 >/dev/null 2>&1; then
    echo "BidOptimizer is already running on port 8501"
    echo "Stopping existing instance..."
    kill_port_processes
    kill_streamlit_processes
    sleep 2
fi

# Verify port is free
for i in {1..5}; do
    if ! lsof -i:8501 >/dev/null 2>&1; then
        break
    fi
    echo "Waiting for port 8501 to be free... (attempt $i/5)"
    sleep 1
done

# Final check
if lsof -i:8501 >/dev/null 2>&1; then
    echo "ERROR: Port 8501 is still in use. Cannot start BidOptimizer."
    echo "Please check running processes and try again."
    read -p "Press Enter to close..."
    exit 1
fi

echo "Starting BidOptimizer..."
streamlit run app/main.py

# Minimize terminal window after launch (optional)
osascript -e 'tell application "System Events" to set visible of application process "Terminal" to false' 2>/dev/null || true
