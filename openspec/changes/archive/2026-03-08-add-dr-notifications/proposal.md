# Add DR Notifications

## Problem
The current TrueNAS backup script lacks any form of active or passive monitoring. If a backup fails (due to network issues, API changes, or storage problems), the container may crash or silently fail without notifying the administrator. In a Disaster Recovery (DR) scenario, silent failures are unacceptable.

## Solution
Implement a dual-layer notification system:
1. **Passive Monitoring (Dead Man's Snitch):** Ping an external Uptime Kuma "Push" monitor upon successful backup completion. If Uptime Kuma doesn't receive this ping within the expected timeframe, it will alert the administrator.
2. **Active Alerting (Telegram):** If an exception occurs during the backup process, actively catch the error and send a detailed webhook notification via Telegram.

## Scope
- Modify `truenas-backup.py` to include a robust `try...except` block around the core logic.
- Add HTTP GET request for Uptime Kuma success ping.
- Add HTTP POST request for Telegram error notifications.
- Update `docker-compose.yml` to support new environment variables and add a `restart: unless-stopped` policy to ensure the container recovers from crashes.
- Update `README.md` to document the new DR features.

## Non-Goals
- Adding complex logging to external systems (Elasticsearch, etc.).
- Implementing automatic retry logic beyond what Docker's restart policy provides.
