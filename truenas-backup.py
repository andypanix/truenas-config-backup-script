import os
import subprocess
import requests
import schedule
import time
import logging
import argparse
import sys
from datetime import datetime
from dotenv import load_dotenv
import urllib3

# Disable InsecureRequestWarning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
load_dotenv()

# USER CONFIGURABLE VARIABLES
server_url = os.environ.get("SERVER_URL")
api_key = os.environ.get("API_KEY")
sec_seed = os.environ.get("SEC_SEED", "true")
backuploc = os.environ.get("BACKUPLOC")
max_nr_of_files = int(os.environ.get("MAXNR_OF_FILES", 10))
scheduled_time = os.environ.get("SCHEDULED_TIME")  # Time to run the job

# Notification variables
uptime_kuma_url = os.environ.get("UPTIME_KUMA_URL")
telegram_bot_token = os.environ.get("TELEGRAM_BOT_TOKEN")
telegram_chat_id = os.environ.get("TELEGRAM_CHAT_ID")

# Set directory for backups
backup_main_dir = backuploc if backuploc else "/app/truenas-backup"
os.makedirs(backup_main_dir, exist_ok=True)


def send_telegram_alert(message):
    """Sends an alert to Telegram if configured."""
    if not telegram_bot_token or not telegram_chat_id:
        return

    try:
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": telegram_chat_id,
            "text": f"🚨 TrueNAS Backup Error\n\n{message}",
        }
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logging.info("Telegram alert sent successfully.")
    except Exception as e:
        logging.error(f"Failed to send Telegram alert: {e}")


def uptime_kuma_ping():
    """Pings Uptime Kuma if configured."""
    if not uptime_kuma_url:
        return

    try:
        response = requests.get(uptime_kuma_url, timeout=10)
        response.raise_for_status()
        logging.info("Successfully pinged Uptime Kuma.")
    except Exception as e:
        logging.error(f"Failed to ping Uptime Kuma: {e}")


def backup():
    logging.info("Starting backup process...")
    try:
        # Use appropriate extension if we are exporting the secret seed
        file_ext = "tar" if sec_seed.lower() == "true" else "db"

        # Generate file name
        file_name = f"{subprocess.check_output('hostname').decode().strip()}-TrueNAS-{datetime.now().strftime('%Y%m%d%H%M%S')}.{file_ext}"

        logging.info("Requesting backup from TrueNAS API...")
        response = requests.post(
            f"{server_url}/api/v2.0/config/save",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "*/*",
                "Content-Type": "application/json",
            },
            json={"secretseed": sec_seed.lower() == "true"},
            verify=False,  # Bypass SSL certificate verification
            stream=True,  # Stream the response content
            timeout=60,
        )
        response.raise_for_status()

        logging.info(f"Saving backup to {file_name}...")
        with open(os.path.join(backup_main_dir, file_name), "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        # The next section checks for and deletes old backups
        if max_nr_of_files != 0:
            file_list = [
                f
                for f in os.listdir(backup_main_dir)
                if os.path.isfile(os.path.join(backup_main_dir, f))
            ]
            nr_of_files = len(file_list)

            if max_nr_of_files < nr_of_files:
                n_files_to_remove = nr_of_files - max_nr_of_files
                file_list.sort(
                    key=lambda f: os.path.getctime(os.path.join(backup_main_dir, f))
                )

                for i in range(n_files_to_remove):
                    file_to_remove = file_list[i]
                    file_path = os.path.join(backup_main_dir, file_to_remove)
                    os.remove(file_path)
                    logging.info(f"Removed old backup: {file_to_remove}")

        logging.info("Backup completed successfully.")
        uptime_kuma_ping()
        return True

    except Exception as e:
        error_msg = f"Backup failed: {str(e)}"
        logging.error(error_msg)
        send_telegram_alert(error_msg)
        return False


# Parse command line arguments
parser = argparse.ArgumentParser(description="TrueNAS Config Backup Script")
parser.add_argument(
    "--now", action="store_true", help="Run backup immediately and exit"
)
args = parser.parse_args()

if args.now:
    logging.info("Running manual one-shot backup (--now flag provided)...")
    success = backup()
    if success:
        logging.info("Manual backup finished successfully. Exiting.")
        sys.exit(0)
    else:
        logging.error("Manual backup failed. Exiting with error code 1.")
        sys.exit(1)

# Schedule the backup function
if scheduled_time:
    schedule.every().day.at(scheduled_time).do(backup)
    logging.info(f"Backup scheduled daily at {scheduled_time}")
else:
    logging.error(
        "SCHEDULED_TIME environment variable is not set. Backup will not run."
    )
    sys.exit(1)

# Print message before starting the backup
print("Starting backup service in background mode...")

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(1)
