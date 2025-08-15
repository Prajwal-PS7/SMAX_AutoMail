import os
import glob
import json
from mods.logger import log, log_success, log_error

CONFIG_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_FILE = os.path.join(CONFIG_DIR, 'conf', 'config.json')

def load_config():
    log("Loading [config.json] file.", TAG="CONFIG")
    try:
        with open(CONFIG_FILE, 'r', encoding='UTF-8') as file:
            return json.load(file)
    except Exception as e:
        log_error(f"Error loading config file: {e}", TAG="CONFIG")
        log("File [config.json] not found.", TAG="CONFIG")
        return {}

def load_csv():
    log("Loading device file in [data] directory", TAG="CONFIG")
    try:
        FILES = glob.glob("./data/device_*.csv")
        if not FILES:
            log_error(f"No CSV file found in [data] directory!", TAG="CONFIG")
            log(f"No CSV file found in [data] directory!", TAG="CONFIG")
            return None
        LATEST_FILE = max(FILES, key=os.path.getctime)
        log_success(f"Latest data file selected: {LATEST_FILE}", TAG="CONFIG")
        log("Latest data file selected", TAG="CONFIG")
        return LATEST_FILE
    except Exception as e:
        log_error(f"Error while selecting latest CSV: {e}", TAG="CONFIG")
        log(f"Failed to select latest CSV file.", TAG="CONFIG")
        return None
