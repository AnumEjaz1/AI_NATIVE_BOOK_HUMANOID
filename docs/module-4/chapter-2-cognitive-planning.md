---
sidebar_position: 2
title: "Chapter 2: Cognitive Planning - Using LLMs for Natural Language Goal Conversion"
---

# Chapter 2: Cognitive Planning - Using LLMs for Natural Language Goal Conversion

## Overview

This chapter explores the Cognitive Planning component of the Vision-Language-Action (VLA) system. It covers how Large Language Models (LLMs) can be used to convert high-level natural language goals into structured ROS 2 plans that enable autonomous robot behavior.

## Learning Objectives

By the end of this chapter, you will understand:
- How to integrate LLMs into the robotic planning pipeline
- Techniques for converting natural language goals into structured action sequences
- Methods for incorporating environmental perception data into planning decisions
- Best practices for ensuring safe and reliable cognitive planning

## LLM Integration Architecture

### System Architecture Overview

The cognitive planning system bridges high-level human goals with low-level robot actions by leveraging LLMs to generate executable plans. This involves a multi-step process:

1. **Goal Interpretation**: Understanding the user's natural language request
2. **Context Integration**: Incorporating environmental and robot state information
3. **Plan Generation**: Creating a sequence of ROS 2 actions to achieve the goal
4. **Validation and Safety**: Ensuring the generated plan is safe and executable

```python
import openai
import json
from typing import Dict, List, Any

class CognitivePlanner:
    def __init__(self, api_key: str):
        openai.api_key = api_key
        self.client = openai.OpenAI()

    def generate_plan(self, goal: str, environment_context: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate a structured plan from natural language goal and environmental context"""

        prompt = self._construct_prompt(goal, environment_context)

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": self._get_system_prompt()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            functions=[
                {
                    "name": "generate_ros_plan",
                    "description": "Generate a sequence of ROS 2 actions to achieve the specified goal",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "actions": {
                                "type": "array",
                                "items": {
                                    "type": "object",
                                    "properties": {
                                        "action_type": {"type": "string", "enum": ["navigation", "manipulation", "perception", "communication"]},
                                        "parameters": {"type": "object"},
                                        "description": {"type": "string"}
                                    }
                                }
                            }
                        }
                    }
                }
            ],
            function_call={"name": "generate_ros_plan"}
        )

        # Parse the function call result
        function_args = json.loads(response.choices[0].message.function_call.arguments)
        return function_args["actions"]
```

### Environmental Context Integration

The cognitive planner must incorporate real-time environmental data to make informed decisions. This includes information about objects, locations, and robot capabilities.

```python
def get_environment_context(self) -> Dict[str, Any]:
    """Collect environmental and robot state information"""
    context = {
        "robot_state": self._get_robot_state(),
        "object_locations": self._get_object_locations(),
        "navigable_areas": self._get_navigable_areas(),
        "robot_capabilities": self._get_robot_capabilities(),
        "current_time": self._get_current_time(),
        "safety_constraints": self._get_safety_constraints()
    }
    return context

def _get_robot_state(self) -> Dict[str, Any]:
    """Get current robot state including battery, location, and active tasks"""
    # Implementation to get robot's current state
    return {
        "position": {"x": 0.0, "y": 0.0, "theta": 0.0},
        "battery_level": 0.85,
        "gripper_status": "open",
        "current_task": None
    }
```

## Plan Generation and Validation

### Structured Plan Format

The cognitive planner generates plans in a structured format that can be directly executed by the ROS 2 system. Each action in the plan includes type, parameters, and safety checks.

```python
def _construct_prompt(self, goal: str, context: Dict[str, Any]) -> str:
    """Construct the LLM prompt with goal and environmental context"""
    prompt = f"""
    You are a cognitive planning system for a humanoid robot. Your task is to convert the user's natural language goal into a sequence of ROS 2 actions.

    User Goal: {goal}

    Environmental Context:
    - Robot State: {context['robot_state']}
    - Object Locations: {context['object_locations']}
    - Navigable Areas: {context['navigable_areas']}
    - Robot Capabilities: {context['robot_capabilities']}
    - Safety Constraints: {context['safety_constraints']}

    Generate a sequence of ROS 2 actions to achieve the goal. Each action should be one of:
    - navigation: Move to a specific location
    - manipulation: Manipulate an object
    - perception: Sense the environment
    - communication: Communicate with the user

    Ensure the plan is safe, executable, and considers the environmental constraints.
    """
    return prompt

def _get_system_prompt(self) -> str:
    """System prompt defining the cognitive planner's role and constraints"""
    return """
    You are a cognitive planning system for a humanoid robot. Your role is to interpret natural language goals and convert them into structured ROS 2 action sequences.

    Guidelines:
    1. Always prioritize safety in your plans
    2. Consider the robot's current state and capabilities
    3. Break complex goals into simple, executable actions
    4. Include environmental constraints in your planning
    5. Generate specific, measurable action parameters
    6. Add error handling considerations where appropriate
    """
```

