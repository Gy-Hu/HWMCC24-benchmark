#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "vcdparser::vcdparser" for configuration ""
set_property(TARGET vcdparser::vcdparser APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(vcdparser::vcdparser PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libvcdparser.so"
  IMPORTED_SONAME_NOCONFIG "libvcdparser.so"
  )

list(APPEND _cmake_import_check_targets vcdparser::vcdparser )
list(APPEND _cmake_import_check_files_for_vcdparser::vcdparser "${_IMPORT_PREFIX}/lib/libvcdparser.so" )

# Import target "vcdparser::vcdparserexec" for configuration ""
set_property(TARGET vcdparser::vcdparserexec APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(vcdparser::vcdparserexec PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/vcdparserexec"
  )

list(APPEND _cmake_import_check_targets vcdparser::vcdparserexec )
list(APPEND _cmake_import_check_files_for_vcdparser::vcdparserexec "${_IMPORT_PREFIX}/bin/vcdparserexec" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
