---
title: Physics Simulation with Gazebo
sidebar_position: 1
---

# Physics Simulation with Gazebo

This chapter covers simulating gravity, collisions, joint dynamics, world files, and integrating ROS 2 with Gazebo for humanoid robots.

## Learning Objectives

By the end of this chapter, you will be able to:
- Set up a physics simulation in Gazebo for humanoid robots
- Configure gravity and collision properties accurately
- Create and customize world files for different simulation scenarios
- Integrate Gazebo with ROS 2 for humanoid robot simulation

## Introduction

Physics simulation is the foundation of any digital twin, providing the realistic environment needed for safe testing before real-world deployment. Gazebo provides a robust physics engine that enables accurate simulation of real-world physics phenomena.

## Prerequisites

Before diving into physics simulation with Gazebo, ensure you have a solid understanding of ROS 2 fundamentals covered in Module 1. Specifically, you should be familiar with:
- ROS 2 nodes, topics, and services
- The concept of DDS and middleware
- How to create and configure ROS 2 packages
- Basic rclpy usage for Python-based ROS 2 nodes

If you need a refresher, please review [Module 1: The Robotic Nervous System (ROS 2)](/docs/module-1/chapter-1-ros2-architecture).

## Setting Up Gazebo for Humanoid Robots

Gazebo provides a comprehensive physics simulation environment that accurately models real-world physics including gravity, collisions, and joint dynamics. For humanoid robots, this means:

- Gravity affects the robot realistically
- Collision detection prevents parts from intersecting
- Joint constraints limit movement to realistic ranges
- Forces and torques can be applied to simulate actuators

## Configuring Gravity and Collisions

In Gazebo, gravity is enabled by default and can be configured in the world file. For humanoid robots, it's important to ensure that:

- Gravity is set to realistic values (typically 9.81 m/s²)
- Collision meshes are properly defined for each link
- Inertial properties are accurately specified

### Gravity Configuration Examples

Gravity can be configured in your world file using the following SDF format:

```xml
<sdf version="1.7">
  <world name="default">
    <!-- Set global gravity -->
    <gravity>0 0 -9.8</gravity>

    <!-- Your models and other elements -->
  </world>
</sdf>
```

You can also modify gravity during runtime using Gazebo services:

```bash
# Change gravity to zero (simulate microgravity)
rosservice call /gazebo/set_gravity "gravity: {x: 0.0, y: 0.0, z: 0.0}"

# Change gravity to simulate moon gravity (1/6 of Earth)
rosservice call /gazebo/set_gravity "gravity: {x: 0.0, y: 0.0, z: -1.63}"
```

### Collision Configuration

For humanoid robots, proper collision detection requires:

1. **Collision meshes**: Define simple geometric shapes or detailed meshes for collision detection
2. **Inertial properties**: Accurately model mass distribution
3. **Surface properties**: Configure friction and restitution coefficients

Example collision and inertial configuration in URDF:

```xml
<link name="link_name">
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0"/>
    <geometry>
      <capsule length="0.1" radius="0.05"/>
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0"/>
    <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01"/>
  </inertial>
</link>
```

## Creating Custom World Files

World files in Gazebo define the environment in which the simulation takes place. These files use the Simulation Description Format (SDF) and provide the physics properties, lighting, and objects for your simulation. For humanoid robot applications, you might want to create:

- Indoor environments with furniture and obstacles
- Outdoor terrains with different surfaces
- Testing scenarios with specific challenges

### World File Structure

A basic world file includes:

- Global physics parameters (gravity, solver settings)
- Light sources (sun, directional, point lights)
- Models and their initial positions
- Plugins for additional functionality

Example world file structure:

```xml
<?xml version="1.0" ?>
<sdf version="1.7">
  <world name="humanoid_world">
    <!-- Physics parameters -->
    <physics type="ode">
      <gravity>0 0 -9.8</gravity>
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1.0</real_time_factor>
    </physics>

    <!-- Light sources -->
    <light name="sun" type="directional">
      <cast_shadows>true</cast_shadows>
      <pose>0 0 10 0 0 0</pose>
      <diffuse>0.8 0.8 0.8 1</diffuse>
      <specular>0.2 0.2 0.2 1</specular>
      <attenuation>
        <range>1000</range>
        <constant>0.9</constant>
        <linear>0.01</linear>
        <quadratic>0.001</quadratic>
      </attenuation>
      <direction>-0.4 0.2 -1.0</direction>
    </light>

    <!-- Include models -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <include>
      <uri>model://sun</uri>
    </include>

    <!-- Place your robot -->
    <include>
      <uri>model://my_humanoid_robot</uri>
      <pose>0 0 1 0 0 0</pose>
    </include>

    <!-- Static objects -->
    <model name="table">
      <pose>2 0 0 0 0 0</pose>
      <link name="link">
        <collision name="collision">
          <geometry>
            <box>
              <size>1 0.8 0.8</size>
            </box>
          </geometry>
        </collision>
        <visual name="visual">
          <geometry>
            <box>
              <size>1 0.8 0.8</size>
            </box>
          </geometry>
        </visual>
        <inertial>
          <mass>10</mass>
          <inertia>
            <ixx>1</ixx>
            <ixy>0</ixy>
            <ixz>0</ixz>
            <iyy>1</iyy>
            <iyz>0</iyz>
            <izz>1</izz>
          </inertia>
        </inertial>
      </link>
    </model>
  </world>
</sdf>
```

