#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource


def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    robotino_bringup_path = get_package_share_directory('robotino_bringup')

    rviz_path = os.path.join(
        robotino_bringup_path, 'rviz', 'ros2.rviz'
    )

    return LaunchDescription([
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=[
                '-d', rviz_path
            ],
            output='screen',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(robotino_bringup_path, 'launch', 'robotino_gazebo.launch.py')
            )
        ),
        Node(
            package='teleop_twist_keyboard',
            executable='teleop_twist_keyboard',
            namespace='robotino',
            output='screen',
            prefix='xterm -e'
        )
    ])