# Copyright 2025 tesollo
#
# BSD-3-Clause license

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, RegisterEventHandler
from launch.conditions import IfCondition
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, FindExecutable, PathJoinSubstitution, LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
import os


def generate_launch_description():
    declared_arguments = []
    declared_arguments.append(
        DeclareLaunchArgument("gui", default_value="false", description="Start RViz2 automatically.")
    )
    gui = LaunchConfiguration("gui")

    pkg_description = FindPackageShare("dg5f_s_description").find("dg5f_s_description")
    model_path = os.path.dirname(pkg_description)

    if 'IGN_GAZEBO_RESOURCE_PATH' in os.environ:
        os.environ['IGN_GAZEBO_RESOURCE_PATH'] = os.environ['IGN_GAZEBO_RESOURCE_PATH'] + ':' + model_path
    else:
        os.environ['IGN_GAZEBO_RESOURCE_PATH'] = model_path

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [FindPackageShare("ros_gz_sim"), "/launch/gz_sim.launch.py"]
        ),
        launch_arguments={"gz_args": " -r empty.sdf -v 0"}.items(),
    )

    robot_description_content1 = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([FindPackageShare("dg5f_s_gz"), "urdf", "dg5f_s_right_gz.xacro"]),
    ])
    robot_description_content2 = Command([
        PathJoinSubstitution([FindExecutable(name="xacro")]),
        " ",
        PathJoinSubstitution([FindPackageShare("dg5f_s_gz"), "urdf", "dg5f_s_right_gz.xacro"]),
    ])

    robot_description1 = {"robot_description": robot_description_content1}
    robot_description2 = {"robot_description": robot_description_content2}

    robot_controllers = PathJoinSubstitution([
        FindPackageShare("dg5f_s_gz"), "config", "dg5f_s_right_gz_controller.yaml",
    ])

    node_robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description1],
    )
    node_robot_state_other_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        output="screen",
        parameters=[robot_description2],
        remappings=[("/robot_description", "/robot_description_other")],
    )

    gz_spawn_entity = Node(
        package="ros_gz_sim",
        executable="create",
        output="screen",
        arguments=[
            "-topic", "/robot_description",
            "-name", "dg5f_s_right",
            "-allow_renaming", "true",
            "-x", "0.0", "-y", "0.0", "-z", "0.0",
        ],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster"],
        output="screen",
    )

    joint_trajectory_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_trajectory_controller", '--param-file', robot_controllers],
    )

    nodes = [
        gazebo,
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=gz_spawn_entity,
                on_exit=[joint_state_broadcaster_spawner],
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=joint_state_broadcaster_spawner,
                on_exit=[joint_trajectory_controller_spawner],
            )
        ),
        node_robot_state_publisher,
        gz_spawn_entity,
        node_robot_state_other_publisher,
    ]

    return LaunchDescription(nodes)
