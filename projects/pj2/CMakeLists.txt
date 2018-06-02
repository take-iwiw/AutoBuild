cmake_minimum_required(VERSION 2.8)

SET(BIN_NAME project1)
project(${BIN_NAME})

add_executable (${BIN_NAME} main.c)
target_link_libraries (${BIN_NAME} m)
