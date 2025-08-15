from mods.setup import load_config
from mods.logger import init_logger
from mods.fetch_data import create_token, fetch_asset_data, create_csv
from mods.data_filter import read_csv, group_by_owner, group_by_sol, sol_format, read_sol_mapping
from mods.mailer import send_owner_mail, send_sol_mail, send_unassigned_owner_mail, send_unassigned_sol_mail

CONFIG = load_config()
SOL_CSV = read_sol_mapping()

def main():
    init_logger()

    JWT_TOKEN = create_token()
    ASSET_DATA = fetch_asset_data(JWT_TOKEN)

    create_csv(ASSET_DATA)

    ASSETS = read_csv()
    ASSIGNED_ASSETS, UNASSIGNED_ASSETS = group_by_owner(ASSETS)
    ASSIGNED_SOL, UNASSIGNED_SOL = group_by_sol(ASSETS, SOL_CSV)

    send_owner_mail(ASSIGNED_ASSETS)
    send_unassigned_owner_mail(UNASSIGNED_ASSETS)
    send_sol_mail(ASSIGNED_SOL)
    FORMAT_UNASSIGNED_SOL = sol_format(UNASSIGNED_SOL)
    send_unassigned_sol_mail(FORMAT_UNASSIGNED_SOL)

if __name__ == "__main__":
    main()
