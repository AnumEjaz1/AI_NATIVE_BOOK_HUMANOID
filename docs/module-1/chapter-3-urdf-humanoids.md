---
sidebar_position: 3
---

# Robot Modeling with URDF

This chapter provides clear explanations of URDF (Unified Robot Description Format) structure for humanoid robots, including links, joints, sensors, coordinate frames, and preparing models for simulation.

## Learning Objectives

By the end of this chapter, you will be able to:
- Understand the structure of URDF files for humanoid robots
- Identify and describe links, joints, and sensors in URDF
- Explain the role of coordinate frames in robot modeling
- Prepare URDF models for simulation
- Create example URDF models for humanoid robots

## Introduction to URDF

URDF (Unified Robot Description Format) is an XML-based format used in ROS to describe robot models. It defines the physical and visual properties of a robot, including its links, joints, and other components. URDF is essential for simulation, visualization, and kinematic analysis of robots.

For humanoid robots, URDF becomes particularly important as it needs to represent complex kinematic chains with multiple degrees of freedom.

## Links

Links represent rigid bodies in a robot. Each link has physical and visual properties that define how it appears and behaves in simulation.

### Link Properties
- **Visual**: How the link appears in visualization (geometry, material, origin)
- **Collision**: How the link interacts in collision detection (geometry, origin)
- **Inertial**: Physical properties for dynamics simulation (mass, inertia matrix)

### Example Link Definition
```xml
<link name="link_name">
  <visual>
    <origin xyz="0 0 0" rpy="0 0 0" />
    <geometry>
      <cylinder length="0.1" radius="0.05" />
    </geometry>
    <material name="blue">
      <color rgba="0 0 1 1" />
    </material>
  </visual>
  <collision>
    <origin xyz="0 0 0" rpy="0 0 0" />
    <geometry>
      <cylinder length="0.1" radius="0.05" />
    </geometry>
  </collision>
  <inertial>
    <mass value="1.0" />
    <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
  </inertial>
</link>
```

## Joints

Joints define the connection between links and specify how they can move relative to each other. Different joint types allow for different types of motion.

### Joint Types
- **Fixed**: No movement between links (0 DOF)
- **Revolute**: Single axis rotation, limited range (1 DOF)
- **Continuous**: Single axis rotation, unlimited range (1 DOF)
- **Prismatic**: Single axis translation, limited range (1 DOF)
- **Floating**: 6 DOF movement (not commonly used)
- **Planar**: Movement in a plane (3 DOF)

### Joint Properties
- **Parent**: The link that is closer to the robot base
- **Child**: The link that is further from the robot base
- **Origin**: Transform from parent to child
- **Axis**: The axis of motion for movable joints
- **Limits**: For revolute and prismatic joints (effort, velocity, lower, upper)

### Example Joint Definition
```xml
<joint name="joint_name" type="revolute">
  <parent link="parent_link" />
  <child link="child_link" />
  <origin xyz="0 0 0.1" rpy="0 0 0" />
  <axis xyz="0 0 1" />
  <limit lower="-1.57" upper="1.57" effort="100" velocity="1" />
</joint>
```

## Sensors

Sensors in URDF define where sensor elements are placed on the robot. While URDF doesn't simulate sensor data directly, it specifies where sensors are physically located.

### Common Sensor Types
- **Camera**: Visual sensors
- **IMU**: Inertial measurement units
- **Laser Range Finder**: LIDAR sensors
- **Force/Torque**: Force and torque sensors

### Example Sensor Definition
```xml
<gazebo reference="sensor_link">
  <sensor name="camera" type="camera">
    <pose>0 0 0 0 0 0</pose>
    <visualize>true</visualize>
    <update_rate>30.0</update_rate>
    <camera name="head">
      <horizontal_fov>1.3962634</horizontal_fov>
      <image>
        <width>800</width>
        <height>600</height>
        <format>R8G8B8</format>
      </image>
      <clip>
        <near>0.02</near>
        <far>300</far>
      </clip>
    </camera>
  </sensor>
</gazebo>
```

## Coordinate Frames

Coordinate frames in URDF define the reference frames for each link. These frames are crucial for kinematic calculations and are used by the ROS tf2 system for coordinate transformations.

### Frame Conventions
- Each link has its own coordinate frame
- Transformations between frames are computed based on joint positions
- The base_link frame is typically the root of the robot's kinematic chain
- Frames follow the right-hand rule convention