### Physics Configuration

The physics engine configuration affects simulation accuracy and performance:

- **Max step size**: Smaller values increase accuracy but decrease performance
- **Real time factor**: Controls how fast the simulation runs relative to real time
- **ODE solver parameters**: Adjust for stability and performance

### Model Inclusion

World files can include pre-built models from the Gazebo model database or custom models:

```xml
<!-- Include a model from the database -->
<include>
  <uri>model://ground_plane</uri>
</include>

<!-- Include a custom model -->
<include>
  <uri>model://my_custom_humanoid</uri>
  <pose>0 0 1 0 0 0</pose>
</include>
```

### Environment-Specific Worlds

For humanoid robot testing, consider creating worlds with:

- **Obstacle courses**: Test navigation and path planning
- **Multi-level environments**: Test climbing and balance
- **Dynamic environments**: Moving objects for real-time reaction testing
- **Different gravity conditions**: Test performance under various physical conditions

## Joint Dynamics Configuration

Joint dynamics are critical for realistic humanoid robot simulation. Properly configured joints ensure that robot movements are physically accurate and stable. Key aspects include:

### Joint Types for Humanoid Robots

Different joint types are used for different parts of a humanoid robot:

- **Revolute joints**: Used for rotating joints like elbows, knees, and shoulders
- **Continuous joints**: Used for joints that can rotate infinitely, like wrists
- **Prismatic joints**: Used for linear motion joints
- **Fixed joints**: Used to connect rigid parts

Example URDF joint definition:

```xml
<joint name="shoulder_joint" type="revolute">
  <parent link="torso"/>
  <child link="upper_arm"/>
  <origin xyz="0.2 0 0.3" rpy="0 0 0"/>
  <axis xyz="0 1 0"/>
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1"/>
  <dynamics damping="0.1" friction="0.0"/>
</joint>
```

### Joint Limits and Constraints

Proper joint limits prevent unrealistic movements:

- **Position limits**: Define the minimum and maximum angles
- **Effort limits**: Define maximum force/torque
- **Velocity limits**: Define maximum speed
- **Damping**: Simulates friction in the joint
- **Friction**: Simulates static friction effects

### Joint Control

Joint control in Gazebo can be achieved through ROS 2 control interfaces:

1. **Position control**: Set target joint positions
2. **Velocity control**: Set target joint velocities
3. **Effort control**: Apply specific forces/torques to joints

Example joint state publisher:

```bash
# Publish joint states to control the robot
ros2 topic pub /joint_states sensor_msgs/msg/JointState "{
  name: ['joint1', 'joint2'],
  position: [0.5, -0.3],
  velocity: [0.0, 0.0],
  effort: [0.0, 0.0]
}"
```

## Integrating with ROS 2

Gazebo integrates seamlessly with ROS 2 through the Gazebo ROS packages (gazebo_ros_pkgs). This integration allows comprehensive communication between the physics simulation and the robot control system:

### Gazebo ROS Packages

The key packages for ROS 2 integration include:

- **gazebo_ros**: Core package providing the bridge between Gazebo and ROS 2
- **gazebo_plugins**: Provides ROS interfaces for sensors and actuators
- **gazebo_ros_control**: Interface for controlling robot joints through ROS 2

### Launching Gazebo with ROS 2

You can launch Gazebo with ROS 2 integration using launch files:

```xml
<!-- example.launch.xml -->
<launch>
  <!-- Start Gazebo with ROS 2 interface -->
  <include file="$(find-pkg-share gazebo_ros)/launch/gzserver.launch.py">
    <arg name="world" value="$(find-pkg-share my_robot_description)/worlds/my_world.sdf"/>
  </include>

  <include file="$(find-pkg-share gazebo_ros)/launch/gzclient.launch.py"/>

  <!-- Launch your robot controller -->
  <node pkg="my_robot_controller" exec="controller_node" name="robot_controller"/>
</launch>
```

### Common ROS 2 Interfaces

Gazebo provides several standard ROS 2 interfaces for robot interaction:

#### Joint State Publisher
- Topic: `/joint_states`
- Message type: `sensor_msgs/JointState`
- Publishes current joint positions, velocities, and efforts

