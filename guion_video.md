# Guion para el video de sustentación

El material se grabó sin audio para que puedan añadir sus voces y hacer la edición. Duración sugerida: 3 a 4 minutos. Pueden repartirse el relato entre Juliana y Alejandro.

## 1. Presentación — 15 s

**Imagen:** título del proyecto y breve vista del robot en Gazebo.  
**Decir:** “Somos Juliana Solorza y Alejandro Huertas. En este proyecto integramos la simulación y navegación autónoma de un robot diferencial con ROS 2 Humble, Gazebo y Nav2.”

## 2. Modelo y control — 30 s

**Imagen:** `02_gazebo_robot.mp4`; mostrar el robot y los obstáculos.  
**Decir:** “Partimos de una descripción propia en Xacro con base, ruedas, LiDAR e IMU. Probamos dos formas de controlar las ruedas: el plugin DiffDrive de Gazebo y `ros2_control` con `diff_drive_controller`. En ambos casos enviamos velocidad y observamos el desplazamiento y la odometría.”

## 3. Sensores y estimación — 25 s

**Imagen:** captura RViz o pantalla con los tópicos `/scan`, `/imu` y `/odometry/filtered`.  
**Decir:** “El LiDAR publica el escaneo del entorno y la IMU mide la orientación y la velocidad angular. `robot_localization` combina estas mediciones con la odometría de las ruedas mediante un EKF 2D. El resultado se publica en `/odometry/filtered` y en la transformación `odom` a `base_footprint`.”

## 4. Mapeo — 35 s

**Imagen:** primeros 35 segundos de `03_recorrido_SLAM_RViz.mp4` y después `04_mapa_final_RViz.png`.  
**Decir:** “Con SLAM Toolbox recorrimos el entorno mientras RViz mostraba el escaneo y el mapa que se iba construyendo. Al terminar guardamos el mapa en formato YAML y PGM, con una resolución de cinco centímetros por celda. También verificamos las transformaciones del robot.”

## 5. AMCL y planificación — 35 s

**Imagen:** `05_navegacion_mision_Nav2.mp4`; enseñar mapa, costmaps y trayectoria.  
**Decir:** “Después cargamos el mapa en Nav2. AMCL localizó el robot y los costmaps representaron los obstáculos. El planificador generó una ruta sobre el mapa y el controlador envió las velocidades al robot.”

## 6. Servicio de misión y resultado — 30 s

**Imagen:** terminar el clip de Nav2 con `06_waypoints_alcanzados.png`; incluir una sobreimpresión con `/start_mission` y el mensaje de misión completada.  
**Decir:** “Para automatizar el recorrido implementamos `/start_mission`. El nodo lee los puntos desde un archivo YAML y los entrega a Nav2 mediante `nav2_simple_commander`. La prueba final alcanzó los tres waypoints y terminó correctamente.”

## 7. Cierre — 10 s

**Imagen:** enlace del repositorio.  
**Decir:** “El código, la configuración, el mapa y las evidencias están disponibles en el repositorio de GitHub enlazado en el informe. Con esto mostramos desde el modelo y la integración de sensores hasta una misión autónoma ejecutada en simulación.”
