#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
set(CMAKE_IMPORT_FILE_VERSION 1)

# Import target "verilogparser::verilogparser" for configuration ""
set_property(TARGET verilogparser::verilogparser APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(verilogparser::verilogparser PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/lib/libverilogparser.so"
  IMPORTED_SONAME_NOCONFIG "libverilogparser.so"
  )

list(APPEND _cmake_import_check_targets verilogparser::verilogparser )
list(APPEND _cmake_import_check_files_for_verilogparser::verilogparser "${_IMPORT_PREFIX}/lib/libverilogparser.so" )

# Import target "verilogparser::verilogparserexec" for configuration ""
set_property(TARGET verilogparser::verilogparserexec APPEND PROPERTY IMPORTED_CONFIGURATIONS NOCONFIG)
set_target_properties(verilogparser::verilogparserexec PROPERTIES
  IMPORTED_LOCATION_NOCONFIG "${_IMPORT_PREFIX}/bin/verilogparserexec"
  )

list(APPEND _cmake_import_check_targets verilogparser::verilogparserexec )
list(APPEND _cmake_import_check_files_for_verilogparser::verilogparserexec "${_IMPORT_PREFIX}/bin/verilogparserexec" )

# Commands beyond this point should not need to know the version.
set(CMAKE_IMPORT_FILE_VERSION)
