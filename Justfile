lint +args="":
    docker run --rm -v "$PWD:/data" -w /data ghcr.io/astral-sh/ruff check . {{args}}
