# Makefile для проекта revolt_cli

# Имя бинарника
BINARY_NAME = revolt_cli

# Точка входа для PyInstaller
ENTRY_POINT = revolt_cli/__main__.py

# Папка для бинарника
DIST_DIR = dist

# Папка для Python артефактов
BUILD_DIR = build_artifacts

# Виртуальное окружение через Poetry
POETRY = poetry run

# -------------------
# Основная цель сборки
# -------------------
build: clean install pyinstaller_build poetry_build
	@echo "Build completed!"
	@echo "Binary: $(DIST_DIR)/$(BINARY_NAME)"
	@echo "Python packages: $(BUILD_DIR)/"

# -------------------
# Установка зависимостей (включая dev)
# -------------------
install:
	@echo "Installing dependencies via Poetry..."
	poetry install

# -------------------
# Очистка предыдущих сборок
# -------------------
clean:
	@echo "Cleaning previous builds..."
	rm -rf build $(DIST_DIR) *.spec $(BUILD_DIR)
	@echo "Clean completed."

# -------------------
# Сборка бинарника через PyInstaller
# -------------------
pyinstaller_build:
	@echo "Building binary $(BINARY_NAME) via PyInstaller..."
	$(POETRY) pyinstaller --onefile --name $(BINARY_NAME) $(ENTRY_POINT)
	@echo "Binary ready in $(DIST_DIR)/$(BINARY_NAME)"

# -------------------
# Сборка wheel и tar.gz через Poetry
# -------------------
poetry_build:
	@echo "Building Python package (wheel and tar.gz)..."
	mkdir -p $(BUILD_DIR)
	poetry build --format wheel --format sdist -o $(BUILD_DIR)
	@echo "Python package ready in $(BUILD_DIR)/"

# -------------------
# Быстрый запуск бинарника после сборки
# -------------------
run: build
	@./$(DIST_DIR)/$(BINARY_NAME)
