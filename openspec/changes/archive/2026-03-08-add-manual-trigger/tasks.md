# Add Manual Trigger: Tasks

- [x] Task 1: Update `truenas-backup.py` argument parsing
  - Import `argparse` and `sys`.
  - Add argument parser for `--now`.
  - Update `backup()` to return `True` or `False`.
  - Implement the branching logic to run once and exit if `--now` is present.
- [x] Task 2: Update `README.md`
  - Add a section on how to run manual/instant backups using Docker.