#### Robot State Publisher
- Topic: `/tf` and `/tf_static`
- Message type: `tf2_msgs/TFMessage`
- Publishes coordinate transforms between robot frames

#### Joint Trajectory Controller
- Topic: `/joint_trajectory_controller/joint_trajectory`
- Service: `/joint_trajectory_controller/follow_joint_trajectory`
- Controls robot joints with position, velocity, or effort commands

### Sensor Integration

Gazebo sensors automatically publish to ROS 2 topics:

- **Camera sensors**: `/camera/image_raw`, `/camera/camera_info`
- **LIDAR sensors**: `/scan`, `/laser_scan`
- **IMU sensors**: `/imu/data`, `/imu/data_raw`
- **Force/Torque sensors**: `/wrench`

Example sensor configuration in URDF:

```xml
<gazebo reference="camera_link">
  <sensor name="camera" type="camera">
    <update_rate>30</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.1</near>
        <far>100</far>
      </clip>
    </camera>
    <plugin name="camera_controller" filename="libgazebo_ros_camera.so">
      <frame_name>camera_link_optical</frame_name>
      <min_depth>0.1</min_depth>
      <max_depth>100</max_depth>
    </plugin>
  </sensor>
</gazebo>
```

### Simulation Control Services

Gazebo provides several services for simulation control:

- `/gazebo/pause_physics` - Pause the physics simulation
- `/gazebo/unpause_physics` - Resume the physics simulation
- `/gazebo/reset_simulation` - Reset the entire simulation
- `/gazebo/set_model_state` - Set the state of a model
- `/gazebo/get_model_state` - Get the state of a model

### Example ROS 2 Integration

Here's a complete example of launching a humanoid robot in Gazebo with ROS 2:

```bash
# Launch the robot in Gazebo
ros2 launch my_humanoid_bringup gazebo.launch.py

# Monitor joint states
ros2 topic echo /joint_states

# Send commands to the robot
ros2 topic pub /joint_trajectory_controller/joint_trajectory trajectory_msgs/msg/JointTrajectory "{
  joint_names: ['hip_joint', 'knee_joint'],
  points: [{
    positions: [0.1, 0.2],
    time_from_start: {sec: 1, nanosec: 0}
  }]
}"
```

This integration enables a complete simulation environment where you can develop and test robot control algorithms before deploying to real hardware.

## Cross-References

For more information on related topics, see:
- [Chapter 2: High-Fidelity Interaction with Unity](./chapter-2-high-fidelity-interaction-with-unity) - Learn how to visualize physics simulation results in Unity
- [Chapter 3: Sensor Simulation for Perception](./chapter-3-sensor-simulation-for-perception) - Explore how sensors interact with physics simulations

## Hands-On Exercises

### Exercise 1: Basic Physics Simulation Setup
1. Launch Gazebo with a simple humanoid model
2. Verify that gravity is affecting the model appropriately
3. Check that joint limits are properly enforced
4. Record your observations about the physical behavior

### Exercise 2: Custom World Creation
1. Create a new world file with a custom environment
2. Include at least 3 objects (e.g., table, box, ramp)
3. Configure physics parameters for the world
4. Test the world with a humanoid model to ensure proper collision detection

### Exercise 3: Joint Control
1. Create a simple ROS 2 node that publishes joint commands
2. Control at least 2 joints of a humanoid model
3. Observe how the physics simulation responds to the commands
4. Experiment with different control parameters (position, velocity, effort)

### Exercise 4: Sensor Integration
1. Add a camera sensor to your humanoid model
2. Verify that the sensor data is published to ROS 2 topics
3. Visualize the sensor data using RViz2
4. Document the sensor's performance in your simulation environment

## Verification Checkpoints

To ensure you've successfully completed this chapter, verify the following:

- [ ] You can launch Gazebo with a humanoid robot model
- [ ] Gravity is properly configured and affecting the robot
- [ ] Joint limits and dynamics are correctly set up
- [ ] You can create and load custom world files
- [ ] ROS 2 topics are properly connected to Gazebo simulation
- [ ] You've completed all hands-on exercises successfully
- [ ] You understand how to configure physics parameters for different scenarios

## Summary

Physics simulation with Gazebo provides the foundation for safe, realistic testing of humanoid robots before deployment in the real world. The combination of accurate physics modeling and ROS 2 integration makes it an ideal platform for digital twin development.

## Next Steps

Continue to [Chapter 2: High-Fidelity Interaction with Unity](./chapter-2-high-fidelity-interaction-with-unity) to learn about visualizing physics simulation results, or proceed to [Chapter 3: Sensor Simulation for Perception](./chapter-3-sensor-simulation-for-perception) to explore sensor simulation. When you're ready to explore how these simulation techniques connect to real-world applications, continue to Module 3 which covers navigation and AI-driven autonomy.