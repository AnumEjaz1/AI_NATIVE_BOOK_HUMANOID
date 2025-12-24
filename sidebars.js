// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: 'Module 1 - The Robotic Nervous System (ROS 2)',
      items: [
        'module-1/chapter-1-ros2-architecture',
        'module-1/chapter-2-python-agents-rclpy',
        'module-1/chapter-3-urdf-humanoids',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - The Digital Twin (Gazebo & Unity)',
      items: [
        'module-2/chapter-1-physics-simulation-with-gazebo',
        'module-2/chapter-2-high-fidelity-interaction-with-unity',
        'module-2/chapter-3-sensor-simulation-for-perception',
        'module-2/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - The AI-Robot Brain (NVIDIA Isaac™)',
      items: [
        'module-3/chapter-1-nvidia-isaac-sim-and-synthetic-data',
        'module-3/chapter-2-isaac-ros-and-accelerated-perception',
        'module-3/chapter-3-navigation-with-nav2-for-humanoid-robots',
        'module-3/glossary',
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action (VLA)',
      items: [
        'module-4/chapter-1-voice-to-action',
        'module-4/chapter-2-cognitive-planning',
        'module-4/chapter-3-capstone-integration',
      ],
    },
  ],
};

module.exports = sidebars;