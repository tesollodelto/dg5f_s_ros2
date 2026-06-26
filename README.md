# DG5F-S ROS 2

[![CI](https://github.com/tesollodelto/dg5f_s_ros2/actions/workflows/ci.yml/badge.svg)](https://github.com/tesollodelto/dg5f_s_ros2/actions/workflows/ci.yml)
![ROS 2 Humble](https://img.shields.io/badge/ROS_2-Humble-blue?logo=ros)
![ROS 2 Jazzy](https://img.shields.io/badge/ROS_2-Jazzy-blue?logo=ros)

ROS 2 packages for the **Delto Gripper DG5F-S** (5-finger robotic hand, small version, left/right).

Supports both **20-DOF** and **15-DOF** variants.

## Packages

| Package | Description |
|---|---|
| `dg5f_s_description` | URDF/xacro model, meshes, and RViz display launch |
| `dg5f_s_driver` | ros2_control hardware driver and controller launch files |
| `dg5f_s_gz` | Gazebo simulation |
| `dg5f_s_moveit_config` | MoveIt 2 configuration (SRDF, planners, mock hardware) |

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
colcon build --packages-select dg5f_s_description dg5f_s_driver dg5f_s_gz dg5f_s_moveit_config
source install/setup.bash
```

## ⚠️ Before You Control

The `dg5f_s_driver` (ros2_control) operates in **Developer Mode**, which uses a custom protocol over Ethernet.
Before launching a hardware driver, set the gripper to **Developer Mode** using the DIP switch near the *LED Check Point*.

> **Note:** The DG5F-S switch/LED panel differs from the DG3F/DG5F button panel — it is a **DIP switch**, not the button/LED panel used by the other models.

<img src="./dg5f_s_driver/images/manual.png" width="400px"/>

| No. | System Mode | LED indication |
|---|---|---|
| ① | Operator Mode | White LEDs blink once · Socket Connect: Green LED On · Disconnect: Green LED Blinks |
| ② | **Developer Mode** (required for ros2_control) | White LEDs blink · Socket Connect: Green LED On · Disconnect: Green LED Blinks |
| ③ | Boot Mode | Red LED Blinks |
| ④ | Not used | — |

- **Operator Mode:** uses the product's internal controller and the Modbus Protocol (register map / provided UI).
- **Developer Mode:** lets you control the hand with a custom-developed controller, receiving per-joint information for direct joint control. **This is the mode ros2_control requires.**
- If there is an issue with switch operation or communication, the **red LED blinks**.

This applies only to real hardware launches; the mock-hardware, Gazebo, and MoveIt mock setups below do not require a gripper.

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

# PID controller — individual (one PidController per joint)
ros2 launch dg5f_s_driver dg5f_s_right_pid_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_left_pid_controller.launch.py

# PID controller — all-in-one (single grouped PidController)
ros2 launch dg5f_s_driver dg5f_s_right_pid_all_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_left_pid_all_controller.launch.py

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

# PID controller — individual (one PidController per joint)
ros2 launch dg5f_s_driver dg5f_s_15dof_right_pid_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_15dof_left_pid_controller.launch.py

# PID controller — all-in-one (single grouped PidController)
ros2 launch dg5f_s_driver dg5f_s_15dof_right_pid_all_controller.launch.py
ros2 launch dg5f_s_driver dg5f_s_15dof_left_pid_all_controller.launch.py

# Gazebo simulation
ros2 launch dg5f_s_gz dg5f_s_15dof_right_gz.launch.py
ros2 launch dg5f_s_gz dg5f_s_15dof_left_gz.launch.py
```

### Mock Hardware & MoveIt

```bash
# Mock hardware (no device required)
ros2 launch dg5f_s_driver dg5f_s_right_mock.launch.py
ros2 launch dg5f_s_driver dg5f_s_left_mock.launch.py

# MoveIt 20-DOF (mock hardware, default)
ros2 launch dg5f_s_moveit_config dg5f_s_right_moveit.launch.py
ros2 launch dg5f_s_moveit_config dg5f_s_left_moveit.launch.py

# MoveIt 15-DOF
ros2 launch dg5f_s_moveit_config dg5f_s_15dof_right_moveit.launch.py
ros2 launch dg5f_s_moveit_config dg5f_s_15dof_left_moveit.launch.py

# MoveIt (real hardware)
ros2 launch dg5f_s_moveit_config dg5f_s_right_moveit.launch.py use_mock:=false delto_ip:=169.254.186.72
```

## PID Controllers (Position → Effort)

Naming convention (consistent across all Delto drivers). `<ns>` is the driver namespace
(`dg5f_s_left`, `dg5f_s_right`, `dg5f_s_15dof_left`, `dg5f_s_15dof_right`):

| Variant | Config | Controllers | Reference Topic |
|---------|--------|-------------|-----------------|
| **Individual** (`pid`) | `<ns>_pid_controller.yaml` | one `pid_controller/PidController` per joint, named `<joint>_pospid` | `/<ns>/<joint>_pospid/reference` |
| **All-in-one** (`pid_all`) | `<ns>_pid_all_controller.yaml` | a single `pid_controller/PidController` named `joint_pospid` managing all joints | `/<ns>/joint_pospid/reference` |

Both take a `control_msgs/MultiDOFCommand` position reference and output effort. Gains are seeded from the JTC config (`p: 1.5`).

Test scripts: `<ns>_pid_test.py` (individual) and `<ns>_pid_all_test.py` (grouped), e.g.:

```bash
ros2 run dg5f_s_driver dg5f_s_left_pid_test.py
ros2 run dg5f_s_driver dg5f_s_left_pid_all_test.py
```
