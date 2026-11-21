#!/usr/bin/env python3
"""Drive one safe rectangular loop to collect scans for SLAM."""
import time

import rclpy
from geometry_msgs.msg import Twist
from rclpy.node import Node


class Explorer(Node):
    def __init__(self):
        super().__init__('sl am_exploration_demo'.replace(' ', ''))
        self.publisher = self.create_publisher(Twist, '/cmd_vel', 10)

    def segment(self, linear, angular, duration, label):
        self.get_logger().info(label)
        command = Twist()
        command.linear.x = linear
        command.angular.z = angular
        end = time.monotonic() + duration
        while rclpy.ok() and time.monotonic() < end:
            command = Twist()
            command.linear.x = linear
            command.angular.z = angular
            self.publisher.publish(command)
            rclpy.spin_once(self, timeout_sec=0.01)
            time.sleep(0.09)
        self.publisher.publish(Twist())
        time.sleep(0.4)


def main():
    rclpy.init()
    explorer = Explorer()
    time.sleep(1.0)
    for index in range(4):
        explorer.segment(0.20, 0.0, 15.0, f'Lado {index + 1}/4: avance recto.')
        explorer.segment(0.0, 0.60, 2.62, 'Giro de 90 grados.')
    explorer.publisher.publish(Twist())
    explorer.get_logger().info('Recorrido de exploración terminado.')
    explorer.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
