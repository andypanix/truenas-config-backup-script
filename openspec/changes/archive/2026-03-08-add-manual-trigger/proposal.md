# Add Manual Trigger

## Problem
The current script is designed strictly as a background daemon. There is no built-in way to easily force an immediate backup on demand (e.g., to test notifications, verify credentials on first setup, or trigger a pre-upgrade backup) without temporarily manipulating the `SCHEDULED_TIME` variable and waiting.

## Solution
Introduce a command-line argument `--now`. When this flag is provided, the script will bypass the schedule daemon loop, execute the `backup()` function immediately, and exit.

## Scope
- Update `truenas-backup.py` to parse command-line arguments using `argparse`.
- Allow the script to exit cleanly (`exit 0` on success, `exit 1` on failure) when running in one-shot mode.
- Document the new feature in `README.md`.