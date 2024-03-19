import logging
import socket
import time
import pychromecast
import os
import datetime
from audioServer import confirmServerStart


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

def get_ip_address():
    # Attempt to connect to an external host in order to determine the local machine's IP address
    try:
        # The use of '1.1.1.1' is arbitrary and is simply used to establish a connection to determine the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("1.1.1.1", 80))
        ip_address = s.getsockname()[0]
        s.close()
    except Exception as e:
        ip_address = "Error: " + str(e)
    return ip_address

currentIP = get_ip_address()

# Audio file URLs, correctly including `currentIP` in the 'fajr' URL
audio_files = {
    'fajr': f'http://{currentIP}:8512/Fajr%20Athan%20-%20Mishary%20Afasy.mp3',
    'dhuhr': f'http://{currentIP}:8512/Athan%20-%20Islam%20Sobhi.mp3',
    'asr': f'http://{currentIP}:8512/Athan%20-%20Islam%20Sobhi.mp3',
    'maghrib': f'http://{currentIP}:8512/Athan%20-%20Mishary%20Afasy.mp3',
    'isha': f'http://{currentIP}:8512/Athan%20-%20Islam%20Sobhi.mp3',
    'imsak': f'http://{currentIP}:8512/Imsak%20Notif.m4a',
    'suhoor': f'http://{currentIP}:8512/Suhoor%20Alram.mp3'
}

# Volume levels for each prayer
volume_levels = {
    'fajr': 0.4,
    'dhuhr': 0.5,
    'asr': 0.5,
    'maghrib': 0.8,
    'isha': 0.5,
    'imsak': 0.4,
    'suhoor': 0.6
}




def playAudio(targetAudioDevice, prayer):

    if not confirmServerStart():
        return
    
    audioFile = audio_files.get(prayer, audio_files['dhuhr'])
    volumeLvl = volume_levels.get(prayer, 0.5)
    

    try:
        chromecasts, browser = pychromecast.get_chromecasts()
        if not chromecasts:
            logging.error("No Chromecast devices found.")
            return

        # Attempt to find the specific Chromecast device by name
        cast = next((cc for cc in chromecasts if cc.name == targetAudioDevice), None)
        if cast is None:
            logging.error(f"Chromecast device named '{targetAudioDevice}' not found.")
            return

        # Connect to the device
        cast.wait()
        logging.info(f"Connected to Chromecast named '{targetAudioDevice}'. Setting volume to {volumeLvl}.")
        cast.set_volume(volumeLvl)

        # Play the audio file
        mc = cast.media_controller
        mc.play_media(audioFile, 'audio/mp3')
        mc.block_until_active()
        logging.info(f"Playing audio: {audioFile}")

        # Wait for the audio to finish playing
        while not mc.status.player_is_idle:
            time.sleep(1)

        logging.info("Audio playback finished.")

    except Exception as e:
        logging.error(f"An error occurred: {e}")

    finally:
        # Ensure the Chromecast discovery service is properly stopped
        pychromecast.discovery.stop_discovery(browser)

