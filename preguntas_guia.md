# Respuestas a las preguntas de la guía

## Comparación de controladores

**¿Qué controlador genera la odometría en cada caso?** En la configuración DiffDrive, el plugin de Gazebo estima la odometría a partir de las ruedas simuladas y la publica en `/wheel/odometry`. Con `ros2_control`, `diff_drive_controller` integra el movimiento de las articulaciones y publica `/diff_drive_controller/odom`.

**¿Qué diferencias se observan en estabilidad y latencia?** En las pruebas ambos modos desplazaron el robot y publicaron odometría. No se midió latencia ni se hizo una prueba prolongada de estabilidad; por ello no se puede afirmar cuantitativamente que uno sea más rápido o estable. DiffDrive requiere menos configuración en Gazebo. `ros2_control` añade la activación del controlador, pero separa el controlador de las interfaces de hardware.

**¿Cuál enfoque es más adecuado para un robot real?** `ros2_control` es la opción más adaptable a hardware real porque permite conectar controladores con interfaces de motores y encoders. Para llevarlo al robot todavía hay que integrar y validar sus drivers, calibrar ruedas y medir latencia. DiffDrive es un plugin de simulación.

## EKF

**¿Qué sensores se fusionan?** Odometría de ruedas (`/wheel/odometry_cov`) e IMU (`/imu_cov`), configuradas en modo 2D.

**¿Qué frame publica el EKF?** Publica `/odometry/filtered` y la transformación dinámica `odom → base_footprint`.

**¿Qué ocurre si se desactiva la IMU?** El EKF puede seguir con la odometría de ruedas, pero pierde la medición independiente de yaw y velocidad angular. La orientación queda más expuesta al error acumulado de las ruedas y puede degradarse la estimación usada por SLAM.

## SLAM

**¿Qué resolución tiene el mapa?** 0,05 m por celda (5 cm/celda); el mapa guardado tiene 223 × 223 celdas.

**¿Cómo afecta la velocidad del robot al SLAM?** A mayor velocidad o aceleración, aumenta el desplazamiento entre escaneos y puede empeorar su correspondencia, deformando el mapa. Una velocidad moderada y giros suaves ayudan a solapar lecturas, con el costo de tardar más.

## AMCL

**¿Qué ocurre si el robot inicia en una pose incorrecta?** AMCL comienza con partículas alrededor de una ubicación equivocada. Puede corregirse si el mapa y las lecturas distinguen la pose al moverse, pero también puede quedar mal localizado. En ese caso `map → odom` es incorrecta y Nav2 planea desde una pose falsa. Hay que proporcionar una pose inicial razonable en RViz o desde la aplicación.

**¿Cómo afecta el ruido del láser?** Las lecturas espurias pueden introducir obstáculos falsos, deformar el mapa y reducir la precisión de AMCL; también afectan los costmaps. Filtrar mediciones y limitar velocidad/giros reduce su efecto.

## Nav2

**¿Qué planner se usa por defecto?** `nav2_navfn_planner/NavfnPlanner`, bajo el identificador `GridBased` en `nav2_params.yaml`.

**¿Qué comportamiento de recuperación se ejecuta?** El árbol predeterminado de navegación por múltiples poses contempla replanificación y recuperación; los comportamientos configurados incluyen limpiar costmaps, `Spin`, `Wait` y `BackUp` (además de `DriveOnHeading` y `AssistedTeleop`). La misión validada terminó con éxito, así que no afirmamos que una recuperación se haya disparado durante esa ejecución.
