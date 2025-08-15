import json
import csv
import subprocess
import os
from mods.logger import log, log_error, log_success
from mods.setup import load_config
import datetime

CONFIG = load_config()

def create_token():
    log(f"Token creation Starting...", TAG="Main")
    AUTH_URL = CONFIG['TENANT']['AUTH_URL']
    USERNAME = CONFIG['SMAX_AUTH']['USERNAME']
    PASSWORD = CONFIG['SMAX_AUTH']['PASSWORD']
    CURL_AUTH = [
        'curl', '-k', '-s', '-X', 'POST',
        AUTH_URL,
        '-H', 'Content-Type: application/json',
        '-d', f'{{ "login": "{USERNAME}", "password": "{PASSWORD}" }}'
    ]
    log(f"Authenticating user...", TAG="Main")
    AUTH_RESPONSE = subprocess.Popen(CURL_AUTH, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    AUTH_OUTPUT, AUTH_ERROR = AUTH_RESPONSE.communicate()

    if AUTH_ERROR:
        log(f"Authentication failed!", TAG="AUTH")
        log_error(f"Authentication failed!", TAG="AUTH")
        log_error(AUTH_ERROR.decode(), TAG="AUTH")
        return None
    log_success(f"Authentication Success.", TAG="AUTH")
    log(f"Authentication Success.", TAG="AUTH")
    log(f"Fetching JWT Token...", TAG="AUTH")
    log(f"Token Generated Successfully...", TAG="AUTH")
    return AUTH_OUTPUT.decode().strip().replace('"', '')

def fetch_asset_data(JWT_TOKEN):
    log(f"Asset data fetching Starting...", TAG="ASSET")
    GET_URL = CONFIG['TENANT']['GET_URL']
    CURL_REQUEST = [
        'curl', '-k', '-s', '-X', 'GET',
        GET_URL,
        '-H', f'Cookie: SMAX_AUTH_TOKEN={JWT_TOKEN}'
    ]

    REQUEST_RESPONSE = subprocess.Popen(CURL_REQUEST, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    REQUEST_OUTPUT, REQUEST_ERROR = REQUEST_RESPONSE.communicate()

    if REQUEST_ERROR:
        log(f"Failed to fetch asset data.", TAG="ASSET")
        log_error(f"Failed to fetch asset data!", TAG="ASSET")
        log_error(REQUEST_ERROR.decode(), TAG="ASSET")
        return None
    log_success(f"Asset data fetched successfully.", TAG="ASSET")
    log(f"Asset data fetched successfully...", TAG="ASSET")
    return REQUEST_OUTPUT.decode()

def create_csv(JSON_DATA):
    log(f"Asset data file creation Starting...", TAG="CSV")
    DATE_FORMAT = datetime.datetime.now().strftime("%Y-%m-%d")
    CSV_FILE = os.path.join("data", f"device_{DATE_FORMAT}.csv")

    DATA = json.loads(JSON_DATA)
    ENTITIES = DATA.get("entities", [])

    HEADERS = [
       'Entity Type', 'Id', 'Hostname', 'Sub Type', 'Type', 'Asset Tag', 'SOL ID', 'Support Type', 'Device Status', 'Owner Name', 'Owner EIN', 'Owner Email'
    ]
    log(f"Mapping Asset data format form JSON to CSV...", TAG="CSV")
    with open(CSV_FILE, 'w', newline='', encoding='utf-8') as FILE:
        writer = csv.DictWriter(FILE, fieldnames=HEADERS)
        writer.writeheader()

        for e in ENTITIES:
            p = e['properties']
            r = e['related_properties']
            row = {
                'Entity Type': e['entity_type'],
                'Id': p.get('Id', ''),
                'Hostname': p.get('DisplayLabel'),
                'Sub Type': p.get('SubType', ''),
                'Type': p.get('Subtypeprinter_c', ''),
                'Asset Tag': p.get('AssetTag', ''),
                'SOL ID': r.get('Solid1_c', {}).get('DisplayLabel', ''),
                'Support Type': p.get('WarrantyAMC1_c', ''),
                'Device Status': p.get('Devicestatus_c', ''),
                'Owner Name': r.get('OwnedByPerson', {}).get('Name', ''),
                'Owner EIN': p.get('UserEIN_c', ''),
                'Owner Email': r.get('OwnedByPerson', {}).get('Email', '')
            }
            writer.writerow(row)

    log(f"Asset data Mapped into CSV File...", TAG="CSV")
    log_success(f"Asset data fetched into [{CSV_FILE}] file.", TAG="WRITE")
    log(f"Asset data file creation finished.", TAG="CSV")
    return CSV_FILE

