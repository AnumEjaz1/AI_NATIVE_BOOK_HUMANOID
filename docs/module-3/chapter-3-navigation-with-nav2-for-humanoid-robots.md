---
sidebar_position: 3
description: Learn how to adapt Nav2 for humanoid robot navigation, focusing on path planning, costmaps, and localization for bipedal locomotion
---

# Chapter 3: Navigation with Nav2 for Humanoid Robots

## Learning Objectives

By the end of this chapter, you should be able to:
- Explain how to adapt Nav2 for humanoid robot navigation and bipedal locomotion
- Configure path planning algorithms for humanoid-specific constraints
- Set up costmaps for humanoid robots with unique kinematic properties
- Implement localization techniques suitable for humanoid robots
- Design navigation behaviors that account for bipedal characteristics
- Integrate perception data from Isaac ROS into the navigation system

## Introduction

Navigation is a critical capability for autonomous humanoid robots, enabling them to move purposefully through complex environments. While Nav2 (Navigation 2) provides a robust navigation framework for wheeled robots, humanoid robots present unique challenges due to their bipedal locomotion, balance requirements, and different kinematic constraints.

In this chapter, we'll explore how to adapt Nav2 principles for humanoid robot navigation, focusing on the specific requirements of bipedal locomotion and how to integrate perception data from Isaac ROS into the navigation system.

## Understanding Nav2 Architecture for Humanoids

Nav2 is ROS 2's navigation framework that provides localization, path planning, and navigation capabilities. For humanoid robots, several components need to be adapted:

### Core Nav2 Components

1. **Global Planner**: Path planning from start to goal
2. **Local Planner**: Short-term trajectory generation
3. **Controller**: Low-level command generation
4. **Costmap**: Environment representation with obstacles
5. **Recovery Behaviors**: Actions when navigation fails

### Humanoid-Specific Considerations

- **Kinematic Constraints**: Bipedal locomotion vs. wheeled motion
- **Balance Requirements**: Maintaining stability during navigation
- **Step Planning**: Navigating with discrete step locations
- **Z-Motion**: Consideration of vertical movement for stairs/ramps
- **Dynamic Stability**: Real-time balance adjustments during movement

## Path Planning for Bipedal Locomotion

Traditional path planners like A* and Dijkstra work well for wheeled robots, but humanoid robots require specialized path planning that accounts for their unique locomotion characteristics.

### Humanoid-Specific Path Planning Algorithms

#### Footstep Planning

Footstep planners generate sequences of foot positions that maintain balance:

```python
# Humanoid Footstep Planner Example
import numpy as np
from nav2_msgs.action import NavigateToPose
from geometry_msgs.msg import PoseStamped
import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node

class HumanoidFootstepPlanner:
    def __init__(self, node):
        self.node = node
        self.current_pose = None
        self.support_polygon = self.calculate_support_polygon()

    def calculate_support_polygon(self):
        """Calculate the support polygon for the current stance"""
        # Define support polygon based on foot positions
        # For a biped, this is typically the area between feet
        support_polygon = [
            (-0.1, -0.1),  # Left foot position (relative)
            (0.1, -0.1),   # Right foot position (relative)
            (0.1, 0.1),
            (-0.1, 0.1)
        ]
        return support_polygon

    def plan_footsteps(self, start_pose, goal_pose):
        """Plan sequence of footsteps from start to goal"""
        # This is a simplified example - actual footstep planning
        # would be much more complex
        footsteps = []

        # Calculate straight-line path
        dx = goal_pose.position.x - start_pose.position.x
        dy = goal_pose.position.y - start_pose.position.y
        distance = np.sqrt(dx**2 + dy**2)

        # Generate footsteps along the path
        num_steps = int(distance / 0.3)  # Assume 0.3m step size

        for i in range(1, num_steps + 1):
            step_x = start_pose.position.x + (dx * i / num_steps)
            step_y = start_pose.position.y + (dy * i / num_steps)

            # Alternate between left and right foot
            if i % 2 == 1:
                # Left foot step
                step_pose = PoseStamped()
                step_pose.pose.position.x = step_x
                step_pose.pose.position.y = step_y + 0.1  # Offset for left foot
                step_pose.pose.position.z = 0.0
                footsteps.append(('left', step_pose))
            else:
                # Right foot step
                step_pose = PoseStamped()
                step_pose.pose.position.x = step_x
                step_pose.pose.position.y = step_y - 0.1  # Offset for right foot
                step_pose.pose.position.z = 0.0
                footsteps.append(('right', step_pose))

        return footsteps

class HumanoidNav2Node(Node):
    def __init__(self):
        super().__init__('humanoid_nav2_node')

        # Initialize footstep planner
        self.footstep_planner = HumanoidFootstepPlanner(self)

        # Nav2 action client
        self.nav_to_pose_client = ActionClient(
            self,
            NavigateToPose,
            'navigate_to_pose'
        )

        # Subscribe to robot pose
        self.pose_sub = self.create_subscription(
            PoseStamped,
            '/robot_pose',
            self.pose_callback,
            10
        )

    def pose_callback(self, msg):
        """Update current robot pose"""
        self.footstep_planner.current_pose = msg.pose

    def plan_to_pose(self, goal_pose):
        """Plan path to goal pose using footstep planning"""
        if self.footstep_planner.current_pose is None:
            self.get_logger().warn("Current pose not available")
            return False

        footsteps = self.footstep_planner.plan_footsteps(
            self.footstep_planner.current_pose,
            goal_pose
        )

        # Convert footsteps to Nav2-compatible format
        return self.execute_navigation(footsteps)

    def execute_navigation(self, footsteps):
        """Execute navigation using planned footsteps"""
        # This would implement the actual navigation execution
        # using the humanoid's locomotion system
        return True
```

