# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.16

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /mnt/d/kafka-sample/cpp/src/producers

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /mnt/d/kafka-sample/cpp/src/producers/build

# Include any dependencies generated for this target.
include CMakeFiles/coinbase.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/coinbase.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/coinbase.dir/flags.make

CMakeFiles/coinbase.dir/coinbase_producer.cpp.o: CMakeFiles/coinbase.dir/flags.make
CMakeFiles/coinbase.dir/coinbase_producer.cpp.o: ../coinbase_producer.cpp
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/mnt/d/kafka-sample/cpp/src/producers/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building CXX object CMakeFiles/coinbase.dir/coinbase_producer.cpp.o"
	/usr/bin/c++  $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -o CMakeFiles/coinbase.dir/coinbase_producer.cpp.o -c /mnt/d/kafka-sample/cpp/src/producers/coinbase_producer.cpp

CMakeFiles/coinbase.dir/coinbase_producer.cpp.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing CXX source to CMakeFiles/coinbase.dir/coinbase_producer.cpp.i"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -E /mnt/d/kafka-sample/cpp/src/producers/coinbase_producer.cpp > CMakeFiles/coinbase.dir/coinbase_producer.cpp.i

CMakeFiles/coinbase.dir/coinbase_producer.cpp.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling CXX source to assembly CMakeFiles/coinbase.dir/coinbase_producer.cpp.s"
	/usr/bin/c++ $(CXX_DEFINES) $(CXX_INCLUDES) $(CXX_FLAGS) -S /mnt/d/kafka-sample/cpp/src/producers/coinbase_producer.cpp -o CMakeFiles/coinbase.dir/coinbase_producer.cpp.s

# Object files for target coinbase
coinbase_OBJECTS = \
"CMakeFiles/coinbase.dir/coinbase_producer.cpp.o"

# External object files for target coinbase
coinbase_EXTERNAL_OBJECTS =

coinbase: CMakeFiles/coinbase.dir/coinbase_producer.cpp.o
coinbase: CMakeFiles/coinbase.dir/build.make
coinbase: /usr/local/lib/libcppkafka.so.0.4.0
coinbase: /usr/local/lib/librdkafka.so
coinbase: CMakeFiles/coinbase.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/mnt/d/kafka-sample/cpp/src/producers/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking CXX executable coinbase"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/coinbase.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/coinbase.dir/build: coinbase

.PHONY : CMakeFiles/coinbase.dir/build

CMakeFiles/coinbase.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/coinbase.dir/cmake_clean.cmake
.PHONY : CMakeFiles/coinbase.dir/clean

CMakeFiles/coinbase.dir/depend:
	cd /mnt/d/kafka-sample/cpp/src/producers/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /mnt/d/kafka-sample/cpp/src/producers /mnt/d/kafka-sample/cpp/src/producers /mnt/d/kafka-sample/cpp/src/producers/build /mnt/d/kafka-sample/cpp/src/producers/build /mnt/d/kafka-sample/cpp/src/producers/build/CMakeFiles/coinbase.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : CMakeFiles/coinbase.dir/depend

