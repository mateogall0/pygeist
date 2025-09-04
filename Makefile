# Compiler and flags
CC := gcc
CFLAGS := -Wall -Wextra -std=gnu11 -fPIC \
	  -I$(PWD) -Icore/include \
	  $(shell python3-config --includes)

LDFLAGS := -shared $(shell python3-config --ldflags)


# Source directories
CORE_SERVER_SRC := core/src/server
CORE_COMMON_SRC := core/src/common
ADAPTER_SERVER_SRC := adapters/src/server

# Target Python module
ADAPTER_TARGET := zeitgeist_server
TARGET_NAME := _adapter.so

# Build directory for object files
OBJ_DIR := build

# Find all source files recursively
CORE_SRC := $(shell find $(CORE_SERVER_SRC) $(CORE_COMMON_SRC) -name '*.c')
ADAPTER_SRC := $(shell find $(ADAPTER_SERVER_SRC) -name '*.c')
SRC := $(CORE_SRC) $(ADAPTER_SRC)

# Corresponding object files in build directory
OBJ := $(patsubst %.c,$(OBJ_DIR)/%.o,$(SRC))

# Default target
all: $(ADAPTER_TARGET)/$(TARGET_NAME)

# Build shared library
$(ADAPTER_TARGET)/$(TARGET_NAME): $(OBJ)
	@mkdir -p $(ADAPTER_TARGET)
	$(CC) $(LDFLAGS) -o $@ $^

# Compile source files into object files in build/
$(OBJ_DIR)/%.o: %.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	rm -rf $(OBJ_DIR)
	rm -f $(ADAPTER_TARGET)/$(TARGET_NAME)

.PHONY: all clean
