import datetime
import json
import logging
import os
import schedule
from athanScheduler import athanTimesCreator
from audioPlayer import playAudio
import time as time_module


#Set Audio Device name
targetAudioDevice = "Insert Device Name"

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


athanTimesCreator()
def dailyTimesUpdater():
     schedule.every().day.at("00:01").do(athanTimesCreator())



def check_and_play_prayers():
    # Load the prayer times
    dirPath = os.path.dirname(os.path.abspath(__file__))
    prayerTimesFile = os.path.join(dirPath, 'dailyTimes.json')
    with open(prayerTimesFile, 'r') as f:
        prayerTimes = json.load(f)

    
    excluded_times = ['sunset', 'sunrise', 'midnight']  # Times to ignore

    while True:
        now = datetime.datetime.now().strftime('%H:%M')
        for prayer, time in prayerTimes.items():
            if prayer in excluded_times:  # Skip excluded times
                continue
            if now == time:
                logging.info(f"It's time for {prayer}. Playing Athan.")
                playAudio(targetAudioDevice, prayer)
                # Wait for a minute after playing audio to prevent replaying in the same minute
                time_module.sleep(60)
        time_module.sleep(60)  # Check every 60 seconds

if __name__ == '__main__':
    dailyTimesUpdater()
    check_and_play_prayers()
