import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import HomepageFeatures from '@site/src/components/HomepageFeatures';

import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <div className={styles.heroContent}>
          <h1 className="hero__title">{siteConfig.title}</h1>
          <p className="hero__subtitle">{siteConfig.tagline}</p>
          <p className={styles.heroDescription}>
            A comprehensive guide to Physical AI and Humanoid Robotics, covering the complete learning journey from foundational ROS 2 concepts to advanced Vision-Language-Action systems.
          </p>
          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              Get Started
            </Link>
            <Link
              className="button button--outline button--lg"
              to="/docs/module-1/chapter-1-ros2-architecture">
              Explore Modules
            </Link>
          </div>
        </div>
      </div>
    </header>
  );
}

export default function Home() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Physical AI Book - ${siteConfig.title}`}
      description="A comprehensive guide to Physical AI and Humanoid Robotics, covering ROS 2, simulation, AI, and autonomous systems">
      <HomepageHeader />
      <main>
        <HomepageFeatures />
      </main>
    </Layout>
  );
}