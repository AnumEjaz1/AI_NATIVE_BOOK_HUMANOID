---
sidebar_position: 1
title: "Chapter 1: Voice-to-Action - Speech-to-Text Pipelines and ROS 2 Action Routing"
---

# Chapter 1: Voice-to-Action - Speech-to-Text Pipelines and ROS 2 Action Routing

## Overview

This chapter introduces the Voice-to-Action component of the Vision-Language-Action (VLA) system. It covers the implementation of speech-to-text conversion and the routing of voice commands into ROS 2 actions for humanoid robot control.

## Learning Objectives

By the end of this chapter, you will understand:
- How to implement speech-to-text conversion for natural language processing
- How to route processed text commands to appropriate ROS 2 action servers
- The integration between voice input and robot action execution
- Best practices for voice command interpretation and error handling

## Speech-to-Text Pipeline Implementation

### Setting Up Speech Recognition

The first step in implementing the Voice-to-Action system is to establish a robust speech-to-text pipeline. This involves capturing audio input from the user and converting it to text that can be processed by the robot's cognitive systems.

```python
import speech_recognition as sr
import rospy
from std_msgs.msg import String

class VoiceToActionNode:
    def __init__(self):
        rospy.init_node('voice_to_action')
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

        # Publisher for processed commands
        self.command_publisher = rospy.Publisher('voice_commands', String, queue_size=10)

        # Configure speech recognition settings
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
```

### Voice Command Processing

Once we have the speech-to-text pipeline established, we need to process the commands and route them to appropriate ROS 2 action servers. This involves natural language processing to understand the user's intent and map it to specific robot actions.

```python
def process_voice_command(self, audio):
    try:
        # Convert audio to text using Google's speech recognition
        text = self.recognizer.recognize_google(audio)
        rospy.loginfo(f"Recognized command: {text}")

        # Parse the command and determine appropriate action
        action = self.parse_command(text)

        if action:
            self.route_to_ros_action(action, text)

    except sr.UnknownValueError:
        rospy.logwarn("Could not understand audio")
    except sr.RequestError as e:
        rospy.logerr(f"Speech recognition error: {e}")
```

## ROS 2 Action Integration

### Action Server Communication

The Voice-to-Action system must communicate with existing ROS 2 action servers to execute robot behaviors. This requires understanding the action interfaces and properly formatting requests.

```python
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

class ActionRouter:
    def __init__(self):
        # Connect to navigation action server
        self.nav_client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
        self.nav_client.wait_for_server()

    def execute_navigation_action(self, x, y, theta):
        goal = MoveBaseGoal()
        goal.target_pose.header.frame_id = "map"
        goal.target_pose.header.stamp = rospy.Time.now()
        goal.target_pose.pose.position.x = x
        goal.target_pose.pose.position.y = y
        goal.target_pose.pose.orientation.z = theta

        self.nav_client.send_goal(goal)
        self.nav_client.wait_for_result()
```

### Command Parsing and Intent Recognition

The system needs to parse natural language commands and convert them into structured actions that ROS 2 can execute. This involves understanding the user's intent and extracting relevant parameters.

```python
def parse_command(self, text):
    """Parse natural language command and return structured action"""
    text_lower = text.lower()

    if "move" in text_lower and "forward" in text_lower:
        # Extract distance if specified
        distance = self.extract_distance(text_lower) or 1.0
        return {"action": "move_forward", "distance": distance}

    elif "turn" in text_lower or "rotate" in text_lower:
        direction = self.extract_direction(text_lower)
        angle = self.extract_angle(text_lower) or 90.0
        return {"action": "turn", "direction": direction, "angle": angle}

    elif "pick up" in text_lower or "grasp" in text_lower:
        object_name = self.extract_object(text_lower)
        return {"action": "grasp_object", "object": object_name}

    return None
```

## Error Handling and Validation

### Robust Command Processing

The system must handle various error conditions gracefully, including unclear audio, unrecognized commands, and failed action executions.

```python
def validate_and_execute(self, action):
    """Validate action parameters and execute safely"""
    try:
        if action["action"] == "move_forward":
            if 0.1 <= action["distance"] <= 10.0:  # Validate distance bounds
                self.execute_move_forward(action["distance"])
            else:
                rospy.logwarn(f"Invalid distance: {action['distance']}")
        # Additional validation for other actions...
    except Exception as e:
        rospy.logerr(f"Action execution failed: {e}")
```

## Testing and Validation

### Unit Tests for Voice Processing

```python
import unittest

class TestVoiceToAction(unittest.TestCase):
    def setUp(self):
        self.vta_node = VoiceToActionNode()

    def test_command_parsing(self):
        action = self.vta_node.parse_command("Move forward 2 meters")
        self.assertEqual(action["action"], "move_forward")
        self.assertEqual(action["distance"], 2.0)

    def test_unrecognized_command(self):
        action = self.vta_node.parse_command("Invalid command")
        self.assertIsNone(action)
```

## Summary

This chapter has covered the implementation of the Voice-to-Action system, including speech-to-text conversion, command parsing, and routing to ROS 2 actions. The system provides a natural interface for users to control the humanoid robot through voice commands, forming the foundation of the VLA system.

In the next chapter, we'll explore cognitive planning using LLMs to convert natural language goals into structured ROS 2 plans.