#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "vexpparser::vexpparser" for configuration ""
set_property(TARGET vexpparser::vexpparser APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(vexpparser::vexpparser PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libvexpparser.so"
  IMPORTED_SONAME_NOCONFIG "libvexpparser.so"
  )

list(APPEND _cmake_import_check_targets vexpparser::vexpparser )
list(APPEND _cmake_import_check_files_for_vexpparser::vexpparser "${_IMPORT_PREFIX}/lib/libvexpparser.so" )

# Import target "vexpparser::vexpparserexec" for configuration ""
set_property(TARGET vexpparser::vexpparserexec APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(vexpparser::vexpparserexec PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/vexpparserexec"
  )

list(APPEND _cmake_import_check_targets vexpparser::vexpparserexec )
list(APPEND _cmake_import_check_files_for_vexpparser::vexpparserexec "${_IMPORT_PREFIX}/bin/vexpparserexec" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
