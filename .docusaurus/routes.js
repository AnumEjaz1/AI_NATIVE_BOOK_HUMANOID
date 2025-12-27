import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/__docusaurus/debug',
    component: ComponentCreator('/__docusaurus/debug', '5b9'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/config',
    component: ComponentCreator('/__docusaurus/debug/config', '6c9'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/content',
    component: ComponentCreator('/__docusaurus/debug/content', '600'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/globalData',
    component: ComponentCreator('/__docusaurus/debug/globalData', 'fd1'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/metadata',
    component: ComponentCreator('/__docusaurus/debug/metadata', 'a56'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/registry',
    component: ComponentCreator('/__docusaurus/debug/registry', '02c'),
    exact: true
  },
  {
    path: '/__docusaurus/debug/routes',
    component: ComponentCreator('/__docusaurus/debug/routes', 'dc5'),
    exact: true
  },
  {
    path: '/docs',
    component: ComponentCreator('/docs', '04d'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '016'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', 'a06'),
            routes: [
              {
                path: '/docs/intro',
                component: ComponentCreator('/docs/intro', 'aed'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1/',
                component: ComponentCreator('/docs/module-1/', '9bb'),
                exact: true
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
                path: '/docs/module-2/',
                component: ComponentCreator('/docs/module-2/', '2d0'),
                exact: true
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
                path: '/docs/module-3/',
                component: ComponentCreator('/docs/module-3/', '7bf'),
                exact: true
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
                path: '/docs/module-4/',
                component: ComponentCreator('/docs/module-4/', '668'),
                exact: true
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
