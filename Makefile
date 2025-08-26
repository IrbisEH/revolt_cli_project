# Установка зависимостей
install:
	poetry install

# Сборка бинаря
build:
	poetry run pyinstaller --onefile myarp/cli.py -n myarp

# Установка бинаря в систему
install-bin:
	sudo mv dist/myarp /usr/local/bin/myarp
	sudo setcap cap_net_raw+ep /usr/local/bin/myarp

# Очистка
clean:
	rm -rf dist build __pycache__ .pytest_cache *.spec
