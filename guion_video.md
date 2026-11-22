# Guion de voz para los videos

Las grabaciones son silenciosas para que puedan añadir voces y música en la edición. Este guion está separado según los tres clips incluidos en `evidencias/`. Pueden repartirse las intervenciones entre Juliana y Alejandro. Ajusten las pausas a lo que se vea en su edición.

## Video 1 — Simulación en Gazebo

**Archivo:** `02_gazebo_robot.mp4` · aproximadamente 20 segundos.

**0:00–0:05 — Mundo y robot**  
“Aquí se observa el mundo de prueba creado en Gazebo, con el robot diferencial y dos obstáculos. El modelo se describe con Xacro e incluye ruedas, LiDAR e IMU.”

**0:05–0:13 — Control**  
“Probamos el movimiento con el plugin DiffDrive de Gazebo, que recibe `/cmd_vel` y genera `/wheel/odometry`. También activamos la alternativa `ros2_control` con `diff_drive_controller`; ambas configuraciones movieron el robot y publicaron odometría.”

**0:13–0:20 — Cierre del clip**  
“Esta simulación es la base para probar la estimación de movimiento, el mapeo y la navegación antes de llevar el sistema a un robot físico.”

## Video 2 — Exploración y mapa en RViz

**Archivo:** `03_recorrido_SLAM_RViz.mp4` · 75 segundos. Si el video final se recorta, conserva el recorrido y el mapa que aparece en pantalla.

**0:00–0:12 — Inicio del recorrido**  
“Con el mundo en marcha, iniciamos SLAM Toolbox y hacemos un recorrido controlado. El LiDAR publica `/scan`; el EKF combina la odometría de ruedas y la IMU para estimar el movimiento.”

**0:12–0:35 — Escaneo y construcción**  
“En RViz se ve cómo las lecturas del LiDAR se incorporan al mapa. Las zonas ocupadas corresponden a obstáculos detectados; las zonas libres son espacio observado y las áreas no recorridas pueden permanecer desconocidas.”

**0:35–0:55 — Interpretación**  
“SLAM estima simultáneamente la trayectoria y el mapa. La calidad depende de la cobertura y de mantener coherentes el reloj simulado y las transformaciones entre `map`, `odom` y el robot.”

**0:55–1:15 — Mapa guardado**  
“Al terminar guardamos el mapa en formatos YAML y PGM, con resolución de cinco centímetros por celda. Este archivo se reutiliza después para la localización y la navegación.”

## Video 3 — Nav2, AMCL y misión

**Archivo:** `05_navegacion_mision_Nav2.mp4` · aproximadamente 30 segundos.

**0:00–0:08 — Localización**  
“Cargamos el mapa guardado en Nav2. AMCL estima la pose del robot a partir del LiDAR y el mapa. En RViz vemos el estado de localización y los costmaps que representan los obstáculos.”

**0:08–0:18 — Planificación**  
“El planificador calcula una ruta hacia los objetivos y el controlador envía velocidades al robot. La ruta se ejecuta en el marco `map` usando la odometría filtrada para el movimiento continuo.”

**0:18–0:25 — Servicio propio**  
“La misión se inicia mediante el servicio ROS `/start_mission`. El nodo lee tres waypoints de un archivo YAML y los envía a Nav2 con `nav2_simple_commander`.”

**0:25–0:30 — Resultado**  
“La ejecución validada alcanzó los tres waypoints y terminó correctamente. El código, el mapa y las evidencias están enlazados en el repositorio incluido en el informe.”

## Cierre opcional en pantalla

Mostrar el enlace `https://github.com/julss642/rbtc-proyecto-final-ros2` y la captura `06_waypoints_alcanzados.png`. No narren resultados adicionales que no aparezcan en las evidencias.
