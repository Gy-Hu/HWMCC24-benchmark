message(STATUS "Build Type: ${CMAKE_BUILD_TYPE}")

FIND_PACKAGE(BISON 3.0.4 REQUIRED)
FIND_PACKAGE(FLEX 2.5.35 REQUIRED)

set(SOURCE_DIR ${CMAKE_CURRENT_SOURCE_DIR})
set(BINARY_DIR ${CMAKE_CURRENT_BINARY_DIR})

set(FLEX_INPUT  vexp_scanner.l)
set(FLEX_OUTPUT vexp_scanner.cpp)

set(BISON_INPUT  vexp_parser.y)
set(BISON_OUTPUT vexp_parser.cc)
set(BISON_OUTPUT_HEADER vexp_parser.hh)

# ------------------------------------------------------------------------

if(DEFINED FLEXLEXER_INCLUDE_PATH)
  message(STATUS "Flex include path:   ${FLEXLEXER_INCLUDE_PATH}")
  include_directories(${FLEXLEXER_INCLUDE_PATH})
endif()

message(STATUS "Parser Build Flags Debug:   ${CMAKE_CXX_FLAGS_DEBUG}")
message(STATUS "Parser Link Flags Debug:    ${CMAKE_EXE_LINKER_FLAGS_DEBUG}")
message(STATUS "Parser Build Flags Release: ${CMAKE_CXX_FLAGS_RELEASE}")
message(STATUS "Parser Link Flags Release:  ${CMAKE_EXE_LINKER_FLAGS_RELEASE}")

# ------------------------------------------------------------------------

add_custom_command(
  COMMAND ${BISON_EXECUTABLE}
  ARGS -y ${SOURCE_DIR}/${BISON_INPUT} -o ${BINARY_DIR}/${BISON_OUTPUT}
  OUTPUT ${BINARY_DIR}/${BISON_OUTPUT} ${BINARY_DIR}/${BISON_OUTPUT_HEADER}
  WORKING_DIRECTORY ${SOURCE_DIR} #/${BISON_INPUT}
  DEPENDS ${SOURCE_DIR}/${BISON_INPUT}
)

add_custom_command(
  COMMAND ${FLEX_EXECUTABLE}
  ARGS -o ${BINARY_DIR}/${FLEX_OUTPUT} ${SOURCE_DIR}/${FLEX_INPUT}
  OUTPUT ${BINARY_DIR}/${FLEX_OUTPUT}
  WORKING_DIRECTORY ${SOURCE_DIR} #/${FLEX_INPUT}
  DEPENDS ${BINARY_DIR}/${BISON_OUTPUT} ${BINARY_DIR}/${BISON_OUTPUT_HEADER} ${SOURCE_DIR}/${FLEX_INPUT}
)

SET_SOURCE_FILES_PROPERTIES(${BINARY_DIR}/${FLEX_OUTPUT}  GENERATED)
SET_SOURCE_FILES_PROPERTIES(${BINARY_DIR}/${BISON_OUTPUT} GENERATED)

# ------------------------------------------------------------------------

set(VEXP_PARSER_LIB_SRC ${BINARY_DIR}/${FLEX_OUTPUT}
                   ${BINARY_DIR}/${BISON_OUTPUT}
                   ${SOURCE_DIR}/vexp.cc
                   ${SOURCE_DIR}/interpreter.cpp
)

add_library(${VEXP_LIBRARY_NAME} ${VEXP_PARSER_LIB_SRC})
add_library(${VEXP_LIBRARY_NAME}::${VEXP_LIBRARY_NAME} ALIAS ${VEXP_LIBRARY_NAME})

if(${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME})
  if(${CMAKE_COMPILER_IS_GNUCXX})
    target_compile_options(${VEXP_LIBRARY_NAME} PRIVATE -Wall)
    target_compile_options(${VEXP_LIBRARY_NAME} PRIVATE -W)
  endif()
endif()

set_property(
  TARGET ${VEXP_LIBRARY_NAME}
  PROPERTY POSITION_INDEPENDENT_CODE ON
)

set_target_properties(${VEXP_LIBRARY_NAME} PROPERTIES C_EXTENSIONS OFF)

target_include_directories(${VEXP_LIBRARY_NAME}
  PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${PROJECT_SOURCE_DIR}/include>
)

target_include_directories(${VEXP_LIBRARY_NAME}
  PUBLIC
    $<INSTALL_INTERFACE:include>
    $<BUILD_INTERFACE:${BINARY_DIR}>
)

# ------------------------------------------------------------------------

add_executable(${VEXP_EXECUTABLE_NAME} vexp_test.cc)

if(${CMAKE_PROJECT_NAME} STREQUAL ${PROJECT_NAME})
  if(${CMAKE_COMPILER_IS_GNUCXX})
    target_compile_options(${VEXP_EXECUTABLE_NAME} PRIVATE -Wall)
    target_compile_options(${VEXP_EXECUTABLE_NAME} PRIVATE -W)
  endif()
endif()

target_link_libraries(${VEXP_EXECUTABLE_NAME} ${VEXP_LIBRARY_NAME})

target_include_directories(${VEXP_EXECUTABLE_NAME} 
    PRIVATE ${PROJECT_SOURCE_DIR}/include
)

# ------------------------------------------------------------------------

install(TARGETS ${VEXP_LIBRARY_NAME} ${VEXP_EXECUTABLE_NAME}
  EXPORT ${VEXP_PARSER_TARGETS_EXPORT_NAME}
  LIBRARY DESTINATION lib
  ARCHIVE DESTINATION lib
  RUNTIME DESTINATION bin
  INCLUDES DESTINATION ${VLOG_PARSER_INCLUDE_INSTALL_DIR}
)

install(
  DIRECTORY ${VEXP_PARSER_INCLUDE_BUILD_DIR}/vexpparser
  DESTINATION ${VEXP_PARSER_INCLUDE_INSTALL_DIR}
)

