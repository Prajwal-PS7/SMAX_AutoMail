# SMAX-Asset-Owner-Notification-Tool
This project is a Python-based automation tool designed to fetch asset data from SMAX (Service Management Automation X) using REST API. It authenticates and validates tokens to securely retrieve asset details and filters the asset list based on the assigned asset owner. Once filtered, the tool automatically sends an email notification containing the list of assets to their respective owners.


## Key Features
✅ Secure Authentication – Uses REST API token authentication for data retrieval. <br/>
✅ Asset Filtering – Filters asset records based on ownership. <br/>
✅ Automated Email Alerts – Sends asset lists to respective owners via email. <br/>
✅ Customizable HTML Email Template – Uses HTML & CSS for email formatting. <br/>
✅ Error Handling & Logging – Logs API requests, errors, and email delivery status. <br/>

## Technology Stack
* Backend: Python 3
* Frontend (Email Formatting): HTML, CSS
* API Communication: REST API (SMAX)
* Email Handling: SMTP (or relevant email service)

## Setup & Usage

1. **Download the Tool:**
   Download the script to the target Unix-based system.
      ```bash
   git clone clone https://github.com/yourusername/smax-asset-notification.git
   ```
2. **Go to directory path**
      ```bash
   cd smax-asset-notification
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
Configure SMAX API Credentials and Email Settings in the .env or config.py file.

3. **Run the tool:**
   ```bash
   python main.py
   ```

## Future Enhancements
🔹 Add support for multiple notification channels (e.g., Teams, Slack). <br/>
🔹 Implement a web-based dashboard for better control and monitoring. <br/>
🔹 Enhance security by integrating OAuth authentication. <br/>

## Contributions
Feel free to fork this repository, raise issues, or submit pull requests. Any feedback or contributions are welcome!

## Disclaimer

This script is provided as-is without any warranty. Use it at your own risk and ensure that you understand its impact on your system before execution.

For detailed information about the SMAX (Service Management Automation X) REST API, refer to the official documentation provided by the OEM (MicroFocus / OpenText).
