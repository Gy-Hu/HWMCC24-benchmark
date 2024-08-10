#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "smtparser::smtparser" for configuration ""
set_property(TARGET smtparser::smtparser APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(smtparser::smtparser PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libsmtparser.so"
  IMPORTED_SONAME_NOCONFIG "libsmtparser.so"
  )

list(APPEND _cmake_import_check_targets smtparser::smtparser )
list(APPEND _cmake_import_check_files_for_smtparser::smtparser "${_IMPORT_PREFIX}/lib/libsmtparser.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
