#!/usr/bin/env python3
"""Attach finite measurement covariances to simulator sensor messages."""
import rclpy
from nav_msgs.msg import Odometry
from rclpy.node import Node
from sensor_msgs.msg import Imu


class CovarianceRelay(Node):
    def __init__(self):
        super().__init__('sensor_covariance_relay')
        self.odom_pub = self.create_publisher(Odometry, '/wheel/odometry_cov', 10)
        self.imu_pub = self.create_publisher(Imu, '/imu_cov', 10)
        self.create_subscription(Odometry, '/wheel/odometry', self.odom_cb, 10)
        self.create_subscription(Imu, '/imu', self.imu_cb, 10)

    def odom_cb(self, msg):
        msg.pose.covariance[0] = 0.02
        msg.pose.covariance[7] = 0.02
        msg.pose.covariance[35] = 0.03
        msg.twist.covariance[0] = 0.02
        msg.twist.covariance[7] = 0.03
        msg.twist.covariance[35] = 0.03
        self.odom_pub.publish(msg)

    def imu_cb(self, msg):
        msg.orientation_covariance[8] = 0.03
        msg.angular_velocity_covariance[8] = 0.02
        msg.linear_acceleration_covariance[0] = 0.05
        msg.linear_acceleration_covariance[4] = 0.05
        msg.linear_acceleration_covariance[8] = 0.08
        self.imu_pub.publish(msg)


def main():
    rclpy.init()
    node = CovarianceRelay()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
