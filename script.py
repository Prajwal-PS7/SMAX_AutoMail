
# ------------------ !! Import Statements !! ------------------#

import json
import csv
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gethostbyname, gaierror

# ------------------ !! Curl Configuration !! ------------------#

# Curl command for JWT token generation
curl_auth = [
    'curl', '-k', '-X', 'POST', 'https://127.0.0.1:8080/auth/authentication-endpoint/authenticate/token?TENANTID=123456789',
    '-H', 'Content-Type: application/json',
    '-d', '{"Login":"FakeUser","password":"FakePass@123"}'
]

# Execute curl command for authentication
auth_response = subprocess.Popen(curl_auth, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
auth_output, auth_error = auth_response.communicate()

jwt_token = auth_output.decode('UTF-8')

# Check if JWT token is successfully generated
if jwt_token:
    print("!! JWT Token generated Successfully !!")

    # Curl request to fetch asset data
    curl_request = [
        'curl', '-k', '-X', 'GET', 'https://127.0.0.1:8080/rest/123456789/ems/Device?filter=((SubType%3D%27Desktop%27%20or%20SubType%3D%27Laptop%27%20or%20SubType%3D%27MobileDevice%27%20or%20SubType%3D%27VoipEquipment%27%20or%20SubType%3D%27NetworkPrinter%27%20or%20SubType%3D%27CashRegister%27%20or%20SubType%3D%27ThinClient%27%20or%20SubType%3D%27CCTVSystem_c%27%20or%20SubType%3D%27FireControlExtingushers_c%27%20or%20SubType%3D%27SmokeDetectors_c%27%20or%20SubType%3D%27FireDetectionSystems_c%27%20or%20SubType%3D%27RodentRepellent_c%27%20or%20SubType%3D%27WaterLeakageDetector_c%27%20or%20SubType%3D%27PowerUPS_c%27%20or%20SubType%3D%27Blade_c%27%20or%20SubType%3D%27MODEM_c%27%20or%20SubType%3D%27BladeEnclosure_c%27%20or%20SubType%3D%27Printer_c%27%20or%20SubType%3D%27Ipad_c%27%20or%20SubType%3D%27IPPhone_c%27%20or%20SubType%3D%27Biometric_c%27%20or%20SubType%3D%27Tablet_c%27%20or%20SubType%3D%27VideoConferencing_c%27%20or%20SubType%3D%27UPS_c%27)%20and%20(PhaseId%3D%27pAwaitingDelivery%27%20or%20PhaseId%3D%27pNew%27%20or%20PhaseId%3D%27pInStock%27%20or%20PhaseId%3D%27pReceive%27%20or%20PhaseId%3D%27pReturnedForMaintenance%27%20or%20PhaseId%3D%27pInUse%27%20or%20PhaseId%3D%27pPrepare%27%20or%20PhaseId%3D%27pRetire%27%20or%20PhaseId%3D%27pEnded%27))&layout=SubType,OwnedByPerson.Name,OwnedByPerson.Email,OwnedByPerson.EmployeeNumber,DisplayLabel,PrimaryIPAddress_c,AssetTag,Solid1_c,Solid1_c.DisplayLabel,Solid1_c.Id,Solid1_c.IsDeleted&meta=totalCount&order=SubType%20asc&size=250&skip=0',
        '-H', f'Cookie: SMAX_AUTH_TOKEN={jwt_token}', '-H', 'Accept: application/json'
    ]

    # Execute curl command for fetching asset data
    response = subprocess.Popen(curl_request, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = response.communicate()

    # Decode response and load into JSON
    out_data = output.decode('UTF-8')
    data = json.loads(out_data)

    # Capture the Device Data
    entities_data = data['entities']

    # Convert JSON data to CSV format
    csv_data = []
    csv_header = ['entity_type', 'AssetTag', 'SubType', 'Id', 'DisplayLabel', 'Solid1_c.DisplayLabel', 'OwnedByPerson.Email', 'OwnedByPerson.EmployeeNumber', 'OwnedByPerson.Name']

    csv_data.append(csv_header)

    # Loop through each entity and append data to CSV
    for ent in entities_data:
        related_properties = ent['related_properties']
        properties = ent['properties']
        row = [
            ent['entity_type'],
            properties.get('AssetTag', ''),
            properties.get('SubType', ''),
            properties.get('Id', ''),
            properties.get('DisplayLabel', ''),
        ]
        sol = related_properties.get('Solid1_c', {})
        row.append(sol.get('DisplayLabel', ''))
        owned_by_person = related_properties.get('OwnedByPerson', {})
        row.append(owned_by_person.get('Email', ''))
        row.append(owned_by_person.get('EmployeeNumber', ''))
        row.append(owned_by_person.get('Name', ''))

        csv_data.append(row)

    # Write data to CSV file
    with open('Device.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(csv_data)

    print("CSV File Created")

else:
    print("!! Failed to generate JWT Token !!")

# ------------------ !! Asset Ownership Filteration !! ------------------ #

# Function to Read CSV File
def read_csv(file_path):
    assets = []
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            assets.append(row)
    return assets

# Function to Group Assets by Owner
def group_assets_by_owner(assets):
    owner_assets = {}
    unassigned_assets = []

    for asset in assets:
        owner_mail = asset['OwnedByPerson.Email']
        asset_info = (
            f"Entity Type: {asset['entity_type']}, Asset Tag: {asset['AssetTag']}, SubType: {asset['SubType']}, "
            f"ID: {asset['Id']}, Hostname: {asset['DisplayLabel']}, SOL ID: {asset['Solid1_c.DisplayLabel']}"
        )

        # Group owned/tagged assets
        if owner_mail:
            if owner_mail not in owner_assets:
                owner_assets[owner_mail] = []
            owner_assets[owner_mail].append(asset_info)

        # Group unassigned assets
        else:
            unassigned_assets.append(asset_info)

    return owner_assets, unassigned_assets

# Read assets from CSV file
csv_file_path = 'Device.csv'
assets = read_csv(csv_file_path)

print("run read_csv")

# Group assets by owner
owner_assets, unassigned_assets = group_assets_by_owner(assets)

# ------------------ !! Mail Configuration !! ------------------ #

# SMTP Server Configuration
smtp_server = "smtp_server.com"
smtp_port = 25
sender_email = "admin@fake.com"

# Function to send email
def send_email(to_email, subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        # Connect to the SMTP server
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.sendmail(sender_email, to_email, message.as_string())
        server.quit()
        print(f"Email sent successfully to {to_email}")

    except smtplib.SMTPException as e:
        print(f"Error: Unable to send email to {to_email}. {e}")
    except gaierror:
        print("Error: Unable to connect to the server. Please check the SMTP server address or network settings.")

# Send email to each asset owner
for owner_mail, assets_info in owner_assets.items():
    subject = f"Test Mail | Asset Update - {owner_mail}"
    body = "Hello,\n\nHere are your assigned assets:\n\n" + "\n".join(assets_info)
    send_email(owner_mail, subject, body)

# Send email to admin with unassigned assets
if unassigned_assets:
    subject = "Test Mail | Unassigned Assets Update"
    body = "Hello,\n\nHere are the unassigned assets:\n\n" + "\n".join(unassigned_assets)
    send_email("admin@fake.com", subject, body)
