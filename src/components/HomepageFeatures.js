import React from 'react';
import clsx from 'clsx';
import styles from './HomepageFeatures.module.css';

const FeatureList = [
  {
    title: 'Module 1: ROS 2 (Robotic Nervous System)',
    description: (
      <>
        Learn ROS 2 fundamentals including nodes, topics, services, and actions.
        Understand how to create Python agents with rclpy and build URDF models for humanoid robots.
        Establish the foundation for all subsequent modules.
      </>
    ),
  },
  {
    title: 'Module 2: Digital Twin (Gazebo & Unity)',
    description: (
      <>
        Master physics simulation with Gazebo, including gravity, collisions, and joint dynamics.
        Learn high-fidelity interaction with Unity for visualization and perception.
        Create realistic environments for safe testing before real-world deployment.
      </>
    ),
  },
  {
    title: 'Module 3: AI-Robot Brain (Isaac & Nav2)',
    description: (
      <>
        Explore NVIDIA Isaac for accelerated perception and synthetic data generation.
        Implement navigation with Nav2 for humanoid robots, including path planning and obstacle avoidance.
        Integrate perception and navigation for intelligent robot behavior.
      </>
    ),
  },
  {
    title: 'Module 4: Vision-Language-Action (VLA)',
    description: (
      <>
        Combine voice, vision, and control for natural human-robot interaction.
        Use LLMs for cognitive planning and convert natural language goals into structured ROS 2 plans.
        Build end-to-end autonomous humanoid systems with integrated perception, reasoning, and actuation.
      </>
    ),
  },
];

function Feature({title, description}) {
  return (
    <div className={clsx('col col--3')}>
      <div className="text--center padding-horiz--md">
        <h3>{title}</h3>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={clsx(styles.features, 'homepage-features')}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}