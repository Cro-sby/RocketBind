cmake_minimum_required(VERSION 3.10)
project(RocketBind LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Force 64-bit build
if(NOT CMAKE_SIZEOF_VOID_P EQUAL 8)
    message(FATAL_ERROR "RocketBind requires a 64-bit build. Please use -A x64 or set CMAKE_GENERATOR_PLATFORM=x64")
endif()

# Path to BakkesModSDK
set(BAKKESMODSDK_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../BakkesModSDK-master")

# Path to ImGui
set(IMGUI_ROOT "${CMAKE_CURRENT_SOURCE_DIR}/../imgui-master/imgui-master")

# Include directories
include_directories(
    ${BAKKESMODSDK_ROOT}/include
    ${CMAKE_CURRENT_SOURCE_DIR}
    ${IMGUI_ROOT}
)

# Link directories
link_directories(${BAKKESMODSDK_ROOT}/lib)

# ImGui source files
set(IMGUI_SOURCES
    ${IMGUI_ROOT}/imgui.cpp
    ${IMGUI_ROOT}/imgui_draw.cpp
    ${IMGUI_ROOT}/imgui_tables.cpp
    ${IMGUI_ROOT}/imgui_widgets.cpp
)

# Add the plugin as a shared library
add_library(RocketBind SHARED
    RocketBind.cpp
    RocketBind.h
    RocketBindGUI.cpp
    ${IMGUI_SOURCES}
)

# Link against BakkesMod SDK
target_link_libraries(RocketBind pluginsdk.lib)

# Set output directory
set_target_properties(RocketBind PROPERTIES
    RUNTIME_OUTPUT_DIRECTORY_RELEASE ${CMAKE_CURRENT_SOURCE_DIR}/Release
    RUNTIME_OUTPUT_DIRECTORY_DEBUG ${CMAKE_CURRENT_SOURCE_DIR}/Debug
)
