import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    package = get_package_share_directory('rbtc_mission_manager')
    return LaunchDescription([Node(
        package='rbtc_mission_manager', executable='mission_manager', output='screen',
        parameters=[{'waypoints_file': os.path.join(package, 'config', 'waypoints.yaml'),
                    'use_sim_time': True}])])
