import json
import logging
import os
from datetime import datetime, timedelta
from prayTimes import PrayTimes


# Setup logging
current_file_name = os.path.splitext(os.path.basename(__file__))[0]
today_date = datetime.datetime.now().strftime('%Y-%m-%d')
log_directory = os.path.expanduser("~/Documents/logs")
log_file_name = f"{current_file_name}-{today_date}.log"
log_file_path = os.path.join(log_directory, log_file_name)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    filename=log_file_path,
    filemode='a'  # Append mode
)

# Set Calculation Method
# 'MWL' Muslim World League
# 'ISNA' Islamic Society of North America
# 'Egypt' Egyptian General Authority of Survey
# 'Makkah' Umm Al-Qura University
# 'Karachi' University of Islamic Sciences
# 'Tehran' Institute of Geophysics, UoT
# 'Jafari' Shia Ithna Ashri, Leva Institute, Qum
pt = PrayTimes('ISNA')

# Set location and timezone
latitude = 0
longitude = 0
elevation = 0 # Elevation with respect to surrounding areas in meters.
timezone = 0  # Adjust for your timezone

# Manually adjust for DST if necessary. Uncomment the next line if DST is in effect.
timezone += 1


def dailyTimesPath():
    # Get the directory of the current script
    dir_path = os.path.dirname(os.path.abspath(__file__))

    # Define the path to dailyTimes.json relative to the current script's directory
    file_path = os.path.join(dir_path, 'dailyTimes.json')

    # Check if the file exists
    if not os.path.exists(file_path):
        # If the file doesn't exist, create it
        with open(file_path, 'w') as file:
            # Optionally, initialize the file with an empty dictionary or some default content
            json.dump({}, file)
        print("dailyTimes.json has been created.")

    # If the file exists or has been created, return its path for further use
    return file_path

def athanTimesCreator():
    today = datetime.now()
    date_tuple = (today.year, today.month, today.day)
    prayer_times = pt.getTimes(date_tuple, (latitude, longitude, elevation), timezone)
    
    # Calculate and log existing prayer times
    for prayer in ['imsak', 'fajr', 'dhuhr', 'asr', 'maghrib', 'isha']:
        if prayer in prayer_times:
            logging.info(f"{prayer}: {prayer_times[prayer]}")
    
    # Calculate suhoor time as one hour before imsak and add it to the prayer_times
    if 'imsak' in prayer_times:
        imsak_time_str = prayer_times['imsak']
        imsak_time = datetime.strptime(imsak_time_str, '%H:%M')
        suhoor_time = imsak_time - timedelta(hours=1)
        suhoor_time_str = suhoor_time.strftime('%H:%M')
        prayer_times['suhoor'] = suhoor_time_str
        logging.info(f"suhoor: {suhoor_time_str}")

    dailyTimesFPath = dailyTimesPath()
    
    # Save the updated prayer times to the specified file
    with open(dailyTimesFPath, 'w') as f:
        json.dump(prayer_times, f, indent=4)









