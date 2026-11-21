#!/usr/bin/env python3
import math
import threading
import time

import yaml
import rclpy
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
from rclpy.node import Node
from std_srvs.srv import Trigger


class MissionManager(Node):
    def __init__(self):
        super().__init__('mission_manager')
        self.declare_parameter('waypoints_file', '')
        self.navigator = BasicNavigator()
        self.navigator.set_parameters([
            rclpy.parameter.Parameter('use_sim_time', value=True)])
        self._busy = False
        self._lock = threading.Lock()
        self._service = self.create_service(Trigger, '/start_mission', self._start)
        self.get_logger().info('Servicio /start_mission listo.')

    def _start(self, request, response):
        del request
        with self._lock:
            if self._busy:
                response.success = False
                response.message = 'Ya hay una misión en ejecución.'
                return response
            self._busy = True
        threading.Thread(target=self._run, daemon=True).start()
        response.success = True
        response.message = 'Misión aceptada. Consulta los resultados en la terminal.'
        return response

    def _run(self):
        try:
            path = self.get_parameter('waypoints_file').value
            with open(path, encoding='utf-8') as stream:
                mission = yaml.safe_load(stream)['mission']
            frame = mission.get('frame_id', 'map')
            poses = []
            for point in mission['waypoints']:
                pose = PoseStamped()
                pose.header.frame_id = frame
                pose.header.stamp = self.navigator.get_clock().now().to_msg()
                pose.pose.position.x = float(point['x'])
                pose.pose.position.y = float(point['y'])
                yaw = float(point.get('yaw', 0.0))
                pose.pose.orientation.z = math.sin(yaw / 2.0)
                pose.pose.orientation.w = math.cos(yaw / 2.0)
                poses.append(pose)
            self.get_logger().info(f'Iniciando misión: {len(poses)} waypoints.')
            initial_pose = PoseStamped()
            initial_pose.header.frame_id = frame
            initial_pose.header.stamp = self.navigator.get_clock().now().to_msg()
            initial_pose.pose.orientation.w = 1.0
            self.navigator.setInitialPose(initial_pose)
            self.navigator.waitUntilNav2Active()
            if not self.navigator.goThroughPoses(poses):
                self.get_logger().error('Nav2 rechazó la misión.')
                return
            last_feedback = 0.0
            while not self.navigator.isTaskComplete():
                feedback = self.navigator.getFeedback()
                now = time.monotonic()
                if feedback and now - last_feedback >= 1.0:
                    self.get_logger().info(
                        f'Waypoints restantes: {feedback.number_of_poses_remaining}')
                    last_feedback = now
            result = self.navigator.getResult()
            if result == TaskResult.SUCCEEDED:
                self.get_logger().info('MISIÓN COMPLETADA: todos los waypoints alcanzados.')
            elif result == TaskResult.CANCELED:
                self.get_logger().warning('Misión cancelada.')
            else:
                self.get_logger().error('Nav2 terminó la misión con fallo.')
        except Exception as exc:
            self.get_logger().error(f'Error ejecutando la misión: {exc}')
        finally:
            with self._lock:
                self._busy = False


def main():
    rclpy.init()
    manager = MissionManager()
    executor = rclpy.executors.MultiThreadedExecutor(num_threads=2)
    executor.add_node(manager)
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        manager.navigator.destroy_node()
        manager.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
