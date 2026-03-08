# Add Manual Trigger: Design

## Architecture

1. **Argument Parsing (`truenas-backup.py`)**
   - Import the standard `argparse` and `sys` modules.
   - Define a parser that accepts an optional `--now` flag.
   - Modify the `backup()` function to return a boolean (`True` on success, `False` on exception) so the calling context knows the outcome.

2. **Execution Flow**
   - After setting up the environment variables and logging:
     ```python
     parser = argparse.ArgumentParser(description="TrueNAS Config Backup Script")
     parser.add_argument('--now', action='store_true', help="Run backup immediately and exit")
     args = parser.parse_args()
     ```
   - If `args.now` is True:
     - Call `success = backup()`.
     - Call `sys.exit(0 if success else 1)`.
   - If `args.now` is False:
     - Proceed with the existing scheduling logic and enter the `while True` loop.

3. **Docker Interaction**
   - The primary intended usage will be via Docker:
     ```bash
     docker compose run --rm truenas-backup-config python truenas-backup.py --now
     ```
     or against the running container:
     ```bash
     docker exec -it truenas-backup-config python truenas-backup.py --now
     ```