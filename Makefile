# Makefile for C++ project using nvcc

# Compiler
NVCC = nvcc

# Directories
INCLUDE_DIR = include
SRC_DIR = src
OBJ_DIR = obj
BIN_DIR = bin

# Flags
CXXFLAGS = -I$(INCLUDE_DIR)

# Source and object files
SRC_FILES = $(wildcard $(SRC_DIR)/*.cpp)
OBJ_FILES = $(patsubst $(SRC_DIR)/%.cpp, $(OBJ_DIR)/%.o, $(SRC_FILES))

# Target executable
TARGET = $(BIN_DIR)/app

# Default target
all: $(TARGET)

# Link object files to create the executable
$(TARGET): $(OBJ_FILES)
	@mkdir -p $(BIN_DIR)
	$(NVCC) $(OBJ_FILES) -o $@

# Compile source files to object files
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OBJ_DIR)
	$(NVCC) $(CXXFLAGS) -c $< -o $@

# Clean up build files
clean:
	rm -rf $(OBJ_DIR) $(BIN_DIR)

.PHONY: all clean