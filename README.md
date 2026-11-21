# Proyecto final: navegación autónoma con ROS 2

Implementación desde cero de un robot diferencial simulado con ROS 2 Humble, Gazebo Fortress y Nav2. El proyecto integra odometría, IMU, EKF, SLAM, AMCL, planificación y una misión que se inicia mediante un servicio ROS.

**Integrantes:** Juliana Solorza y Alejandro Huertas.

## Paquetes

- `dif_bot_description`: robot diferencial en Xacro, sensores LiDAR e IMU, plugin de control de Gazebo y alternativa basada en `ros2_control`.
- `rbtc_bringup`: mundo con obstáculos, puentes Gazebo–ROS, EKF, lanzamientos para SLAM, localización, navegación y RViz.
- `rbtc_mission_manager`: servicio `/start_mission`, ejecución de waypoints YAML con `nav2_simple_commander`.

## Requisitos

- Ubuntu 22.04 y ROS 2 Humble.
- Gazebo Fortress con `ros_gz`.
- Nav2, SLAM Toolbox, `robot_localization`, `xacro`, `ros2_control` y `gz_ros2_control`.

En WSL, iniciar Gazebo con renderizado por software para habilitar el LiDAR GPU:

```bash
export LIBGL_ALWAYS_SOFTWARE=1
```

## Compilar

```bash
source /opt/ros/humble/setup.bash
cd ~/rbtc_proyecto_final
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

## Flujo de trabajo

Cada comando se ejecuta en una terminal independiente, con los dos `source` anteriores aplicados.

1. Iniciar el mundo, el robot, los sensores, el EKF y los puentes:

   ```bash
   ros2 launch rbtc_bringup simulation.launch.py
   ```

2. Iniciar SLAM y visualizar los datos en RViz:

   ```bash
   ros2 launch rbtc_bringup slam.launch.py
   rviz2 -d $(ros2 pkg prefix rbtc_bringup)/share/rbtc_bringup/rviz/rbtc_default.rviz
   ```

3. Explorar el entorno o conducir manualmente. El recorrido reproducible está en `scripts/explore_loop.py`:

   ```bash
   python3 scripts/explore_loop.py
   ```

4. Guardar el mapa y detener SLAM antes de iniciar Nav2:

   ```bash
   ros2 run nav2_map_server map_saver_cli -f src/rbtc_bringup/maps/rbtc_map
   ```

5. Iniciar navegación y el administrador de misiones:

   ```bash
   ros2 launch rbtc_bringup navigation.launch.py
   ros2 launch rbtc_bringup mission.launch.py
   ros2 service call /start_mission std_srvs/srv/Trigger "{}"
   ```

Los puntos están en `src/rbtc_mission_manager/config/waypoints.yaml`. Se usan como coordenadas del marco `map` y pueden editarse antes de solicitar la misión.

## Comparación de control diferencial

El lanzamiento principal emplea el plugin DiffDrive de Gazebo, que recibe `/cmd_vel` y publica `/wheel/odometry`. La alternativa `simulation_ros2_control.launch.py` activa `gz_ros2_control`, `joint_state_broadcaster` y `diff_drive_controller`; el controlador recibe `/diff_drive_controller/cmd_vel_unstamped` y publica `/diff_drive_controller/odom`. Ambos modos se activaron y desplazaron el robot durante la validación.

## Verificaciones registradas

- Compilación de los tres paquetes con `colcon build --symlink-install`.
- Expansión Xacro y validación URDF del robot.
- Movimiento y odometría con DiffDrive de Gazebo y con `ros2_control`.
- Datos de `/scan` y `/imu`; fusión de `/wheel/odometry_cov` y `/imu_cov` mediante `robot_localization`.
- Mapa 2D guardado en `rbtc_bringup/maps/rbtc_map.yaml` y `rbtc_map.pgm`.
- Nav2 y AMCL activos; el servicio `/start_mission` inició y completó los tres waypoints.

El archivo `evidencias/` contiene capturas y grabaciones sin audio del proceso. Se puede añadir narración en la edición del video.