#### Balanced Path Planning

Humanoid robots must consider balance when planning paths:

```python
# Balanced Path Planning Example
class BalancedPathPlanner:
    def __init__(self):
        self.balance_threshold = 0.05  # meters
        self.support_margin = 0.02     # safety margin

    def is_path_balanced(self, path, support_polygon):
        """Check if path maintains balance"""
        for pose in path:
            # Calculate center of mass position relative to support polygon
            com_x = pose.position.x
            com_y = pose.position.y

            # Check if COM is within support polygon with safety margin
            is_balanced = self.check_balance(com_x, com_y, support_polygon)
            if not is_balanced:
                return False
        return True

    def check_balance(self, com_x, com_y, support_polygon):
        """Check if center of mass is within support polygon"""
        # This would implement polygon inclusion testing
        # Simplified example
        return True  # Placeholder
```

### Global Planner Configuration for Humanoids

Configure the global planner with humanoid-specific parameters:

```yaml
# Humanoid Nav2 Global Planner Configuration
global_costmap:
  global_costmap:
    ros__parameters:
      update_frequency: 1.0
      publish_frequency: 1.0
      width: 20
      height: 20
      resolution: 0.05  # Higher resolution for precise footstep planning
      robot_base_frame: "base_link"
      global_frame: "map"
      rolling_window: false
      track_unknown_space: true
      plugins: ["static_layer", "obstacle_layer", "inflation_layer"]

      inflation_layer:
        enabled: true
        cost_scaling_factor: 5.0  # Higher inflation for humanoid safety
        inflation_radius: 0.8     # Larger safety radius for humanoid

global_planner:
  ros__parameters:
    planner_frequency: 1.0
    use_astar: false
    allow_unknown: true
    tolerance: 0.5              # Humanoid-specific tolerance
    use_final_approach_orientation: false  # Bipedal approach may need different orientation
```

## Costmap Configuration for Humanoid Robots

Costmaps in Nav2 represent the environment with obstacles, but humanoid robots need different costmap configurations due to their unique characteristics.

### Multi-Layer Costmap for Humanoids

Humanoid robots require consideration of multiple height levels (for stairs, ramps, obstacles):

```yaml
# Humanoid Multi-Layer Costmap Configuration
local_costmap:
  local_costmap:
    ros__parameters:
      update_frequency: 5.0
      publish_frequency: 2.0
      width: 6.0
      height: 6.0
      resolution: 0.025  # Finer resolution for precise navigation
      robot_base_frame: "base_link"
      global_frame: "odom"
      rolling_window: true
      track_unknown_space: false

      plugins: ["voxel_layer", "inflation_layer"]

      voxel_layer:
        plugin: "nav2_costmap_2d::VoxelLayer"
        enabled: true
        voxel_size: 0.05    # Voxel size for 3D obstacle representation
        observation_sources: "scan"
        scan:
          topic: "/laser_scan"
          max_obstacle_height: 2.0    # Consider obstacles up to humanoid height
          clearing: true
          marking: true
          data_type: "LaserScan"
          obstacle_range: 3.0
          raytrace_range: 4.0

      inflation_layer:
        plugin: "nav2_costmap_2d::InflationLayer"
        enabled: true
        cost_scaling_factor: 10.0     # Higher cost scaling for humanoid safety
        inflation_radius: 1.0         # Larger safety radius
        inflate_unknown: false
```

