import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():
    nav2 = get_package_share_directory('nav2_bringup')
    bringup = get_package_share_directory('rbtc_bringup')
    return LaunchDescription([IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2, 'launch', 'bringup_launch.py')),
        launch_arguments={
            'use_sim_time': 'true',
            'map': os.path.join(bringup, 'maps', 'rbtc_map.yaml'),
            'params_file': os.path.join(bringup, 'config', 'nav2_params.yaml'),
            'autostart': 'true',
        }.items())])
