INCLUDE(FindPkgConfig)
PKG_CHECK_MODULES(PC_MXLGS mxlgs)

FIND_PATH(
    MXLGS_INCLUDE_DIRS
    NAMES mxlgs/api.h
    HINTS $ENV{MXLGS_DIR}/include
        ${PC_MXLGS_INCLUDEDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/include
          /usr/local/include
          /usr/include
)

FIND_LIBRARY(
    MXLGS_LIBRARIES
    NAMES gnuradio-mxlgs
    HINTS $ENV{MXLGS_DIR}/lib
        ${PC_MXLGS_LIBDIR}
    PATHS ${CMAKE_INSTALL_PREFIX}/lib
          ${CMAKE_INSTALL_PREFIX}/lib64
          /usr/local/lib
          /usr/local/lib64
          /usr/lib
          /usr/lib64
)

INCLUDE(FindPackageHandleStandardArgs)
FIND_PACKAGE_HANDLE_STANDARD_ARGS(MXLGS DEFAULT_MSG MXLGS_LIBRARIES MXLGS_INCLUDE_DIRS)
MARK_AS_ADVANCED(MXLGS_LIBRARIES MXLGS_INCLUDE_DIRS)

