This script is designed to automate the process of creating backups of your TrueNAS configuration and deleting old backups once a specified limit is reached. The script uses environment variables to configure various settings, such as the server URL, API key, backup location, and the maximum number of backup files to keep. Here's a simple explanation of the main components of the script:

## Setup Instructions

1. Copy the provided `.env.template` file to `.env`:
   ```bash
   cp .env.template .env
   ```
2. Open the `.env` file and populate it with your specific values (TrueNAS URL, API Key, path, etc.).
3. Build and start the container using Docker Compose:
   ```bash
   docker compose up -d --build
   ```

## Security Considerations (API Key)

⚠️ **IMPORTANT:** In TrueNAS CORE (and older versions of SCALE), downloading the system configuration with the `secretseed` requires administrative privileges. This means the API Key you provide in the `.env` file usually has **root-level access** to your NAS.

To protect your system, strongly adhere to these best practices:
1. **Protect your `.env` file:** Never commit your `.env` file to version control (it is ignored by default via `.gitignore`). Ensure the file permissions on your Docker host are restrictive (e.g., `chmod 600 .env`).
2. **Restrict Network Access:** Ensure your TrueNAS management interface (ports 80/443) is not exposed to the public internet.
3. **IP Firewalling (Recommended):** Since the API Key has root privileges, configure a firewall rule on your TrueNAS network settings to reject API calls unless they originate from the specific IP address of the machine running this Docker container.

## How It Works

Import required libraries: The script imports various libraries needed for its functionality, such as os, subprocess, requests, schedule, time, logging, datetime, and dotenv.
Load environment variables: The script uses the dotenv library to load environment variables from the `.env` file, which contains user-configurable variables like the server URL, API key, secret seed, backup location, maximum number of backup files, and scheduled time for the backup.

Create the backup directory: The script creates a directory for storing backup files using the os.makedirs() function.

Define the backup function: The backup() function is responsible for creating a new backup of the TrueNAS configuration and deleting old backups if the maximum number of backup files is reached. The function does the following:
Generates a file name for the backup based on the hostname and the current date and time.
Sends a POST request to the TrueNAS API to save the configuration.
Writes the configuration data to a file in the backup directory.
Checks if there are more backup files than the maximum number allowed and deletes the oldest backup files until the limit is reached.

### Optional DR Notifications
The script optionally supports Disaster Recovery (DR) level notifications:
1. **Passive Monitoring (Uptime Kuma):** You can set `UPTIME_KUMA_URL` to a Push monitor URL. The script will ping this URL *only* when a backup succeeds. If Uptime Kuma doesn't receive this ping within your scheduled timeframe (e.g. 24h), it can trigger its own alerts.
2. **Active Error Alerting (Telegram):** If you configure `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`, the script will send a direct message to that Telegram chat if any error occurs during the backup process (network issue, API error, disk write permission, etc.).

Schedule the backup function: The script uses the schedule library to schedule the backup() function to run at the specified time every day.
Keep the script running: The script continuously runs the scheduled tasks using a while loop, which checks for pending tasks and sleeps for one second between checks.
The script is designed to run indefinitely, creating new backups and deleting old ones according to the specified schedule and maximum number of backup files allowed.