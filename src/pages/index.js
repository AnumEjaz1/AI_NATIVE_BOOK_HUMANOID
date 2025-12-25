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
          <div style={{textAlign: 'center', marginBottom: '1.5rem'}}>
            <h1 className="hero__title">{siteConfig.title}</h1>
            <p className="hero__subtitle">{siteConfig.tagline}</p>
          </div>

          <p className={styles.heroDescription}>
            A comprehensive guide to Physical AI and Humanoid Robotics, covering the complete learning journey from foundational ROS 2 concepts to advanced Vision-Language-Action systems.
          </p>

          <div className={styles.learningPath}>
            <h3 className={styles.learningPathTitle}>Your Learning Journey</h3>
            <div className={styles.pathSteps}>
              <div className={styles.pathStep}>
                <div className={styles.stepNumber}>1</div>
                <div className={styles.stepText}>ROS 2 Fundamentals</div>
              </div>
              <div className={styles.pathArrow}>→</div>
              <div className={styles.pathStep}>
                <div className={styles.stepNumber}>2</div>
                <div className={styles.stepText}>Digital Twins</div>
              </div>
              <div className={styles.pathArrow}>→</div>
              <div className={styles.pathStep}>
                <div className={styles.stepNumber}>3</div>
                <div className={styles.stepText}>AI-Robot Brains</div>
              </div>
              <div className={styles.pathArrow}>→</div>
              <div className={styles.pathStep}>
                <div className={styles.stepNumber}>4</div>
                <div className={styles.stepText}>VLA Systems</div>
              </div>
            </div>
          </div>

          <div className={styles.buttons}>
            <Link
              className="button button--secondary button--lg"
              to="/docs/intro">
              🚀 Start Learning
            </Link>
            <Link
              className="button button--outline button--lg"
              to="/docs/module-1/chapter-1-ros2-architecture">
              📚 Browse Modules
            </Link>
          </div>

          <div style={{marginTop: '2rem', textAlign: 'center', fontSize: '0.9rem', color: 'var(--ifm-color-emphasis-600)'}}>
            <p>Perfect for developers, researchers, and students entering the field of Physical AI and Humanoid Robotics</p>
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
        <section className={styles.featuresSection}>
          <div className="container">
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Comprehensive Learning Modules</h2>
              <p className={styles.sectionSubtitle}>Progress from foundational concepts to advanced implementations</p>
            </div>
          </div>
        </section>
        <HomepageFeatures />

        <section className={styles.whySection}>
          <div className="container">
            <div className={styles.sectionHeader}>
              <h2 className={styles.sectionTitle}>Why Learn Humanoid Robotics?</h2>
              <p className={styles.sectionSubtitle}>The future of human-robot interaction and autonomous systems</p>
            </div>

            <div className="row" style={{marginTop: '2rem'}}>
              <div className="col col--4">
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>🤖</div>
                  <h3>Cutting-edge Technology</h3>
                  <p>Master the latest technologies in robotics, AI, and autonomous systems that are shaping the future of human-robot interaction.</p>
                </div>
              </div>

              <div className="col col--4">
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>🎓</div>
                  <h3>Comprehensive Curriculum</h3>
                  <p>From ROS 2 fundamentals to advanced Vision-Language-Action systems, get a complete education in humanoid robotics.</p>
                </div>
              </div>

              <div className="col col--4">
                <div className={styles.featureCard}>
                  <div className={styles.featureIcon}>🔧</div>
                  <h3>Hands-on Practice</h3>
                  <p>Apply concepts through practical examples, simulations, and real-world implementations with industry-standard tools.</p>
                </div>
              </div>
            </div>
          </div>
        </section>

        <section className={styles.ctaSection}>
          <div className="container">
            <div className={styles.ctaContent}>
              <h2>Ready to Start Your Journey?</h2>
              <p>Join thousands of developers and researchers learning the future of robotics</p>
              <div className={styles.buttons}>
                <Link
                  className="button button--secondary button--lg"
                  to="/docs/intro">
                  Begin Learning Now
                </Link>
              </div>
            </div>
          </div>
        </section>
      </main>
    </Layout>
  );
}