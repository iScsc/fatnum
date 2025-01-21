# Makefile for C++ project using CC

# Compiler
CC = g++

# Directories
INCLUDE_DIR = include
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Flags
CXXFLAGS = -I$(INCLUDE_DIR) -Wall -Wextra -Werror -Wpedantic -fopenmp -g -O0 -std=c++17

filename = $(SRC_DIR)/hdinfo.cpp

# Source and object files
SRC_FILES = $(wildcard $(SRC_DIR)/*.cpp)
HDR_FILES = $(wildcard $(INCLUDE_DIR)/*.hpp)
OBJ_FILES = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRC_FILES))

# Target executable
TARGET = $(BIN_DIR)/app

# Default target
all: $(TARGET)

# Link object files to create the executable
$(TARGET): $(OBJ_FILES)
	@mkdir -p $(BIN_DIR)
	$(CC) $(OBJ_FILES) -o $@

# Compile source files to object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CXXFLAGS) -c $< -o $@

# Rule for testing a single file
testing:
	@mkdir -p $(BIN_DIR)
	$(CC) $(CXXFLAGS) -o $(BIN_DIR)/test $(filename)

# Clean up build files
clean:
	- rm -rf $(OBJ_DIR) $(BIN_DIR)
	- find . -name "*.cpp~" -type f -delete
	- find . -name "*.hpp~" -type f -delete

format:
	find . -name '*.cpp' -o -name '*.hpp' | xargs clang-format -i

.PHONY: all clean