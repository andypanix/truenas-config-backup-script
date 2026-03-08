lint +args="":
    docker run --rm -v "$PWD:/data" -w /data ghcr.io/astral-sh/ruff check . {{args}}

backup:
    docker compose run --rm truenas-backup-config python3 truenas-backup.py --now
