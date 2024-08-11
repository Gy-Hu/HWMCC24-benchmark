# ---------------------------------------------------------------------------- #
# define dependencies
# ---------------------------------------------------------------------------- #
include(CMakeFindDependencyMacro)
find_dependency(glog REQUIRED)
find_dependency(nlohmann_json REQUIRED)
find_dependency(verilogparser REQUIRED)
find_dependency(vcdparser REQUIRED)
find_dependency(vexpparser REQUIRED)
find_dependency(smtparser REQUIRED)
find_dependency(fmt REQUIRED)
find_dependency(Z3 REQUIRED)

if(OFF)
  find_dependency(ilasynth REQUIRED)
endif()

if(OFF)
  find_dependency(smtswitch REQUIRED)
endif()

if()
  find_dependency(Boost 1.50 REQUIRED COMPONENTS python)

  if(${CMAKE_VERSION} VERSION_LESS 3.12)
    message(WARNING "Imported target Python::Python not supported.")
    find_dependency(PythonLibs 2.7 REQUIRED)
  else()
    find_dependency(Python 2.7 REQUIRED COMPONENTS Development)
  endif()

endif()

# ---------------------------------------------------------------------------- #
# define exports
# ---------------------------------------------------------------------------- #
include(FindPackageHandleStandardArgs)

set(${CMAKE_FIND_PACKAGE_NAME}_CONFIG ${CMAKE_CURRENT_LIST_FILE})

find_package_handle_standard_args(ilang CONFIG_MODE)

if(NOT TARGET ilang::ilang)
  include("${CMAKE_CURRENT_LIST_DIR}/ilangTargets.cmake")

  if((NOT TARGET ilang) AND 
     (NOT ilang_FIND_VERSION OR 
      ilang_FIND_VERSION VERSION_LESS 1.0.0))

    add_library(ilang INTERFACE IMPORTED)

    set_target_properties(ilang PROPERTIES
      INTERFACE_LINK_LIBRARIES ilang::ilang
    )

  endif()

endif()

