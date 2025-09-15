BINARY_NAME = revolt-cli
ENTRY_POINT = revolt_cli/__main__.py
DIST_DIR = dist
BUILD_DIR = build_artifacts
POETRY = poetry run

YELLOW = \033[33m
GREEN = \033[92m
RESET = \033[0m

define yellow-echo
    @echo "🤞$(YELLOW)$1$(RESET)"
endef

define green-echo
    @echo "🙌$(GREEN)$1$(RESET)"
endef

build: clean install pyinstaller_build
	$(call green-echo, "Build completed!")

build_all: clean install pyinstaller_build poetry_build
	$(call green-echo, "Build completed!")
	$(call green-echo, "Binary: $(DIST_DIR)/$(BINARY_NAME)")
	$(call green-echo, "Python packages: $(BUILD_DIR)/")

install:
	$(call yellow-echo, "installing dependencies via Poetry...")
	poetry install
	$(call green-echo, "Installing process dependencies successfully done.")

clean:
	$(call yellow-echo, "cleaning previous builds...")
	@if [ -d $(DIST_DIR) ]; then rm -rf build $(DIST_DIR) *.spec $(BUILD_DIR); fi
	$(call green-echo, "Cleaning process successfully done.")

pyinstaller_build:
	$(call yellow-echo, "building binary $(BINARY_NAME) via PyInstaller...")
	$(POETRY) pyinstaller --onefile --name $(BINARY_NAME) $(ENTRY_POINT)
	$(call green-echo, "Building viw PyInstaller process successfully done.")
	$(call green-echo, "Binary ready in $(DIST_DIR)/$(BINARY_NAME)")

poetry_build:
	$(call yellow-echo, "building Python package (wheel and tar.gz)...")
	mkdir -p $(BUILD_DIR)
	poetry build --format wheel --format sdist -o $(BUILD_DIR)
	$(call green-echo, "Python package ready in $(BUILD_DIR)/")

run: build
	@./$(DIST_DIR)/$(BINARY_NAME)