import React from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function CodeBlockContent({
  children,
  className,
  metastring,
  title,
  showCopyButton,
  copyButtonAriaLabel,
  ...props
}) {
  return (
    <div className={clsx('code-block-content', styles.container, className)}>
      {title && (
        <div className={styles.codeBlockTitle}>
          <span className={styles.codeBlockTitleText}>{title}</span>
        </div>
      )}
      <div className={styles.codeBlockContent}>
        <pre {...props} className={clsx('prism-code', styles.codeBlock)}>
          {children}
        </pre>
        {showCopyButton && (
          <div className={styles.codeBlockCopyButton}>
            <button
              className={clsx('clean-btn', styles.copyButton)}
              aria-label={copyButtonAriaLabel}
            >
              Copy
            </button>
          </div>
        )}
      </div>
    </div>
  );
}