import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    # Get the urdf file
    urdf_file_name = 'robotino_platform_kinect.sdf'
    urdf = os.path.join(
        get_package_share_directory('robotino_description'),
        'models', 'robotino_description', urdf_file_name
    )    

    start_gazebo_ros_spawner_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-file', urdf,
            '-entity', 'robotino',
            '-timeout', '90'
        ],
        output='screen',
    )

    ld = LaunchDescription()
    # Add any conditioned actions
    ld.add_action(start_gazebo_ros_spawner_cmd)

    return ld