# ---------------------------------------------------------------------------- #

include(FindPackageHandleStandardArgs)

set(${CMAKE_FIND_PACKAGE_NAME}_CONFIG ${CMAKE_CURRENT_LIST_FILE})

find_package_handle_standard_args(vcdparser CONFIG_MODE)

if(NOT TARGET vcdparser::vcdparser) 

  include("${CMAKE_CURRENT_LIST_DIR}/vcdparserTargets.cmake")

  if((NOT TARGET vcdparser) AND 
     (NOT vcdparser_FIND_VERSION OR vcdparser_FIND_VERSION VERSION_LESS 1.0.0))

    add_library(vcdparser INTERFACE IMPORTED)
    set_target_properties(vcdparser PROPERTIES
      INTERFACE_LINK_LIBRARIES vcdparser::vcdparser
    )

  endif()

endif()
