FROM ros:iron-ros-core-jammy

RUN apt-get update \
    && apt-get install -y \
    wget curl unzip \
    lsb-release \
    mesa-utils \
    build-essential \
    && apt-get clean

# Get gazebo binaries
RUN echo "deb http://packages.osrfoundation.org/gazebo/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/gazebo-stable.list \
    && wget http://packages.osrfoundation.org/gazebo.key -O - | apt-key add - \
    && apt-get update \
    && apt-get install -y \
    gazebo \
    ros-iron-gazebo-ros-pkgs \
    python3-colcon-common-extensions python3-rosdep --no-install-recommends \
    && apt-get clean
RUN rosdep init && rosdep update

RUN curl -L https://github.com/osrf/gazebo_models/archive/refs/heads/master.zip -o /tmp/gazebo_models.zip \
    && unzip /tmp/gazebo_models.zip -d /tmp && mkdir -p ~/.gazebo/models/ && mv /tmp/gazebo_models-master/* ~/.gazebo/models/ \
    && rm -r /tmp/gazebo_models.zip

RUN mkdir -p /ros2_ws/src
COPY ./robotino_description /ros2_ws/src/robotino_description
COPY ./robotino_bringup /ros2_ws/src/robotino_bringup

WORKDIR /ros2_ws
RUN /bin/bash -c 'cd /ros2_ws/ \
    && source /opt/ros/iron/setup.bash \
    && rosdep install --from-paths src --ignore-src -r -y \
    && colcon build'

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
SHELL [ "/bin/bash", "-c" ]
ENTRYPOINT [ "/entrypoint.sh" ]
CMD [ "ros2", "launch", "robotino_bringup", "robotino_bringup.launch.py" ]
