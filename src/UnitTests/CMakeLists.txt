cmake_minimum_required(VERSION 3.5.0)

set(CMAKE_MODULE_PATH "$ENV{DEVELOPMENT_ENVIRONMENT_CMAKE_MODULE_PATH}")

if(NOT WIN32)
    string(REPLACE ":" ";" ${CMAKE_MODULE_PATH} ${CMAKE_MODULE_PATH})
endif()

include(CppCommon)
include(CommonHelpers)
include(BoostCommon)

set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

foreach(_name IN ITEMS
    Serialization_UnitTest
)
    add_executable(${_name} ${_name}.cpp)
    
    target_link_libraries(${_name} CommonHelpers)
    target_link_libraries(${_name} BoostCommon)
    target_link_libraries(${_name} ${Boost_LIBRARIES})

    add_test(NAME ${_name} COMMAND ${_name} --success)
endforeach()
