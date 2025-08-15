import csv
from mods.logger import log, log_success, log_error
from mods.setup import load_config, load_csv

CONFIG = load_config()
SOL_FILE = load_csv()

def read_csv():
    log(f"Reading CSV data file...", TAG="FILTER")
    with open(SOL_FILE, newline='', encoding='UTF-8') as f:
        log_success(f"Data File [{SOL_FILE}] read successfuly!", TAG="FILTER")
        log(f"CSV data file read completed...", TAG="FILTER")
        return list(csv.DictReader(f))

def read_sol_mapping():
    log(f"Loading SOL Mapping file from conf...", TAG="CONFIG")
    MAPPING = {}
    try:
        with open(CONFIG['SOL_CSV'], newline='', encoding="UTF-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                MAPPING[row['SOL'].strip()] = row['Mail'].strip()
        log_success(f"SOL Mapping loaded successfully!", TAG="CONFIG")
        log(f"Sol Mapping file loaded successfully.", TAG="CONFIG")
    except FileNotFoundError:
        log_error(f"[sol.csv] file not found!", TAG="CONFIG")
        log(f"[sol.csv] file not found!", TAG="CONFIG")
    return MAPPING

def create_table(HTML_FORMAT):
    log(f"Formating Asset table...", TAG="FORMAT")
    try:
        with open(CONFIG['MAIL_FORMAT'], "r") as f:
            HTML_CONTENT = f.read()
            HTML_CONTENT = HTML_CONTENT.replace("{table_rows}", HTML_FORMAT)
        return HTML_CONTENT
    except FileNotFoundError:
        log_error(f"HTML file not found!", TAG="FORMAT")
        log(f"[index.html] file not found!", TAG="FORMAT")
        return ""

def json_to_html(DATA):
    log(f"Formating JSON to HTML table...", TAG="FORMAT")
    rows = []

    for ATB in DATA:
        Entity_Type = ATB.get('Entity Type', '')
        Id = ATB.get('Id', '')
        HostName = ATB.get('Hostname', '')
        Sub_Type = ATB.get('Sub Type', '')
        Type = ATB.get('Type', '')
        Asset_Tag = ATB.get('Asset Tag', '')
        SOL_ID = ATB.get('SOL ID', '')
        Support_Type = ATB.get('Support Type', '')
        Device_Status = ATB.get('Device Status', '')
        Owner_Name = ATB.get('Owner Name', '')
        Owner_EIN = ATB.get('Owner EIN', '')
        Owner_Email = ATB.get('Owner Email', '')

        row = f"""
        <tr>
            <td>{Entity_Type}</td>
            <td>{Id}</td>
            <td>{HostName}</td>
            <td>{Sub_Type}</td>
            <td>{Type}</td>
            <td>{Asset_Tag}</td>
            <td>{SOL_ID}</td>
            <td>{Support_Type}</td>
            <td>{Device_Status}</td>
            <td>{Owner_Name}</td>
            <td>{Owner_EIN}</td>
            <td>{Owner_Email}</td>

        </tr>
        """

        rows.append(row)
    
    log(f"JSON to HTML table formating finished...", TAG="FORMAT")
    return "\n".join(rows)

def group_by_owner(ASSETS):

    OWNER_ASSETS = {}
    UNASSIGNED_ASSETS = []
    log(f"Grouping asstes by owners...", TAG="FILTER")

    for dev in ASSETS:
        DEV_TYPE = dev['Sub Type'].strip().lower()
        if DEV_TYPE not in ['desktop','laptop']:
            continue

        OWNER_MAIL = dev['Owner Email'].strip()
        OWNER_EIN = dev['Owner EIN'].strip()

        if OWNER_MAIL:
            if OWNER_MAIL not in OWNER_ASSETS:
                OWNER_ASSETS[OWNER_MAIL] = {"OWNER_EIN": OWNER_EIN, "ASSETS": []}
            OWNER_ASSETS[OWNER_MAIL]["ASSETS"].append(dev)
        else:
            UNASSIGNED_ASSETS.append(dev)

    log(f"Grouping assets by owner finished.", TAG="FILTER")
    return OWNER_ASSETS, UNASSIGNED_ASSETS

def group_by_sol(ASSETS, SOL_MAPPING):

    SOL_GROUP = {}
    UNASSIGNED_SOL = {}
    log(f"Grouping assets by SOL ID...", TAG="FILTER")

    for dev in ASSETS:
        SOL = dev['SOL ID'].strip()
        if SOL in SOL_MAPPING:
            SOL_MAIL = SOL_MAPPING[SOL]
            if SOL_MAIL not in SOL_GROUP:
                SOL_GROUP[SOL_MAIL] = {"SOL_ID": SOL, "ASSETS": []}
            SOL_GROUP[SOL_MAIL]["ASSETS"].append(dev)
        else:
            if SOL not in UNASSIGNED_SOL:
                UNASSIGNED_SOL[SOL] = []
            UNASSIGNED_SOL[SOL].append(dev)

    log(f"Grouping assets by SOL ID finished.", TAG="FILTER")
    return SOL_GROUP, UNASSIGNED_SOL

def sol_format(UNASSIGNED_SOL):
    SOL_ASSET = []
    for SOL_ID, ASSETS in UNASSIGNED_SOL.items():
        SOL_ASSET.extend(ASSETS)
    return SOL_ASSET
