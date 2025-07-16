#!/bin/bash

PARENT_DIR="$(dirname "$(realpath "$0")")"
VENV_PATH="$PARENT_DIR/.venv/bin/python3"
SCRIPT_PATH="$PARENT_DIR/app_py/main.py"

if [ ! -f "$VENV_PATH" ]; then
    echo "Ошибка: Интерпретатор Python не найден в $VENV_PATH"
    exit 1
fi

if [ ! -f "$SCRIPT_PATH" ]; then
    echo "Ошибка: Скрипт не найден в $SCRIPT_PATH"
    exit 1
fi

source "$PARENT_DIR/.venv/bin/activate"

sudo -E "$VENV_PATH" "$SCRIPT_PATH" "$@"