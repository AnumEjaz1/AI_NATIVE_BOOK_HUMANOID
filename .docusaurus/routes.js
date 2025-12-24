import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '217'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', 'b5e'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '7fe'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/chapter-1-ros2-architecture',
                component: ComponentCreator('/docs/module-1/chapter-1-ros2-architecture', '9a3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/chapter-2-python-agents-rclpy',
                component: ComponentCreator('/docs/module-1/chapter-2-python-agents-rclpy', '6c0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/chapter-3-urdf-humanoids',
                component: ComponentCreator('/docs/module-1/chapter-3-urdf-humanoids', 'bac'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/chapter-1-physics-simulation-with-gazebo',
                component: ComponentCreator('/docs/module-2/chapter-1-physics-simulation-with-gazebo', '9ee'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/chapter-2-high-fidelity-interaction-with-unity',
                component: ComponentCreator('/docs/module-2/chapter-2-high-fidelity-interaction-with-unity', '189'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/chapter-3-sensor-simulation-for-perception',
                component: ComponentCreator('/docs/module-2/chapter-3-sensor-simulation-for-perception', '9d8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2/glossary',
                component: ComponentCreator('/docs/module-2/glossary', '06a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/chapter-1-nvidia-isaac-sim-and-synthetic-data',
                component: ComponentCreator('/docs/module-3/chapter-1-nvidia-isaac-sim-and-synthetic-data', 'c87'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/chapter-2-isaac-ros-and-accelerated-perception',
                component: ComponentCreator('/docs/module-3/chapter-2-isaac-ros-and-accelerated-perception', 'ec7'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/chapter-3-navigation-with-nav2-for-humanoid-robots',
                component: ComponentCreator('/docs/module-3/chapter-3-navigation-with-nav2-for-humanoid-robots', 'e83'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3/glossary',
                component: ComponentCreator('/docs/module-3/glossary', 'a21'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4/chapter-1-voice-to-action',
                component: ComponentCreator('/docs/module-4/chapter-1-voice-to-action', '154'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4/chapter-2-cognitive-planning',
                component: ComponentCreator('/docs/module-4/chapter-2-cognitive-planning', 'c22'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4/chapter-3-capstone-integration',
                component: ComponentCreator('/docs/module-4/chapter-3-capstone-integration', 'c1d'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '/',
    component: ComponentCreator('/', '2d1'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
