cmake_minimum_required(VERSION 3.12)
project(dg5f_s_moveit_config)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY config launch srdf
  DESTINATION share/${PROJECT_NAME}
)

ament_package()
