# ---------------------------------------------------------------------------- #

include(FindPackageHandleStandardArgs)

set(${CMAKE_FIND_PACKAGE_NAME}_CONFIG ${CMAKE_CURRENT_LIST_FILE})

find_package_handle_standard_args(smtparser CONFIG_MODE)

if(NOT TARGET smtparser::smtparser) 

  include("${CMAKE_CURRENT_LIST_DIR}/smtparserTargets.cmake")

  if((NOT TARGET smtparser) AND 
     (NOT smtparser_FIND_VERSION OR smtparser_FIND_VERSION VERSION_LESS 1.0.0))

    add_library(smtparser INTERFACE IMPORTED)
    set_target_properties(smtparser PROPERTIES
      INTERFACE_LINK_LIBRARIES smtparser::smtparser
    )

  endif()

endif()