### Safety and Validation Layer

Before executing any plan, the system must validate that the generated actions are safe and executable within the current environment.

```python
class PlanValidator:
    def __init__(self):
        self.safety_rules = self._load_safety_rules()

    def validate_plan(self, plan: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Validate the generated plan for safety and feasibility"""
        validation_result = {
            "is_valid": True,
            "warnings": [],
            "errors": [],
            "modified_plan": plan.copy()
        }

        for i, action in enumerate(plan):
            # Check navigation safety
            if action["action_type"] == "navigation":
                nav_ok, nav_error = self._validate_navigation(action, context)
                if not nav_ok:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append(f"Action {i}: {nav_error}")

            # Check manipulation safety
            elif action["action_type"] == "manipulation":
                manip_ok, manip_error = self._validate_manipulation(action, context)
                if not manip_ok:
                    validation_result["is_valid"] = False
                    validation_result["errors"].append(f"Action {i}: {manip_error}")

        return validation_result

    def _validate_navigation(self, action: Dict[str, Any], context: Dict[str, Any]) -> tuple:
        """Validate navigation action for safety"""
        target_pos = action["parameters"].get("target_position", {})

        # Check if target is in navigable area
        if not self._is_in_navigable_area(target_pos, context["navigable_areas"]):
            return False, f"Target position {target_pos} is not in navigable area"

        # Check safety constraints
        if self._violates_safety_constraints(target_pos, context["safety_constraints"]):
            return False, f"Target position {target_pos} violates safety constraints"

        return True, None
```

## Practical Implementation Example

### Complete Cognitive Planning Pipeline

Here's a complete example of the cognitive planning pipeline in action:

```python
def execute_cognitive_plan(self, natural_language_goal: str):
    """Complete pipeline: goal → plan → validation → execution"""

    # 1. Get environmental context
    context = self.get_environment_context()

    # 2. Generate plan using LLM
    raw_plan = self.generate_plan(natural_language_goal, context)

    # 3. Validate the plan
    validator = PlanValidator()
    validation_result = validator.validate_plan(raw_plan, context)

    if not validation_result["is_valid"]:
        rospy.logerr(f"Plan validation failed: {validation_result['errors']}")
        return False

    # 4. Execute validated plan
    return self._execute_plan(validation_result["modified_plan"])

def _execute_plan(self, plan: List[Dict[str, Any]]) -> bool:
    """Execute the validated plan step by step"""
    for i, action in enumerate(plan):
        rospy.loginfo(f"Executing action {i+1}/{len(plan)}: {action['description']}")

        try:
            if action["action_type"] == "navigation":
                success = self._execute_navigation_action(action["parameters"])
            elif action["action_type"] == "manipulation":
                success = self._execute_manipulation_action(action["parameters"])
            elif action["action_type"] == "perception":
                success = self._execute_perception_action(action["parameters"])
            elif action["action_type"] == "communication":
                success = self._execute_communication_action(action["parameters"])
            else:
                rospy.logerr(f"Unknown action type: {action['action_type']}")
                return False

            if not success:
                rospy.logerr(f"Action {i+1} failed: {action['description']}")
                return False

        except Exception as e:
            rospy.logerr(f"Error executing action {i+1}: {e}")
            return False

    rospy.loginfo("Plan executed successfully")
    return True
```

## Testing and Evaluation

### Plan Quality Metrics

To ensure the cognitive planning system performs well, we need to evaluate the quality of generated plans:

```python
class PlanEvaluator:
    def evaluate_plan(self, goal: str, generated_plan: List[Dict[str, Any]],
                     expected_outcome: str) -> Dict[str, float]:
        """Evaluate the quality of a generated plan"""
        metrics = {
            "goal_achievement_rate": 0.0,
            "plan_efficiency": 0.0,
            "safety_compliance": 0.0,
            "naturalness": 0.0  # How natural the plan seems to humans
        }

        # Implementation of evaluation metrics
        # This would involve simulating or executing the plan and measuring outcomes
        return metrics
```

## Summary

This chapter has covered the implementation of cognitive planning using LLMs to convert natural language goals into structured ROS 2 plans. The system leverages environmental context and safety validation to generate executable plans that bridge high-level human goals with low-level robot actions.

In the next chapter, we'll explore the capstone integration that brings together voice, planning, navigation, perception, and manipulation in a complete autonomous system.