# Data Model: Module 1 – The Robotic Nervous System (ROS 2)

## Entities

### Chapter Document
- **name**: String (e.g., "chapter-1-ros2-architecture")
- **title**: String (e.g., "ROS 2 Architecture Fundamentals")
- **content**: Markdown text
- **module**: Reference to Module 1
- **position**: Integer (1-3 for this module)
- **prerequisites**: List of prerequisite concepts
- **learning_objectives**: List of learning objectives

### Module
- **name**: String ("Module 1 - The Robotic Nervous System (ROS 2)")
- **description**: String (overview of the module)
- **chapters**: List of Chapter Documents
- **target_audience**: String ("Advanced students, developers, and educators")
- **prerequisites**: String ("Basic Python knowledge")

### Navigation Item
- **label**: String (display name in sidebar)
- **to**: String (relative path to document)
- **type**: String ("doc" for documentation pages)
- **id**: String (unique identifier for the navigation item)

## Relationships
- Module contains 3 Chapter Documents (1-to-many)
- Chapter Document has one Module (many-to-one)
- Navigation Items represent the structure of the documentation site

## Validation Rules
- Each Chapter Document must have unique position within Module
- Each Chapter Document must have content that aligns with official ROS 2 documentation
- Each Chapter Document must be written in Markdown format
- Module must contain exactly 3 chapters as specified in the feature requirements

## State Transitions
- Draft → Review → Published (content workflow)
- Each chapter can be in different states during development