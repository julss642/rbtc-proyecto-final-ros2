from glob import glob
import os
from setuptools import find_packages, setup

package_name = 'rbtc_mission_manager'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=['setuptools', 'PyYAML'],
    zip_safe=True,
    maintainer='Juliana Solorza',
    maintainer_email='julss642@users.noreply.github.com',
    description='Servicio ROS 2 para misiones Nav2 desde waypoints YAML.',
    license='Apache-2.0',
    entry_points={'console_scripts': ['mission_manager = rbtc_mission_manager.mission_manager:main']},
)
