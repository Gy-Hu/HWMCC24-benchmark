cmake_minimum_required(VERSION 3.8)

project(vexpparser VERSION 1.1.0 LANGUAGES CXX)

set (CMAKE_CXX_STANDARD 11)

option(VEXP_PARSER_EXPORT_PACAKGE "Export package if enabled." OFF)

# ------------------------------------------------------------------------
set(VEXP_PARSER_TARGET_NAME                 ${PROJECT_NAME})
set(VEXP_PARSER_CONFIG_INSTALL_DIR          "lib/cmake/${PROJECT_NAME}" CACHE INTERNAL "")
set(VEXP_PARSER_INCLUDE_INSTALL_DIR         "include")
set(VEXP_PARSER_INCLUDE_BUILD_DIR           "${PROJECT_SOURCE_DIR}/include")
set(VEXP_PARSER_TARGETS_EXPORT_NAME         "${PROJECT_NAME}Targets")
set(VEXP_PARSER_CMAKE_CONFIG_TEMPLATE       "cmake/config.cmake.in")
set(VEXP_PARSER_CMAKE_CONFIG_DIR            "${CMAKE_CURRENT_BINARY_DIR}")
set(VEXP_PARSER_CMAKE_VERSION_CONFIG_FILE   "${VEXP_PARSER_CMAKE_CONFIG_DIR}/${PROJECT_NAME}ConfigVersion.camke")
set(VEXP_PARSER_CMAKE_PROJECT_CONFIG_FILE   "${VEXP_PARSER_CMAKE_CONFIG_DIR}/${PROJECT_NAME}Config.cmake")
set(VEXP_PARSER_CMAKE_PROJECT_TARGETS_FILE  "${PROJECT_NAME}Targets.cmake")


# ------------------------------------------------------------------------

set(VEXP_LIBRARY_NAME ${PROJECT_NAME}) 
set(VEXP_EXECUTABLE_NAME "${VEXP_LIBRARY_NAME}exec")

add_subdirectory(src)
include_directories(${VEXP_PARSER_INCLUDE_INSTALL_DIR})


# ------------------------------------------------------------------------
# install

include(CMakePackageConfigHelpers)
write_basic_package_version_file(
  ${VEXP_PARSER_CMAKE_VERSION_CONFIG_FILE}
  COMPATIBILITY AnyNewerVersion
)

configure_file(
  ${VEXP_PARSER_CMAKE_CONFIG_TEMPLATE}
  ${VEXP_PARSER_CMAKE_PROJECT_CONFIG_FILE}
  @ONLY
)

install(
  FILES ${VEXP_PARSER_CMAKE_PROJECT_CONFIG_FILE} ${VEXP_PARSER_CMAKE_VERSION_CONFIG_FILE}
  DESTINATION ${VEXP_PARSER_CONFIG_INSTALL_DIR}
)

install(
  EXPORT ${VEXP_PARSER_TARGETS_EXPORT_NAME}
  DESTINATION ${VEXP_PARSER_CONFIG_INSTALL_DIR}
  NAMESPACE ${PROJECT_NAME}::
  FILE ${VEXP_PARSER_PROJECT_TARGETS_FILE}
)

export(
  TARGETS ${VEXP_LIBRARY_NAME}
  NAMESPACE ${PROJECT_NAME}::
  FILE ${VEXP_PARSER_CMAKE_PROJECT_TARGETS_FILE}
)

if(${VEXP_PARSER_EXPORT_PACKAGE})
  export(PACKAGE ${PROJECT_NAME})
endif()


# ---------------------------------------------------------------------------- #
# UNINSTALL
# uninstall files listed in install_manifest.txt
# ---------------------------------------------------------------------------- #
if(NOT TARGET uninstall)
  configure_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/cmake/cmake_uninstall.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake"
    IMMEDIATE @ONLY
  )

  add_custom_target(uninstall
    COMMAND 
      ${CMAKE_COMMAND} -P ${CMAKE_CURRENT_BINARY_DIR}/cmake/cmake_uninstall.cmake
  )
endif()


# ------------------------------------------------------------------------

