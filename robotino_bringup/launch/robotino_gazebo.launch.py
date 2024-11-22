#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition

import xacro

def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time', default='false')
    xacro_file_name = 'robotino_platform_kinect.urdf.xacro'
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    xacro_file = os.path.join(
        get_package_share_directory('robotino_description'),
        'urdf', xacro_file_name
    )
    robot_description_config = xacro.process_file(xacro_file)
    robot_desc = robot_description_config.toxml()
    model_ns = 'robotino'

    default_world_file = os.path.join(
        get_package_share_directory('robotino_description'),
        'worlds', 'playground.world'
    )

    world_file = LaunchConfiguration('world_file')

    return LaunchDescription([
        DeclareLaunchArgument(
            'world_file',
            default_value=default_world_file,
            description='Path to the world file to load in Gazebo'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            namespace=model_ns,
            output='screen',
            parameters=[{'use_sim_time': use_sim_time, 'robot_description': robot_desc}],
            arguments=[robot_desc]
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher',
            name='joint_state_publisher',
            namespace=model_ns,
            output='screen',
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
            ),
            launch_arguments={'world': world_file,
                              'verbose': 'true',
                              'extra_gazebo_args': 'verbose'}.items()
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
            ),
            launch_arguments={'verbose': 'true'}.items(),
            condition=IfCondition(LaunchConfiguration('gui'))
        ),

        Node(
            package='robotino_bringup',
            executable='spawn_robotino',
            arguments=[robot_desc, model_ns],
            output='screen'
        )
    ])