### Humanoid-Specific Cost Calculations

Humanoid robots have different clearance requirements:

```python
# Humanoid-Specific Cost Calculation
class HumanoidCostCalculator:
    def __init__(self):
        # Humanoid dimensions and constraints
        self.step_height_max = 0.15    # Maximum step height (15cm)
        self.step_depth_max = 0.30     # Maximum step depth (30cm)
        self.step_width_max = 0.60     # Maximum step width (60cm)
        self.balance_radius = 0.15     # Balance safety radius

    def calculate_traversability_cost(self, cell):
        """Calculate cost based on traversability for humanoid"""
        base_cost = self.get_base_cost(cell)

        # Add cost for steep changes (stairs, ramps)
        height_diff = self.estimate_height_difference(cell)
        if height_diff > self.step_height_max:
            return 255  # Mark as unwalkable

        # Add balance-related costs
        balance_cost = self.calculate_balance_cost(cell)

        # Combine costs
        total_cost = min(254, base_cost + balance_cost)
        return total_cost

    def calculate_balance_cost(self, cell):
        """Calculate cost based on balance requirements"""
        # Higher costs near obstacles for balance safety
        distance_to_obstacle = self.get_distance_to_nearest_obstacle(cell)
        if distance_to_obstacle < self.balance_radius:
            return int(200 * (1 - distance_to_obstacle / self.balance_radius))
        return 0
```

## Localization for Humanoid Robots

Localization in Nav2 estimates the robot's pose, but humanoid robots may have different sensor configurations and movement patterns.

### Sensor Integration for Humanoid Localization

Humanoid robots often have IMUs and other sensors that affect localization:

```python
# Humanoid Localization Node Example
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Imu, LaserScan
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry
from tf2_ros import TransformBroadcaster
import tf2_geometry_msgs
import tf2_ros
import geometry_msgs.msg

class HumanoidLocalizationNode(Node):
    def __init__(self):
        super().__init__('humanoid_localization')

        # Initialize transform broadcaster
        self.tf_broadcaster = TransformBroadcaster(self)

        # Subscribe to various sensors
        self.imu_sub = self.create_subscription(
            Imu,
            '/imu/data',
            self.imu_callback,
            10
        )

        self.odom_sub = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10
        )

        self.initial_pose_pub = self.create_publisher(
            PoseWithCovarianceStamped,
            '/initialpose',
            10
        )

        # Initialize localization system
        self.initialize_localization_system()

    def initialize_localization_system(self):
        """Initialize the localization system for humanoid"""
        # This would initialize AMCL or other localization methods
        # with humanoid-specific parameters
        pass

    def imu_callback(self, msg):
        """Process IMU data for improved localization"""
        # Use IMU data to improve pose estimates
        # Humanoid IMU data can provide balance and orientation information
        pass

    def odom_callback(self, msg):
        """Process odometry data"""
        # Combine with other sensors for robust localization
        pass
```

### AMCL Configuration for Humanoids

Configure AMCL (Adaptive Monte Carlo Localization) with humanoid-specific parameters:

```yaml
# Humanoid AMCL Configuration
amcl:
  ros__parameters:
    use_sim_time: false
    alpha1: 0.2      # Odometry model noise for walking
    alpha2: 0.2      # Odometry model noise for walking
    alpha3: 0.2      # Odometry model noise for walking
    alpha4: 0.2      # Odometry model noise for walking
    alpha5: 0.0      # No 2D rotation in odometry for bipedal

    base_frame_id: "base_link"
    beam_skip_distance: 0.5
    beam_skip_error_threshold: 0.9
    beam_skip_threshold: 0.3
    do_beamskip: false
    global_frame_id: "map"
    lambda_short: 0.1
    laser_likelihood_max_dist: 2.0
    laser_max_range: 100.0
    laser_min_range: -1.0
    laser_model_type: "likelihood_field"
    max_beams: 60
    max_particles: 2000    # More particles for complex humanoid movement
    min_particles: 500
    odom_frame_id: "odom"
    pf_err: 0.05
    pf_z: 0.99
    recovery_alpha_fast: 0.0
    recovery_alpha_slow: 0.0
    resample_interval: 1
    robot_model_type: "nav2_amcl::DifferentialMotionModel"  # Could be customized for humanoid
    save_pose_rate: 0.5
    sigma_hit: 0.2
    tf_broadcast: true
    transform_tolerance: 1.0  # Longer tolerance for humanoid movement
    update_min_a: 0.2
    update_min_d: 0.15        # Minimum distance before update (step size related)
```

