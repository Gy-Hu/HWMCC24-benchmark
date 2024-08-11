#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "ilang::ilang" for configuration ""
set_property(TARGET ilang::ilang APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(ilang::ilang PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libilang.so"
  IMPORTED_SONAME_NOCONFIG "libilang.so"
  )

list(APPEND _cmake_import_check_targets ilang::ilang )
list(APPEND _cmake_import_check_files_for_ilang::ilang "${_IMPORT_PREFIX}/lib/libilang.so" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
