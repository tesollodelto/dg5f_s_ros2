# DG5F-S ROS 2

[![CI](https://github.com/tesollodelto/dg5f_s_ros2/actions/workflows/ci.yml/badge.svg)](https://github.com/tesollodelto/dg5f_s_ros2/actions/workflows/ci.yml)
![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-blue?logo=ros)
![ROS 2 Jazzy](https://img.shields.io/badge/ROS_2-Jazzy-blue?logo=ros)

ROS 2 packages for the **Delto Gripper DG5F-S** (5-finger robotic hand, compact version, left/right).

Supports both **20-DOF** and **15-DOF** variants.

## Packages

| Package | Description |
|---|---|
| `dg5f_s_description` | URDF/xacro model, meshes, and RViz display launch |
| `dg5f_s_driver` | ros2_control hardware driver and controller launch files |
| `dg5f_s_gz` | Gazebo simulation |

## Dependencies

This repository requires the following packages to build:

```bash
# Clone into your ROS 2 workspace src directory
git clone https://github.com/tesollodelto/dg_hardware.git
git clone https://github.com/tesollodelto/dg_tcp_comm.git
```

- [`delto_hardware`](https://github.com/tesollodelto/dg_hardware) — Unified hardware interface for Delto grippers
- [`delto_tcp_comm`](https://github.com/tesollodelto/dg_tcp_comm) — TCP communication library for Delto grippers

## Build

```bash
cd ~/ros2_ws
colcon build --packages-select dg5f_s_description dg5f_s_driver dg5f_s_gz
source install/setup.bash
```

## Launch

### 20-DOF

```bash
# RViz display
ros2 launch dg5f_s_description dg5f_s_right_display.launch.py
ros2 launch dg5f_s_description dg5f_s_left_display.launch.py

# Hardware driver
ros2 launch dg5f_s_driver dg5f_s_right_driver.launch.py
ros2 launch dg5f_s_driver dg5f_s_left_driver.launch.py

# Effort controller
ros2 launch dg5f_s_driver dg5f_s_right_effort_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_left_effort_controller.launch.py

# Gazebo simulation
ros2 launch dg5f_s_gz dg5f_s_right_gz.launch.py
ros2 launch dg5f_s_gz dg5f_s_left_gz.launch.py
```

### 15-DOF

```bash
# RViz display
ros2 launch dg5f_s_description dg5f_s_15dof_right_display.launch.py
ros2 launch dg5f_s_description dg5f_s_15dof_left_display.launch.py

# Hardware driver
ros2 launch dg5f_s_driver dg5f_s_15dof_right_driver.launch.py
ros2 launch dg5f_s_driver dg5f_s_15dof_left_driver.launch.py

# Effort controller
ros2 launch dg5f_s_driver dg5f_s_15dof_right_effort_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_15dof_left_effort_controller.launch.py

# Gazebo simulation
ros2 launch dg5f_s_gz dg5f_s_15dof_right_gz.launch.py
ros2 launch dg5f_s_gz dg5f_s_15dof_left_gz.launch.py
```