## Practical Exercise: Configuring Nav2 for Humanoid Navigation

Let's implement a complete navigation system for humanoid robots:

1. **Setup**: Configure Nav2 with humanoid-specific parameters
2. **Planning**: Implement footstep planning integration
3. **Execution**: Execute navigation with balance considerations
4. **Evaluation**: Test navigation performance

### Step 1: Nav2 Configuration

Create the main launch file for humanoid navigation:

```python
# Humanoid Navigation Launch Example
import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from nav2_common.launch import RewrittenYaml

def generate_launch_description():
    # Launch configuration variables
    namespace = LaunchConfiguration('namespace')
    use_sim_time = LaunchConfiguration('use_sim_time')
    autostart = LaunchConfiguration('autostart')
    params_file = LaunchConfiguration('params_file')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    map_subscribe_transient_local = LaunchConfiguration('map_subscribe_transient_local')

    # Map server parameters
    map_yaml_file = LaunchConfiguration('map')

    # Coordinates
    x_pose = LaunchConfiguration('x_pose', default='0.0')
    y_pose = LaunchConfiguration('y_pose', default='0.0')
    yaw_pose = LaunchConfiguration('yaw_pose', default='0.0')

    # Declare launch arguments
    declare_namespace_cmd = DeclareLaunchArgument(
        'namespace',
        default_value='',
        description='Top-level namespace')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time',
        default_value='false',
        description='Use simulation (Gazebo) clock if true')

    declare_params_file_cmd = DeclareLaunchArgument(
        'params_file',
        default_value='install/nav2_bringup/share/nav2_bringup/params/nav2_params.yaml',
        description='Full path to the ROS2 parameters file to use for all launched nodes')

    declare_autostart_cmd = DeclareLaunchArgument(
        'autostart',
        default_value='true',
        description='Automatically startup the nav2 stack')

    declare_default_bt_xml_cmd = DeclareLaunchArgument(
        'default_bt_xml_filename',
        default_value='install/nav2_bt_navigator/share/nav2_bt_navigator/behavior_trees/navigate_w_replanning_and_recovery.xml',
        description='Full path to the behavior tree xml file to use')

    declare_map_subscribe_transient_local_cmd = DeclareLaunchArgument(
        'map_subscribe_transient_local',
        default_value='false',
        description='Whether to set the map subscriber QoS to transient local')

    # Map server node
    map_server_node = Node(
        package='nav2_map_server',
        executable='map_server',
        name='map_server',
        namespace=namespace,
        parameters=[params_file],
        remappings=[('cmd_vel', 'cmd_vel')],
        output='screen'
    )

    # Lifecycle manager for navigation
    lifecycle_manager_node = Node(
        package='nav2_lifecycle_manager',
        executable='lifecycle_manager',
        name='lifecycle_manager',
        namespace=namespace,
        parameters=[{'use_sim_time': use_sim_time},
                   {'autostart': autostart},
                   {'node_names': ['map_server',
                                   'planner_server',
                                   'controller_server',
                                   'recoveries_server',
                                   'bt_navigator',
                                   'waypoint_follower']}],
        output='screen'
    )

    # Return the launch description
    return LaunchDescription([
        declare_namespace_cmd,
        declare_use_sim_time_cmd,
        declare_params_file_cmd,
        declare_autostart_cmd,
        declare_default_bt_xml_cmd,
        declare_map_subscribe_transient_local_cmd,
        map_server_node,
        lifecycle_manager_node
    ])
```

### Step 2: Behavior Tree Configuration

Configure behavior trees for humanoid navigation:

```xml
<!-- Humanoid Navigation Behavior Tree -->
<root main_tree_to_execute="MainTree">
    <BehaviorTree ID="MainTree">
        <RecoveryNode number_of_retries="6" name="NavigateRecovery">
            <PipelineSequence name="NavigateWithReplanning">
                <RateController hz="1.0">
                    <ComputePathToPose goal="{goal}" path="{path}" planner_id="GridBased"/>
                </RateController>
                <FollowPath path="{path}" controller_id="FollowPath" />
            </PipelineSequence>
            <ReactiveFallback name="RecoveryFallback">
                <GoalUpdated/>
                <RoundRobin name="RecoveryActions">
                    <Sequence name="ClearingActions">
                        <ClearEntireCostmap name="ClearGlobalCostmap-Context" service_name="global_costmap/clear_entirely_global_costmap"/>
                        <ClearEntireCostmap name="ClearLocalCostmap-Context" service_name="local_costmap/clear_entirely_local_costmap"/>
                        <Spin spin_dist="1.57"/>
                    </Sequence>
                    <Wait wait_duration="5"/>
                </RoundRobin>
            </ReactiveFallback>
        </RecoveryNode>
    </BehaviorTree>
</root>
```

