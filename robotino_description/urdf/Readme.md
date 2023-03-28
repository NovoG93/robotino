# Convert xacro to sdf

1. `cd robotino_description/urdf`
2. `xacro robotino_platform_kinect.urdf.xacro > robotino_platform_kinect.urdf`
3. `cd ../models && gz sdf -p ../urdf/robotino_platform_kinect.urdf > robotino_platform_kinect.sdf`