import React from 'react';
import './TopMenu.css';

interface TopMenuProps {
  hasError: boolean;
}

const TopMenu: React.FC<TopMenuProps> = ({ hasError }) => {
  return (
    <div className={`top-menu ${hasError ? 'error' : ''}`}>
      <div className="menu-content">
        <h1 className="menu-title">Internal Sea</h1>
        <nav className="menu-nav">
          <a href="/session" className="menu-link">Session</a>
        </nav>
      </div>
    </div>
  );
};

export default TopMenu;

