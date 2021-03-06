# include_directories(${CMAKE_SOURCE_DIR}/libutil)
# include_directories(${CMAKE_SOURCE_DIR}/../include)

include_directories(${PYTHON_PATH}/include)
link_directories(${PYTHON_PATH}/libs)
link_directories(${CMAKE_LIBRARY_OUTPUT_DIRECTORY})

file(GLOB headers *.h)
file(GLOB files *.cpp)
file(GLOB doubleconversion third_party/double-conversion/*.cc)
file(GLOB modules Modules/*.cpp)
add_library(Pythia SHARED 
    ${files}
    ${doubleconversion}
    ${modules}
    ${headers}
    Pythia.rc
)

if(CMAKE_BUILD_TYPE STREQUAL RelWithDebInfo OR CMAKE_BUILD_TYPE STREQUAL Release)
    set_target_properties(Pythia PROPERTIES COMPILE_FLAGS "/GL")
    set_target_properties(Pythia PROPERTIES LINK_FLAGS "/LTCG")
endif()

# Copy the file to the @Pythia directory after the fact
add_custom_command(
    TARGET Pythia POST_BUILD
    COMMAND ${CMAKE_COMMAND} -E copy
        "$<TARGET_FILE:Pythia>"
        "${CMAKE_LIBRARY_OUTPUT_DIRECTORY}/../@Pythia/"
)

if(CMAKE_CL_64)
    set_target_properties(Pythia PROPERTIES OUTPUT_NAME "Pythia_x64")
else()
    set_target_properties(Pythia PROPERTIES OUTPUT_NAME "Pythia")
endif()

# add_definitions(-DEXPMODULE)

# target_link_libraries(Pythia debug libutil.lib)
# target_link_libraries(Pythia optimized libutil.lib)
