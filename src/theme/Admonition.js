import React from 'react';
import clsx from 'clsx';
import styles from './Admonition/styles.module.css';

const AdmonitionContent = ({ children }) => (
  <div className={`${styles.admonitionContent} admonition-content`}>{children}</div>
);

const AdmonitionIcon = ({ icon }) => (
  <div className={`${styles.admonitionIcon} admonition-icon`}>
    {typeof icon === 'string' ? <span>{icon}</span> : icon}
  </div>
);

const AdmonitionTitle = ({ children, headingLevel, title }) => {
  const Heading = `h${headingLevel}`;
  return (
    <Heading className={`${styles.admonitionTitle} admonition-heading`}>
      {title}
    </Heading>
  );
};

export default function Admonition({
  children,
  title,
  type,
  icon,
  headingLevel = 5,
  className,
  ...props
}) {
  return (
    <div
      className={clsx(
        'alert',
        `alert--${type}`,
        'shadow--tl',
        className,
        styles.admonition
      )}
      {...props}
    >
      <div className={styles.admonitionHeader}>
        {icon && <AdmonitionIcon icon={icon} />}
        {title && (
          <AdmonitionTitle headingLevel={headingLevel} title={title} />
        )}
      </div>
      <AdmonitionContent>{children}</AdmonitionContent>
    </div>
  );
}