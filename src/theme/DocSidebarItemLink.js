import React from 'react';
import Link from '@docusaurus/Link';
import { useLocation } from '@docusaurus/router';
import { useProgress } from '@site/src/contexts/ProgressContext';
import clsx from 'clsx';

export default function DocSidebarItemLink({ item, onItemClick, activePath, level, index, ...props }) {
  const { isCompleted, isViewed } = useProgress();
  const location = useLocation();
  const { href, label } = item;

  const isActive = activePath === href || location.pathname === href;
  const completed = isCompleted(href || label);
  const viewed = isViewed(href || label);

  return (
    <li className="menu__list-item">
      <Link
        className={clsx(
          'menu__link',
          {
            'menu__link--active': isActive,
            'menu__link--completed': completed,
            'menu__link--viewed': viewed,
          }
        )}
        to={href}
        {...(isExternalLink(href)
          ? { rel: 'noopener noreferrer', target: '_blank' }
          : {})}
        onClick={onItemClick}
      >
        {completed && (
          <span className="completion-badge" title="Completed">
            ✓
          </span>
        )}
        {label}
      </Link>
    </li>
  );
}

function isExternalLink(href) {
  return href.startsWith('http');
}