# Integration Contracts: Digital Twin Simulation Module

## Gazebo-ROS2 Interface Contracts

### Sensor Data Publishing
- **Topic**: `/sensor_data/laser_scan`
- **Message Type**: `sensor_msgs/LaserScan`
- **Purpose**: Publish simulated LiDAR data from Gazebo to ROS2

- **Topic**: `/sensor_data/depth_camera`
- **Message Type**: `sensor_msgs/Image` and `sensor_msgs/CameraInfo`
- **Purpose**: Publish depth camera image data from Gazebo to ROS2

- **Topic**: `/sensor_data/imu`
- **Message Type**: `sensor_msgs/Imu`
- **Purpose**: Publish simulated IMU data from Gazebo to ROS2

### Robot State Publishing
- **Topic**: `/joint_states`
- **Message Type**: `sensor_msgs/JointState`
- **Purpose**: Publish joint positions, velocities, and efforts from Gazebo simulation

- **Topic**: `/tf` and `/tf_static`
- **Message Type**: `tf2_msgs/TFMessage`
- **Purpose**: Publish coordinate transforms between robot frames

## Unity-ROS2 Bridge Contracts

### Communication Protocol
- **Protocol**: TCP/IP with JSON messaging
- **Purpose**: Enable communication between Unity visualizer and ROS2 system

### State Synchronization
- **Message Type**: Custom ROS2 messages for Unity visualization
- **Purpose**: Synchronize simulation state between Gazebo physics and Unity rendering

## Simulation Configuration Contracts

### World File Format
- **Format**: SDF (Simulation Description Format)
- **Purpose**: Define simulation environments with physics properties

### Robot Model Format
- **Format**: URDF (Unified Robot Description Format) / XACRO
- **Purpose**: Define robot kinematics, dynamics, and visual properties

## Quality Standards

### Performance Requirements
- Physics simulation should maintain real-time performance (1x speed)
- Visualization should maintain 30+ FPS for smooth experience
- Sensor data should be published at appropriate frequencies for the sensor type

### Accuracy Requirements
- Physics simulation should match real-world behavior within acceptable tolerances
- Sensor simulation should include realistic noise models
- Visual representation should accurately reflect physical state