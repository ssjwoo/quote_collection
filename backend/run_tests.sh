#!/bin/bash

source .venv/bin/activate
TESTING=true uv run pytest "$@"
