#!/usr/bin/env python3

# Copyright 2025 tesollo
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
#    * Neither the name of the tesollo nor the names of its
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


import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration


class JointTrajectoryPublisher(Node):
    def __init__(self):
        super().__init__('joint_trajectory_publisher')
        self.publisher_ = self.create_publisher(
            JointTrajectory, '/dg5f_s_right/dg5f_s_right_controller/joint_trajectory', 10)
        self.timer = self.create_timer(2.0, self.timer_callback)
        self.joint_names = ["joint_1_1", "joint_1_2", "joint_1_3", "joint_1_4", "joint_2_1", "joint_2_2", "joint_2_3", "joint_2_4", "joint_3_1", "joint_3_2", "joint_3_3", "joint_3_4", "joint_4_1", "joint_4_2", "joint_4_3", "joint_4_4", "joint_5_1", "joint_5_2", "joint_5_3", "joint_5_4"]

        self.angles = [                       [0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0],

                       [0.0, 0.0, 1.4, 1.4,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0],

                       [0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 1.4, 1.4,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0],

                       [0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 1.4, 1.4,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0],

                       [0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 1.4, 1.4,
                        0.0, 0.0, 0.0, 0.0],

                       [0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 1.4, 1.4]]

        self.index = 0

    def timer_callback(self):
        message = JointTrajectory()
        message.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = self.angles[self.index]
        point.time_from_start = Duration(sec=2, nanosec=0)

        message.points.append(point)
        self.get_logger().info("JTC #{} publish: {}".format(
            self.index, self.angles[self.index]))
        self.publisher_.publish(message)

        self.index = (self.index + 1) % len(self.angles)


def main(args=None):
    rclpy.init(args=args)
    node = JointTrajectoryPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