### Step 3: Navigation Execution with Balance

Implement navigation execution with balance considerations:

```python
# Humanoid Navigation Execution
class HumanoidNavigationExecutor:
    def __init__(self, node):
        self.node = node
        self.current_balance_state = "stable"
        self.navigation_active = False

    def execute_navigation_with_balance(self, path):
        """Execute navigation while maintaining balance"""
        if not self.check_initial_balance():
            self.node.get_logger().error("Robot not in stable state for navigation")
            return False

        self.navigation_active = True

        for step in path:
            # Check balance before each step
            if not self.check_balance_before_step(step):
                self.node.get_logger().warn(f"Step {step} would compromise balance")
                return False

            # Execute the step
            success = self.execute_step_with_balance(step)

            if not success:
                self.node.get_logger().error("Step execution failed")
                return False

            # Update balance state
            self.update_balance_state()

        self.navigation_active = False
        return True

    def check_balance_before_step(self, step):
        """Check if step maintains balance"""
        # Implementation would check balance before executing step
        return True

    def execute_step_with_balance(self, step):
        """Execute a single step with balance maintenance"""
        # Implementation would execute the step while monitoring balance
        return True

    def update_balance_state(self):
        """Update the robot's balance state"""
        # Implementation would update balance state based on current pose
        pass

    def check_initial_balance(self):
        """Check if robot is in stable state to begin navigation"""
        # Check IMU data, foot positions, etc.
        return True
```

## Integration with Isaac ROS Perception

Integrating perception data from Isaac ROS into the navigation system:

```python
# Isaac ROS Perception Integration
class IsaacROSNavIntegration:
    def __init__(self, node):
        self.node = node

        # Subscribe to Isaac ROS perception data
        self.object_sub = self.node.create_subscription(
            Detection2DArray,
            '/isaac_ros_object_detections',
            self.object_detection_callback,
            10
        )

        self.vslam_pose_sub = self.node.create_subscription(
            PoseStamped,
            '/isaac_ros_visual_slam/pose',
            self.vslam_pose_callback,
            10
        )

        # Integrate perception into costmap
        self.perception_costmap = self.initialize_perception_costmap()

    def object_detection_callback(self, msg):
        """Process object detections from Isaac ROS"""
        # Add detected objects to costmap
        for detection in msg.detections:
            self.add_detection_to_costmap(detection)

    def vslam_pose_callback(self, msg):
        """Process VSLAM pose estimates"""
        # Use VSLAM pose for improved localization
        self.update_localization_with_vslam(msg.pose)

    def add_detection_to_costmap(self, detection):
        """Add object detection to navigation costmap"""
        # Convert detection to costmap coordinates and add obstacle
        pass

    def update_localization_with_vslam(self, pose):
        """Update robot localization using VSLAM data"""
        # Fuse VSLAM pose with other localization sources
        pass
```

## Verification Checkpoint

To verify your understanding of Nav2 for humanoid navigation:

1. Can you configure Nav2 for humanoid-specific path planning with footstep considerations?
2. Can you set up costmaps that account for humanoid balance and step constraints?
3. Can you implement localization techniques suitable for humanoid robots?
4. Do you understand how to adapt navigation behaviors for bipedal locomotion?
5. Can you integrate perception data from Isaac ROS into the navigation system?

## Summary

In this chapter, we explored Navigation with Nav2 for humanoid robots, focusing on:

- Path planning algorithms adapted for bipedal locomotion
- Costmap configuration with humanoid-specific constraints
- Localization techniques for humanoid robots
- Behavior trees and navigation execution with balance considerations
- Integration of Isaac ROS perception data into navigation

We've now completed all three chapters of Module 3, connecting Isaac Sim for synthetic data generation, Isaac ROS for accelerated perception, and Nav2 for humanoid navigation. This module provides the foundation for autonomous humanoid behavior by connecting simulated robots to AI-driven perception and navigation capabilities.

## Next Steps

This module prepares learners for Vision-Language-Action integration in Module 4, where we'll explore how to orchestrate the perception, simulation, and navigation capabilities developed in this module into cohesive autonomous behaviors. The concepts learned here form the core of the AI Robot Brain that enables humanoid robots to perceive their environment, understand it, and navigate through it autonomously.