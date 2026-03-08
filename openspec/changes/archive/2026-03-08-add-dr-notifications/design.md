# Add DR Notifications: Design

## Proposed Architecture

1. **Environment Variables**
   Introduce three new optional environment variables:
   - `UPTIME_KUMA_URL`: The full push URL provided by Uptime Kuma (e.g., `http://uptime.panix.cloud:88/api/push/zTiwbA...`).
   - `TELEGRAM_BOT_TOKEN`: The bot token provided by BotFather.
   - `TELEGRAM_CHAT_ID`: The ID of the chat/channel where the bot will post error messages.

2. **Python Implementation in `truenas-backup.py`**
   - Import the existing `requests` library.
   - Create a `send_telegram_alert(message)` helper function that checks if `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` exist, and if so, sends a POST request to `https://api.telegram.org/bot<token>/sendMessage`.
   - Create an `uptime_kuma_ping()` helper function that checks if `UPTIME_KUMA_URL` exists, and if so, sends a GET request to the URL.
   - Wrap the main backup procedure (inside `def backup():`) in a `try...except Exception as e:` block.
   - On success (end of `try` block), call `uptime_kuma_ping()`.
   - On exception (`except` block), log the error locally and call `send_telegram_alert()` with a formatted string of the error, then optionally re-raise the exception or just let the schedule continue (preferably, let the schedule continue so it tries again tomorrow without crashing the container).

3. **Docker Improvements**
   - Update `docker-compose.yml` to include a `restart: unless-stopped` policy to ensure the container survives internal failures or host reboots.
   - Pass the new environment variables.

## Considerations
- **Optionality:** If the new environment variables are not set, the script should silently skip the notification steps, remaining backward compatible for users who don't want notifications.
- **Dependency Management:** The `requests` module is already imported and available, so no new dependencies are strictly required (though `urllib.request` was suggested, `requests` is more robust and already in the project).
