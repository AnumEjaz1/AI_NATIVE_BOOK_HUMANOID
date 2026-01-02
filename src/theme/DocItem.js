import React, { useEffect } from 'react';
import DocItem from '@theme-original/DocItem';
import { useProgress } from '@site/src/contexts/ProgressContext';
import { useLocation } from '@docusaurus/router';

export default function DocItemWrapper(props) {
  const { markCompleted, markViewed } = useProgress();
  const location = useLocation();

  // Extract document ID from the route
  const docId = location.pathname.replace('/docs/', '').replace('/', '');

  // Mark as viewed when component mounts
  useEffect(() => {
    if (docId) {
      markViewed(docId);
    }
  }, [docId, markViewed]);

  // Add a completion button or functionality
  const markAsCompleted = () => {
    if (docId) {
      markCompleted(docId);
    }
  };

  return (
    <>
      <div className="doc-completion-controls">
        <button
          className="button button--sm button--primary"
          onClick={markAsCompleted}
          style={{ marginBottom: '1rem' }}
        >
          Mark as Completed
        </button>
      </div>
      <DocItem {...props} />
    </>
  );
}