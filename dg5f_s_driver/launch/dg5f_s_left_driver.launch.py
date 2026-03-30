# Copyright 2025 TESOLLO
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#
#    * Neither the name of the TESOLLO nor the names of its
#      contributors may be used to endorse or promote products derived from
#      this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from launch import LaunchDescription
from launch.substitutions import (
    Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
)
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    ns = "dg5f_s_left"

    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            "delto_ip",
            default_value="169.254.186.73",
            description="IP address for gripper"
        )
    )
    delto_ip = LaunchConfiguration("delto_ip")

    declared_arguments.append(
        DeclareLaunchArgument(
            "delto_port",
            default_value="502",
            description="Port for gripper"
        )
    )
    delto_port = LaunchConfiguration("delto_port")

    declared_arguments.append(
        DeclareLaunchArgument(
            "fingertip_sensor",
            default_value="false",
            description="Enable fingertip F/T sensor"
        )
    )
    fingertip_sensor = LaunchConfiguration("fingertip_sensor")

    declared_arguments.append(
        DeclareLaunchArgument(
            "ft_broadcaster",
            default_value="false",
            description="Enable F/T sensor broadcaster (force/torque only, not tactile)"
        )
    )
    ft_broadcaster = LaunchConfiguration("ft_broadcaster")


    declared_arguments.append(
        DeclareLaunchArgument(
            "io",
            default_value="false",
            description="Enable GPIO"
        )
    )
    io = LaunchConfiguration("io")

    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name="xacro")]),
            " ",
            PathJoinSubstitution(
                [FindPackageShare("dg5f_s_driver"), "urdf",
                 "dg5f_s_left_ros2_control.xacro"]
            ),
            " ", "delto_ip:=", delto_ip,
            " ", "delto_port:=", delto_port,
            " ", "fingertip_sensor:=", fingertip_sensor,
            " ", "io:=", io,
        ]
    )

    robot_description = {"robot_description": robot_description_content}

    robot_controllers = PathJoinSubstitution(
        [FindPackageShare("dg5f_s_driver"), "config",
         "dg5f_s_left_controller.yaml"]
    )

    ft_broadcaster_config = PathJoinSubstitution(
        [FindPackageShare("dg5f_s_driver"), "config",
         "dg5f_s_left_ft_broadcaster.yaml"]
    )

    control_node = Node(
        package="controller_manager",
        executable="ros2_control_node",
        namespace=ns,
        parameters=[robot_controllers],
        remappings=[
            ("~/robot_description", "/" + ns + "/robot_description"),
        ],
        output="screen",
        condition=UnlessCondition(ft_broadcaster),
    )

    control_node_with_ft = Node(
        package="controller_manager",
        executable="ros2_control_node",
        namespace=ns,
        parameters=[robot_controllers, ft_broadcaster_config],
        remappings=[
            ("~/robot_description", "/" + ns + "/robot_description"),
        ],
        output="screen",
        condition=IfCondition(ft_broadcaster),
    )

    robot_state_pub_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        namespace=ns,
        output="screen",
        parameters=[robot_description],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "-c", "/" + ns + "/controller_manager"],
        output="screen",
    )

    delto_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["dg5f_s_left_controller", "-c", "/" + ns + "/controller_manager"],
        output="screen",
    )

    fingertip_broadcasters = []
    for i in range(1, 6):
        fingertip_broadcasters.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=[f"fingertip_{i}_broadcaster",
                           "-c", "/" + ns + "/controller_manager"],
                output="screen",
                condition=IfCondition(ft_broadcaster),
            )
        )

    nodes = [
        control_node,
        control_node_with_ft,
        robot_state_pub_node,
        joint_state_broadcaster_spawner,
        delto_controller_spawner,
    ] + fingertip_broadcasters

    return LaunchDescription(declared_arguments + nodes)
