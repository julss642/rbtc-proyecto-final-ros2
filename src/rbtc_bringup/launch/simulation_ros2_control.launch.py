import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
import xacro


def generate_launch_description():
    bringup = get_package_share_directory('rbtc_bringup')
    description = get_package_share_directory('dif_bot_description')
    gz_share = get_package_share_directory('ros_gz_sim')
    model = os.path.join(description, 'urdf', 'dif_bot.urdf.xacro')
    robot_description = xacro.process_file(model, mappings={'use_ros2_control': 'true'}).toxml()
    world = os.path.join(bringup, 'worlds', 'rbtc_world.sdf')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz_share, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items())
    rsp = Node(package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}], output='screen')
    bridge = Node(package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': os.path.join(bringup, 'config', 'bridge.yaml'), 'use_sim_time': True}],
        output='screen')
    spawn = Node(package='ros_gz_sim', executable='create',
        arguments=['-name','dif_bot','-topic','/robot_description','-x','0','-y','0','-z','0.12'],
        output='screen')
    broadcaster = Node(package='controller_manager', executable='spawner',
        arguments=['joint_state_broadcaster', '--controller-manager', '/controller_manager'], output='screen')
    diff_drive = Node(package='controller_manager', executable='spawner',
        arguments=['diff_drive_controller', '--controller-manager', '/controller_manager'], output='screen')
    return LaunchDescription([gazebo, rsp, bridge, TimerAction(period=3.0, actions=[spawn]),
        TimerAction(period=8.0, actions=[broadcaster, diff_drive])])