### Importance for Humanoid Robots
For humanoid robots, coordinate frames are particularly important for:
- Kinematic chain calculations
- Walking pattern generation
- Balance control
- Motion planning

## Preparing Models for Simulation

URDF models need additional information to work properly in simulation environments like Gazebo.

### Gazebo-Specific Elements
- **Materials**: How the robot appears in Gazebo
- **Controllers**: How joints are controlled
- **Inertial properties**: Mass, center of mass, and moments of inertia
- **Transmission elements**: How actuators connect to joints

### Example Gazebo Integration
```xml
<gazebo reference="link_name">
  <material>Gazebo/Blue</material>
  <mu1>0.2</mu1>
  <mu2>0.2</mu2>
  <self_collide>false</self_collide>
  <gravity>true</gravity>
  <max_contacts>10</max_contacts>
</gazebo>
```

## Example URDF Model for a Humanoid Robot

Here's a simplified example of a humanoid robot URDF:

```xml
<?xml version="1.0"?>
<robot name="simple_humanoid">
  <!-- Base Link -->
  <link name="base_link">
    <inertial>
      <mass value="5.0" />
      <origin xyz="0 0 0" />
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    </inertial>
    <visual>
      <origin xyz="0 0 0" />
      <geometry>
        <box size="0.2 0.1 0.1" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0" />
      <geometry>
        <box size="0.2 0.1 0.1" />
      </geometry>
    </collision>
  </link>

  <!-- Torso -->
  <link name="torso">
    <inertial>
      <mass value="3.0" />
      <origin xyz="0 0 0.2" />
      <inertia ixx="0.1" ixy="0.0" ixz="0.0" iyy="0.1" iyz="0.0" izz="0.1" />
    </inertial>
    <visual>
      <origin xyz="0 0 0.2" />
      <geometry>
        <box size="0.15 0.15 0.3" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0.2" />
      <geometry>
        <box size="0.15 0.15 0.3" />
      </geometry>
    </collision>
  </link>

  <!-- Joint connecting base to torso -->
  <joint name="base_to_torso" type="fixed">
    <parent link="base_link" />
    <child link="torso" />
    <origin xyz="0 0 0.05" />
  </joint>

  <!-- Head -->
  <link name="head">
    <inertial>
      <mass value="1.0" />
      <origin xyz="0 0 0.05" />
      <inertia ixx="0.01" ixy="0.0" ixz="0.0" iyy="0.01" iyz="0.0" izz="0.01" />
    </inertial>
    <visual>
      <origin xyz="0 0 0.05" />
      <geometry>
        <sphere radius="0.08" />
      </geometry>
    </visual>
    <collision>
      <origin xyz="0 0 0.05" />
      <geometry>
        <sphere radius="0.08" />
      </geometry>
    </collision>
  </link>

  <!-- Joint connecting torso to head -->
  <joint name="torso_to_head" type="revolute">
    <parent link="torso" />
    <child link="head" />
    <origin xyz="0 0 0.3" />
    <axis xyz="0 1 0" />
    <limit lower="-0.5" upper="0.5" effort="10" velocity="1" />
  </joint>
</robot>
```

## Best Practices for Humanoid URDF

When creating URDF models for humanoid robots:

1. **Start Simple**: Begin with a basic skeleton and add complexity gradually
2. **Accurate Inertial Properties**: Properly estimate masses and inertias for realistic simulation
3. **Consistent Naming**: Use clear, consistent naming conventions
4. **Validate Kinematics**: Ensure the kinematic chain is correct and physically plausible
5. **Consider Actuator Limits**: Set joint limits that reflect physical constraints
6. **Use Standard Formats**: Follow REP standards for URDF when possible

## Troubleshooting Common Issues

- **Invalid Kinematic Chain**: Ensure all links are connected through joints
- **Inconsistent Units**: Use consistent units throughout the model
- **Inertia Issues**: Make sure inertia matrices are physically plausible
- **Collision Issues**: Check that collision geometry is properly defined

## Summary

URDF is fundamental to representing humanoid robots in ROS 2. Understanding links, joints, sensors, and coordinate frames is crucial for creating accurate robot models that work properly in simulation and for kinematic analysis.

The structure of URDF files allows for detailed specification of robot geometry, kinematics, and dynamics, making it possible to create sophisticated humanoid robot models that can be used for simulation, visualization, and control development.

## References

For more detailed information on URDF and robot modeling in ROS 2, please refer to the official ROS 2 documentation at https://docs.ros.org/en/rolling/