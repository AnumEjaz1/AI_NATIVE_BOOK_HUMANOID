# Quickstart: Digital Twin Simulation Module

## Setup Docusaurus Environment

1. **Install Node.js** (version 18 or higher)
   ```bash
   # Check your Node.js version
   node --version
   ```

2. **Install Docusaurus globally** (if not already installed)
   ```bash
   npm install -g @docusaurus/core@latest
   ```

3. **Verify Docusaurus installation**
   ```bash
   npx docusaurus --version
   ```

## Initialize the Module Content

1. **Create the module directory**
   ```bash
   mkdir -p docs/module-2
   ```

2. **Create the three chapter files** as specified in the feature requirements:
   - `docs/module-2/chapter-1-physics-simulation-with-gazebo.md`
   - `docs/module-2/chapter-2-high-fidelity-interaction-with-unity.md`
   - `docs/module-2/chapter-3-sensor-simulation-for-perception.md`

3. **Add basic content structure to each chapter** (example for Chapter 1):
   ```markdown
   ---
   title: Physics Simulation with Gazebo
   sidebar_position: 1
   ---

   # Physics Simulation with Gazebo

   This chapter covers simulating gravity, collisions, joint dynamics, world files, and integrating ROS 2 with Gazebo for humanoid robots.

   ## Learning Objectives
   - Understand how to set up a physics simulation in Gazebo
   - Configure gravity and collision properties
   - Create custom world files
   - Integrate with ROS 2 for humanoid robots

   ## Introduction
   [Content for the chapter...]
   ```

## Register in Navigation

1. **Update `sidebars.js`** to include the new module:
   ```javascript
   module.exports = {
     // ... existing sidebar configuration ...
     module2: [
       {
         type: 'category',
         label: 'Module 2: Digital Twin Simulation',
         items: [
           'module-2/chapter-1-physics-simulation-with-gazebo',
           'module-2/chapter-2-high-fidelity-interaction-with-unity',
           'module-2/chapter-3-sensor-simulation-for-perception',
         ],
       },
     ],
   };
   ```

## Build and Test

1. **Build the documentation site**
   ```bash
   npm run build
   ```

2. **Start the development server**
   ```bash
   npm run start
   ```

3. **Verify the new module appears correctly** in the navigation and content renders properly.

## Content Guidelines

- Each chapter should follow the learning objectives defined in the specification
- All technical content must align with official Gazebo, Unity, and ROS 2 documentation
- Maintain terminology consistency with Module 1
- Include practical examples and hands-on exercises where appropriate
- Ensure all content is in Markdown format compatible with Docusaurus