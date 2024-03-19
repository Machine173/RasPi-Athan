import os
import datetime


#This delets log files older than 3 days to prevent storage clog. 
#Make sure to run this script at regular intervals using a cron job (on Linux/macOS) or Task Scheduler (on Windows)
# Example: 0 0 * * * /usr/bin/python3 /path/to/your/garbageCollector.py


def clean_old_logs(log_directory, days=3):
    # Calculate the cutoff time; files older than this will be deleted
    cutoff = datetime.datetime.now() - datetime.timedelta(days=days)

    # Check each file in the specified log directory
    for filename in os.listdir(log_directory):
        file_path = os.path.join(log_directory, filename)

        # Skip directories
        if os.path.isdir(file_path):
            continue

        # Get the last modification time of the file
        file_mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))

        # Compare the file's last modification time with the cutoff time
        if file_mod_time < cutoff:
            try:
                os.remove(file_path)
                print(f"Deleted old log file: {filename}")
            except Exception as e:
                print(f"Error deleting file {filename}: {e}")

# Example usage
log_directory = os.path.expanduser("~/Documents/logs")
clean_old_logs(log_directory, days=3)
