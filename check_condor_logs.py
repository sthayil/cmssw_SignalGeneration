import os
import subprocess
import glob
import sys

# Get the directory as input from the user
if len(sys.argv) != 2:
    print("Usage: python check_condor_logs.py <base directory>")
    sys.exit(1)

base_dir = sys.argv[1]
log_dir = os.path.join(base_dir, "logs_from_condor")

# Ensure the log directory exists
if not os.path.exists(log_dir):
    print(f"Directory {log_dir} does not exist.")
    sys.exit(1)

log_pattern = os.path.join(log_dir, "*.log")

# Get all log files in the directory that match the pattern
log_files = glob.glob(log_pattern)

if not log_files:
    print(f"No log files found in {log_dir}")
    sys.exit(1)

# Function to check the last line for exit codes
def check_last_line(log_file):
    try:
        with open(log_file, 'r') as file:
            lines = file.readlines()
            if not lines:
                return

            last_line = lines[-2].strip()

            if "Job terminated of its own accord" in last_line:
                # Extract the exit code from the last line
                parts = last_line.split()
                if "exit-code" in parts:
                    try:
                        # Extract and clean the exit code part
                        exit_code_str = parts[parts.index("exit-code") + 1]
                        exit_code = int(exit_code_str.strip('.'))  # Remove any trailing periods
                        if exit_code in [1, 2]:
                            print(f"Log file: {log_file}")
                            print(f"Last line: {last_line}")
                    except ValueError:
                        print(f"Invalid exit code format in {log_file}: '{exit_code_str}'")

    except Exception as e:
        print(f"Error reading {log_file}: {e}")

# Iterate over each log file and run the condor_wait command
for log_file in log_files:
    try:
        # Run the condor_wait command for each log file
        command = ["condor_wait", log_file]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Check the output of the command
        output = result.stdout.strip()

        # Print the output only if it's not "All jobs done."
        if output != "All jobs done.":
            print(f"Output for {log_file}:")
            print(output)

        # Check the last line of the log file for exit codes
        check_last_line(log_file)
        
    except Exception as e:
        print(f"Error processing {log_file}: {e}")
