import datetime
import os
import glob

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
OUTPUT_DIR = os.path.join(BASE_DIR, "data")

LOG_RETENTION_DAYS = 180           # 6 Months
OUTPUT_RETENTION_DAYS = 365        # 1 Year
TODAY = datetime.datetime.now()

def create_log(LOG_TYPE="runtime"):
    DATE_STAMP = TODAY.strftime("%Y-%m-%d")
    return os.path.join(LOG_DIR, f"{LOG_TYPE}-{DATE_STAMP}.log")

def init_logger():
    log(f"Loging started...", TAG="Main")
    os.makedirs(LOG_DIR, exist_ok=True)
    purge_old_logs()
    purge_old_data()

def write_log(LOG_TYPE, MESSAGE, LEVEL, TAG):
    TIME_STAMP = TODAY.strftime("%Y-%m-%d %H:%M:%S")
    FORMAT = f"{TIME_STAMP} - [{LEVEL}] [{TAG}] : {MESSAGE}"

    LOG_FILE = create_log(LOG_TYPE)
    with open(LOG_FILE, "a") as f:
        f.write(FORMAT + "\n")

def log(MSG, LEVEL="INFO", TAG="Main"):
    write_log("runtime", MSG, LEVEL, TAG)

def log_success(MSG, TAG="Main"):
    write_log("success", MSG, "SUCCESS", TAG)

def log_error(MSG, TAG="Main"):
    write_log("error", MSG, "ERROR", TAG)

def log_cleanup(MSG):
    write_log("cleanup", MSG, "CLEANUP", "Retention")

def purge_old_logs():
    log(f"Removing old logs...", TAG="Main")
    for F in glob.glob(os.path.join(LOG_DIR, "*.log")):
        FILE_TIME = datetime.datetime.fromtimestamp(os.path.getmtime(F))
        if (TODAY - FILE_TIME).days > LOG_RETENTION_DAYS:
            os.remove(F)
            log_cleanup(f"Deleted old log: {F}")
            log(f"Old Logs removed...", TAG="Main")
def purge_old_data():
    log(f"Removing old data...", TAG="Main")
    for F in glob.glob(os.path.join(OUTPUT_DIR, "*.csv")):
        FILE_TIME = datetime.datetime.fromtimestamp(os.path.getmtime(F))
        if (TODAY - FILE_TIME).days > OUTPUT_RETENTION_DAYS:
            os.remove(F)
            log_cleanup(f"Deleted old data: {F}")

# ---------------------------!! Logs !!--------------------------- #          

#    log("Runtime log...", TAG="Main")
#    log_success("Success log.", TAG="Auth")
#    log_error("Error log!", TAG="Error")
#    log_cleanup("Cleanup log !!")
