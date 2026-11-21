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
    world = os.path.join(bringup, 'worlds', 'rbtc_world.sdf')
    model = os.path.join(description, 'urdf', 'dif_bot.urdf.xacro')
    robot_description = xacro.process_file(model).toxml()

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gz_share, 'launch', 'gz_sim.launch.py')),
        launch_arguments={'gz_args': f'-r {world}'}.items())
    state_publisher = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description, 'use_sim_time': True}],
        output='screen')
    spawn = Node(
        package='ros_gz_sim', executable='create',
        arguments=['-name', 'dif_bot', '-topic', '/robot_description', '-x', '0', '-y', '0', '-z', '0.12'],
        output='screen')
    bridge = Node(
        package='ros_gz_bridge', executable='parameter_bridge',
        parameters=[{'config_file': os.path.join(bringup, 'config', 'bridge.yaml'),
                     'use_sim_time': True}], output='screen')
    ekf = Node(
        package='robot_localization', executable='ekf_node', name='ekf_filter_node',
        parameters=[os.path.join(bringup, 'config', 'ekf.yaml'), {'use_sim_time': True}],
        output='screen')
    covariance_relay = Node(
        package='rbtc_bringup', executable='sensor_covariance.py',
        parameters=[{'use_sim_time': True}], output='screen')
    imu_frame = Node(package='tf2_ros', executable='static_transform_publisher',
        arguments=['--x','0','--y','0','--z','0.23','--yaw','0','--pitch','0','--roll','0',
                   '--frame-id','base_footprint','--child-frame-id','dif_bot/base_footprint/imu'])
    lidar_frame = Node(package='tf2_ros', executable='static_transform_publisher',
        arguments=['--x','0.05','--y','0','--z','0.245','--yaw','0','--pitch','0','--roll','0',
                   '--frame-id','base_footprint','--child-frame-id','dif_bot/base_footprint/lidar'])
    return LaunchDescription([
        gazebo, state_publisher, bridge, imu_frame, lidar_frame,
        TimerAction(period=3.0, actions=[spawn]), covariance_relay, ekf])
