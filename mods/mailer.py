import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from socket import gaierror
from mods.setup import load_config
from mods.logger import log, log_success, log_error
from mods.data_filter import create_table, json_to_html

CONFIG = load_config()

def send_mail(OWNER_MAIL, SUBJECT, BODY):
    log("Mail Sender Started.", TAG="MAILER")
    MSG = MIMEMultipart()
    MSG["From"] = CONFIG['USER_MEMBERS']['SENDER_MAIL']
    MSG["To"] = OWNER_MAIL
    MSG["Subject"] = SUBJECT
    MSG.attach(MIMEText(BODY, "html"))

    try:
        SERVER = smtplib.SMTP(CONFIG['SMTP_SERVER']['SMTP_HOST'], CONFIG['SMTP_SERVER']['SMTP_PORT'])
        SERVER.sendmail(CONFIG['USER_MEMBERS']['SENDER_MAIL'], OWNER_MAIL, MSG.as_string())
        log_success(f"Email sent successfully to - {OWNER_MAIL}", TAG="MAILER")
    except smtplib.SMTPException as e:
        log_error(f"Failed to send email to - {OWNER_MAIL}.", TAG="MAILER")
        log_error(f"{e}", TAG="MAILER")
    except gaierror:
        log_error(f"Unable to connect to the server. Please check the SMTP server address or network settings.")
        log("SMTP Connection error!", TAG="MAILER")

def send_owner_mail(ASSIGNED_ASSETS):
    log("Sending mail for assigned owner.", TAG="MAILER")
    for MAIL, DATA in ASSIGNED_ASSETS.items():
        OWNER_EIN = DATA['OWNER_EIN']
        ASSETS = DATA['ASSETS']
        SUBJECT = f"Intimation to Employee (EIN - {OWNER_EIN}) on the Asset Tagged"
        HTML_FORMAT = json_to_html(DATA['ASSETS'])
        MAIL_BODY = create_table(HTML_FORMAT)
        send_mail(MAIL, SUBJECT, MAIL_BODY)

def send_sol_mail(ASSIGNED_SOL):
    log("Sending mail for assigned sol.", TAG="MAILER")
    for MAIL, DATA in ASSIGNED_SOL.items():
        SOL_ID = DATA['SOL_ID']
        ASSETS = DATA['ASSETS']
        SUBJECT = f"Intimation to Branch (SOL - {SOL_ID}) on the Asset Tagged"
        HTML_FORMAT = json_to_html(DATA['ASSETS'])
        MAIL_BODY = create_table(HTML_FORMAT)
        send_mail(MAIL, SUBJECT, MAIL_BODY)

def send_unassigned_owner_mail(UNASSIGNED_ASSETS):
    log("Sending mail for unassigned owner.", TAG="MAILER")
    MAIL = CONFIG['USER_MEMBERS']['SUPPORT_MAIL']
    SUBJECT = f"Intimation to Un-Assigned Owner on the Asset Tagged"
    HTML_FORMAT = json_to_html(UNASSIGNED_ASSETS)
    MAIL_BODY = create_table(HTML_FORMAT)
    send_mail(MAIL, SUBJECT, MAIL_BODY)

def send_unassigned_sol_mail(UNASSIGNED_SOL):
    log("Sending mail for unassigned sol.", TAG="MAILER")
    MAIL = CONFIG['USER_MEMBERS']['SUPPORT_MAIL']
    SUBJECT = f"Intimation to Un-Mapped SOL in config on the Asset Tagged"
    HTML_FORMAT = json_to_html(UNASSIGNED_SOL)
    MAIL_BODY = create_table(HTML_FORMAT)
    send_mail(MAIL, SUBJECT, MAIL_BODY)
