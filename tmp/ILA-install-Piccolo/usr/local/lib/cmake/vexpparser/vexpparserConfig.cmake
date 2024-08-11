# ---------------------------------------------------------------------------- #

include(FindPackageHandleStandardArgs)

set(${CMAKE_FIND_PACKAGE_NAME}_CONFIG ${CMAKE_CURRENT_LIST_FILE})

find_package_handle_standard_args(vexpparser CONFIG_MODE)

if(NOT TARGET vexpparser::vexpparser) 

  include("${CMAKE_CURRENT_LIST_DIR}/vexpparserTargets.cmake")

  if((NOT TARGET vexpparser) AND 
     (NOT vexpparser_FIND_VERSION OR vexpparser_FIND_VERSION VERSION_LESS 1.0.0))

    add_library(vexpparser INTERFACE IMPORTED)
    set_target_properties(vexpparser PROPERTIES
      INTERFACE_LINK_LIBRARIES vexpparser::vexpparser
    )

  endif()

endif()
