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
from control_msgs.msg import MultiDOFCommand


def d2r(deg):
    return deg * 3.141592 / 180.0


angles = [
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 0.0, 0.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
]

global index
index = 0


class PIDControlTestAll(Node):
    def __init__(self):
        super().__init__('pid_control_test_all')

        self.joint_names = ["joint_1_1",
                            "joint_1_2",
                            "joint_1_3",
                            "joint_2_1",
                            "joint_2_2",
                            "joint_2_3",
                            "joint_3_1",
                            "joint_3_2",
                            "joint_3_3",
                            "joint_4_1",
                            "joint_4_2",
                            "joint_4_3",
                            "joint_5_1",
                            "joint_5_2",
                            "joint_5_3"]

        topic_name = '/dg5f_s_15dof_right/joint_pospid/reference'
        self.joint_publisher = self.create_publisher(
            MultiDOFCommand, topic_name, 10)
        self.get_logger().info(f'Created publisher for {topic_name}')

        self.timer = self.create_timer(5.0, self.timer_callback)


    def timer_callback(self):
        global index
        msg = MultiDOFCommand()
        msg.dof_names = self.joint_names
        position = angles[index % len(angles)]
        msg.values = position
        msg.values_dot = [0.0] * len(position)
        index = index + 1
        self.joint_publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PIDControlTestAll()
    try:
        node.get_logger().info('Starting PID control test for ALL joints (grouped controller)...')
        node.get_logger().info('Press Ctrl+C to stop')
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Test stopped by user')
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
