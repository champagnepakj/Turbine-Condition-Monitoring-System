cmake_minimum_required(VERSION 3.20)
project(turbine_agent)

set(CMAKE_CXX_STANDARD 17)

find_package(RdKafka CONFIG QUIET)

if(NOT RdKafka_FOUND)
    find_package(PkgConfig REQUIRED)
    pkg_check_modules(RDKAFKA REQUIRED rdkafka++)
endif()

add_executable(agent src/main.cpp src/signal_generator.cpp src/bearing_geometry.cpp src/kafka_producer.cpp)
target_include_directories(agent PRIVATE include)

if(RdKafka_FOUND)
    target_link_libraries(agent PRIVATE RdKafka::rdkafka++)
else()
    target_include_directories(agent PRIVATE ${RDKAFKA_INCLUDE_DIRS})
    target_link_libraries(agent PRIVATE ${RDKAFKA_LIBRARIES})
endif()
