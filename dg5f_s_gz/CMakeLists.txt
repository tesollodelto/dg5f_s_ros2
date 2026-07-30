cmake_minimum_required(VERSION 3.12)
project(dg5f_s_gz)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(trajectory_msgs REQUIRED)

add_executable(dg5f_s_left_gz_test_cpp src/dg5f_s_left_gz_test.cpp)
# ament_target_dependencies() was removed in the ament_cmake shipped with
# ROS 2 Lyrical. Detect the command rather than the distro so one
# CMakeLists covers Humble, Jazzy and Lyrical.
if(COMMAND ament_target_dependencies)
  ament_target_dependencies(dg5f_s_left_gz_test_cpp rclcpp trajectory_msgs)
else()
  target_link_libraries(dg5f_s_left_gz_test_cpp
    rclcpp::rclcpp
    ${trajectory_msgs_TARGETS}
  )
endif()

add_executable(dg5f_s_right_gz_test_cpp src/dg5f_s_right_gz_test.cpp)
# ament_target_dependencies() was removed in the ament_cmake shipped with
# ROS 2 Lyrical. Detect the command rather than the distro so one
# CMakeLists covers Humble, Jazzy and Lyrical.
if(COMMAND ament_target_dependencies)
  ament_target_dependencies(dg5f_s_right_gz_test_cpp rclcpp trajectory_msgs)
else()
  target_link_libraries(dg5f_s_right_gz_test_cpp
    rclcpp::rclcpp
    ${trajectory_msgs_TARGETS}
  )
endif()

add_executable(dg5f_s_15dof_left_gz_test_cpp src/dg5f_s_15dof_left_gz_test.cpp)
# ament_target_dependencies() was removed in the ament_cmake shipped with
# ROS 2 Lyrical. Detect the command rather than the distro so one
# CMakeLists covers Humble, Jazzy and Lyrical.
if(COMMAND ament_target_dependencies)
  ament_target_dependencies(dg5f_s_15dof_left_gz_test_cpp rclcpp trajectory_msgs)
else()
  target_link_libraries(dg5f_s_15dof_left_gz_test_cpp
    rclcpp::rclcpp
    ${trajectory_msgs_TARGETS}
  )
endif()

add_executable(dg5f_s_15dof_right_gz_test_cpp src/dg5f_s_15dof_right_gz_test.cpp)
# ament_target_dependencies() was removed in the ament_cmake shipped with
# ROS 2 Lyrical. Detect the command rather than the distro so one
# CMakeLists covers Humble, Jazzy and Lyrical.
if(COMMAND ament_target_dependencies)
  ament_target_dependencies(dg5f_s_15dof_right_gz_test_cpp rclcpp trajectory_msgs)
else()
  target_link_libraries(dg5f_s_15dof_right_gz_test_cpp
    rclcpp::rclcpp
    ${trajectory_msgs_TARGETS}
  )
endif()

install(TARGETS
  dg5f_s_left_gz_test_cpp
  dg5f_s_right_gz_test_cpp
  dg5f_s_15dof_left_gz_test_cpp
  dg5f_s_15dof_right_gz_test_cpp
  DESTINATION lib/${PROJECT_NAME})

install(
  DIRECTORY config urdf launch
  DESTINATION share/${PROJECT_NAME}
)

install(
  PROGRAMS
  script/dg5f_s_left_gz_test.py
  script/dg5f_s_right_gz_test.py
  script/dg5f_s_15dof_left_gz_test.py
  script/dg5f_s_15dof_right_gz_test.py
  DESTINATION lib/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
