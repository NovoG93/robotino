#!/bin/bash

source "/opt/ros/$ROS_DISTRO/setup.bash" --

if [ -e /ros2_ws/ ]; then
    source /ros2_ws/install/setup.bash
else
    echo "Error: ROS 2 workspace not found at /ros2_ws."
    exit 1
fi

exec "$@"