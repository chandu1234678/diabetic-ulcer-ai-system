"""
Monitor the training output log file.
"""
import os
import time
from pathlib import Path

log_file = "training.log"
last_lines_count = 0

print(f"Monitoring {log_file}...")
print("Waiting for training to start\n")

while True:
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            lines = f.readlines()
        
        if len(lines) > last_lines_count:
            # Print new lines
            for line in lines[last_lines_count:]:
                print(line.rstrip())
            last_lines_count = len(lines)
    
    time.sleep(5)  # Check every 5 seconds
