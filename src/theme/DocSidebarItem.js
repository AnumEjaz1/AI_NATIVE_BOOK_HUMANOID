import React from 'react';
import DocSidebarItemCategory from '@theme/DocSidebarItem/Category';
import DocSidebarItemLink from '@theme/DocSidebarItem/Link';
import { useProgress } from '@site/src/contexts/ProgressContext';

export default function DocSidebarItem({ item, ...props }) {
  const { getProgressPercentage } = useProgress();

  if (item.type === 'category') {
    // Calculate progress for this category
    const allItems = item.items.flatMap(flattenItems);
    const progressPercentage = getProgressPercentage(allItems);

    return (
      <div className="menu__list-item--with-progress">
        <div className="menu__list-item-meta">
          <div className="progress-indicator">
            <div className="progress-bar">
              <div
                className="progress-fill"
                style={{ width: `${progressPercentage}%` }}
              ></div>
            </div>
            <span className="progress-text">{progressPercentage}%</span>
          </div>
        </div>
        <DocSidebarItemCategory item={item} {...props} />
      </div>
    );
  }

  return item.type === 'link' || item.type === 'doc' ? (
    <DocSidebarItemLink item={item} {...props} />
  ) : (
    <DocSidebarItemCategory item={item} {...props} />
  );
}

// Helper function to flatten nested items for progress calculation
const flattenItems = (item) => {
  if (item.type === 'category') {
    return item.items.flatMap(flattenItems);
  }
  return [item.href || item.docId || item.label];
};