import React from 'react';
import { useProgress } from '@site/src/contexts/ProgressContext';
import { useLocation } from '@docusaurus/router';
import Link from '@docusaurus/Link';
import clsx from 'clsx';

// Component to display progress indicators in sidebar
const ProgressSidebarItem = ({ item, level = 0 }) => {
  const { isCompleted, isViewed, getProgressPercentage } = useProgress();
  const location = useLocation();

  // Determine if this item is the current page
  const isCurrentPage = location.pathname.includes(item.docId || item.href || '');

  // Determine if this is a category with sub-items
  if (item.type === 'category') {
    // Calculate progress for this category
    const allItems = item.items.flatMap(flattenItems);
    const progressPercentage = getProgressPercentage(allItems);

    return (
      <div className={clsx('menu__list-item', level > 0 && 'menu__list-item--nested')}>
        <div className={clsx('menu__list-item-collapsible', isCurrentPage && 'menu__list-item--active')}>
          <div className="menu__list-item-collapsible-content">
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
            <div className="menu__list-item-content">
              <span className={clsx('menu__list-item-title', isCurrentPage && 'menu__list-item-title--active')}>
                {item.label}
              </span>
            </div>
          </div>
        </div>
        <ul className="menu__list">
          {item.items.map((subItem, index) => (
            <li key={subItem.docId || subItem.href || index} className="menu__list-item">
              <ProgressSidebarItem item={subItem} level={level + 1} />
            </li>
          ))}
        </ul>
      </div>
    );
  } else if (item.type === 'link' || item.docId) {
    // For regular link items
    const itemId = item.docId || item.href || item.label;
    const completed = isCompleted(itemId);
    const viewed = isViewed(itemId);

    return (
      <div className={clsx('menu__list-item-content', isCurrentPage && 'menu__list-item-content--active')}>
        <Link
          className={clsx(
            'menu__link',
            isCurrentPage && 'menu__link--active',
            completed && 'menu__link--completed',
            viewed && 'menu__link--viewed'
          )}
          to={item.href || `docs/${item.docId}`}
          aria-current={isCurrentPage ? 'page' : undefined}
        >
          {completed && <span className="completion-badge">✓ </span>}
          {item.label}
        </Link>
      </div>
    );
  }

  return null;
};

// Helper function to flatten nested items for progress calculation
const flattenItems = (item) => {
  if (item.type === 'category') {
    return item.items.flatMap(flattenItems);
  }
  return [item.docId || item.href || item.label];
};

// Main progress sidebar component
const ProgressSidebar = ({ sidebar }) => {
  const { markViewed } = useProgress();
  const location = useLocation();

  // Mark current page as viewed when location changes
  React.useEffect(() => {
    const currentPath = location.pathname.replace('/docs/', '').replace('/', '');
    if (currentPath) {
      markViewed(currentPath);
    }
  }, [location.pathname, markViewed]);

  return (
    <nav className="menu">
      <ul className="menu__list">
        {sidebar.map((item, index) => (
          <li key={item.label || index} className="menu__list-item">
            <ProgressSidebarItem item={item} />
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default ProgressSidebar;