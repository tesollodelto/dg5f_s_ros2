cmake_minimum_required(VERSION 3.8)
project(dg5f_s_driver)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(delto_hardware REQUIRED)

install(
  PROGRAMS
  script/dg5f_s_right_jtc_test.py
  script/dg5f_s_left_jtc_test.py
  script/dg5f_s_15dof_right_jtc_test.py
  script/dg5f_s_15dof_left_jtc_test.py
  script/dg5f_s_right_jtc_action_test.py
  script/dg5f_s_left_jtc_action_test.py
  script/dg5f_s_15dof_right_jtc_action_test.py
  script/dg5f_s_15dof_left_jtc_action_test.py
  script/dg5f_s_right_pid_test.py
  script/dg5f_s_left_pid_test.py
  script/dg5f_s_15dof_right_pid_test.py
  script/dg5f_s_15dof_left_pid_test.py
  script/dg5f_s_right_pid_all_test.py
  script/dg5f_s_left_pid_all_test.py
  script/dg5f_s_15dof_right_pid_all_test.py
  script/dg5f_s_15dof_left_pid_all_test.py
  DESTINATION lib/${PROJECT_NAME}
)

install(
  DIRECTORY config urdf launch
  DESTINATION share/${PROJECT_NAME}
)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()
