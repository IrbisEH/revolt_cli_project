BINARY_NAME = revolt_cli
ENTRY_POINT = revolt_cli/__main__.py
DIST_DIR = dist
BUILD_DIR = build_artifacts
POETRY = poetry run

build: clean install pyinstaller_build poetry_build
	@echo "Build completed!"
	@echo "Binary: $(DIST_DIR)/$(BINARY_NAME)"
	@echo "Python packages: $(BUILD_DIR)/"

install:
	@echo "Installing dependencies via Poetry..."
	poetry install

clean:
	@echo "Cleaning previous builds..."
	rm -rf build $(DIST_DIR) *.spec $(BUILD_DIR)
	@echo "Clean completed."

pyinstaller_build:
	@echo "Building binary $(BINARY_NAME) via PyInstaller..."
	$(POETRY) pyinstaller --onefile --name $(BINARY_NAME) $(ENTRY_POINT)
	@echo "Binary ready in $(DIST_DIR)/$(BINARY_NAME)"

poetry_build:
	@echo "Building Python package (wheel and tar.gz)..."
	mkdir -p $(BUILD_DIR)
	poetry build --format wheel --format sdist -o $(BUILD_DIR)
	@echo "Python package ready in $(BUILD_DIR)/"

run: build
	@./$(DIST_DIR)/$(BINARY_NAME)
