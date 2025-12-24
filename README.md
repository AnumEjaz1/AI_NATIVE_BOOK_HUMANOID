# AI Native Book - Humanoid Robotics

This repository contains the AI Native Book on Humanoid Robotics, a comprehensive guide to Physical AI and humanoid robotics.

## About

This book is designed for advanced students, developers, and educators entering Physical AI and humanoid robotics with basic Python knowledge. Each module builds upon the previous one, creating a comprehensive understanding of humanoid robot systems.

## Modules

- **Module 1**: The Robotic Nervous System (ROS 2) - Learn about ROS 2 as the core middleware for humanoid robot control
- Additional modules will be added covering simulation, perception, and AI-driven autonomy

## Setup

To run this documentation site locally:

1. Make sure you have Node.js (version 18.0 or higher) and npm installed
2. Clone this repository
3. Navigate to the project directory
4. Install dependencies: `npm install`
5. Start the development server: `npm start`

The site will be available at http://localhost:3000

## Development

During development, the site will automatically reload when you make changes to any of the markdown files in the `docs/` directory. The development server will watch for changes and rebuild the site automatically.

To build a production version of the site, run:
```bash
npm run build
```

To serve the production build locally for testing:
```bash
npm run serve
```

## Structure

The documentation is organized in the `docs/` directory:
- `docs/intro.md` - Introduction to the book
- `docs/module-1/` - Module 1: The Robotic Nervous System (ROS 2)
  - `chapter-1-ros2-architecture.md` - ROS 2 Architecture Fundamentals
  - `chapter-2-python-agents-rclpy.md` - Python Agents and Robot Control
  - `chapter-3-urdf-humanoids.md` - Robot Modeling with URDF

The site configuration is in:
- `docusaurus.config.js` - Main Docusaurus configuration
- `sidebars.js` - Navigation sidebar structure
- `package.json` - Project dependencies and scripts

## Contributing

This project follows the Spec-Kit Plus methodology for spec-driven development. See the `specs/` directory for implementation plans and task breakdowns.

To contribute:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test the site locally
5. Submit a pull request