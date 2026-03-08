# Add DR Notifications: Tasks

- [x] Task 1: Update `truenas-backup.py` core logic
  - Wrap the `backup()` function in `try...except Exception as e:`.
  - Create helper functions `send_telegram_alert(message)` and `uptime_kuma_ping()`.
  - Call `uptime_kuma_ping()` on success.
  - Call `send_telegram_alert()` on exception and log the error via standard `logging`.
  - Make sure the notifications are conditional based on the presence of the environment variables.

- [x] Task 2: Update Configuration
  - Update `.env` with placeholder variables `UPTIME_KUMA_URL`, `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`.
  - Update `docker-compose.yml` to inject the new environment variables and add `restart: unless-stopped`.

- [x] Task 3: Update `README.md`
  - Document the new notification features and how to configure them for a robust DR setup.
