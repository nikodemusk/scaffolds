cmake_minimum_required(VERSION 3.21)

include(cmake/prelude.cmake)

project(
    MyC-project
    VERSION 0.1.0
    DESCRIPTION "Ett testprojekt"
    HOMEPAGE_URL "https://example.org"
    LANGUAGES C
)

include(cmake/variables.cmake)

# ---- Declare library ----

add_library(
    MyC-project_lib OBJECT
    source/lib.c
)

target_include_directories(
    MyC-project_lib ${warning_guard}
    PUBLIC
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/source>"
    "\$<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>"
)


target_compile_features(MyC-project_lib PUBLIC c_std_17)

# ---- Declare executable ----

add_executable(MyC-project_exe source/main.c source/test.c)
add_executable(MyC-project::exe ALIAS MyC-project_exe)

set_property(TARGET MyC-project_exe PROPERTY OUTPUT_NAME MyC-project)

target_compile_features(MyC-project_exe PRIVATE c_std_17)

add_custom_target(
    run
    COMMAND $<TARGET_FILE:MyC-project_exe>
    DEPENDS MyC-project_exe
    # WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
    WORKING_DIRECTORY ${PROJECT_SOURCE_DIR}
)

# Hitta SDL3
find_package(SDL3 REQUIRED)

# Länka mot exekveraren
target_link_libraries(MyC-project_exe PRIVATE MyC-project_lib SDL3 m)
# target_link_libraries(MyC-project_exe PRIVATE MyC-project_lib)

# ---- Install rules ----

if(NOT CMAKE_SKIP_INSTALL_RULES)
  include(cmake/install-rules.cmake)
endif()

# ---- Developer mode ----

if(NOT MyC-project_DEVELOPER_MODE)
  return()
elseif(NOT PROJECT_IS_TOP_LEVEL)
  message(
      AUTHOR_WARNING
      "Developer mode is intended for developers of MyC-project"
  )
endif()

include(cmake/dev-mode.cmake)
