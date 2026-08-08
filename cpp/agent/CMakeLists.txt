cmake_minimum_required(VERSION 3.20)
project(turbine_agent)

set(CMAKE_CXX_STANDARD 17)

find_package(RdKafka CONFIG REQUIRED)

add_executable(agent src/main.cpp src/signal_generator.cpp src/bearing_geometry.cpp src/kafka_producer.cpp)
target_include_directories(agent PRIVATE include)
target_link_libraries(agent PRIVATE RdKafka::rdkafka++)
