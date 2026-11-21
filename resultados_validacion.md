# Registro de validación

Entorno usado: Ubuntu 22.04 (WSL), ROS 2 Humble y Gazebo Fortress.

- `colcon build --symlink-install`: compilación exitosa de `dif_bot_description`, `rbtc_bringup` y `rbtc_mission_manager`.
- URDF/Xacro: expansión correcta del modelo en configuración DiffDrive y configuración `ros2_control`.
- Sensores: `/scan` y `/imu` activos. El reloj del mundo se enlaza desde `/world/rbtc_world/clock` hacia `/clock`.
- Fusión: `robot_localization` publica `/odometry/filtered` y TF `odom → base_footprint`, usando odometría de ruedas e IMU con covarianzas finitas.
- SLAM: recorrido de exploración realizado; el mapa 223 × 223 celdas a 0,05 m/celda se guardó en YAML/PGM.
- Control: el plugin DiffDrive de Gazebo y el modo `ros2_control` movieron el robot y publicaron odometría.
- Nav2/AMCL: servidores activos y localización activa en RViz.
- Misión: `/start_mission` aceptó la solicitud. El nodo informó `MISIÓN COMPLETADA: todos los waypoints alcanzados.` con tres waypoints.

Las capturas y grabaciones de pantalla asociadas están en `evidencias/`.
