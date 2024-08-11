# ---------------------------------------------------------------------------- #

include(FindPackageHandleStandardArgs)

set(${CMAKE_FIND_PACKAGE_NAME}_CONFIG ${CMAKE_CURRENT_LIST_FILE})

find_package_handle_standard_args(verilogparser CONFIG_MODE)

if(NOT TARGET verilogparser::verilogparser) 

  include("${CMAKE_CURRENT_LIST_DIR}/verilogparserTargets.cmake")

  if((NOT TARGET verilogparser) AND 
     (NOT verilogparser_FIND_VERSION OR verilogparser_FIND_VERSION VERSION_LESS 1.0.0))

    add_library(verilogparser INTERFACE IMPORTED)
    set_target_properties(verilogparser PROPERTIES
      INTERFACE_LINK_LIBRARIES verilogparser::verilogparser
    )

  endif()

endif()
