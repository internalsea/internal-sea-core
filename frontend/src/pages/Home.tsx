import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import './Home.css';

const Home: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="home">
      <div className="hero">
        <h1>Welcome to Internal Sea Core</h1>
        <p>A modern web application built with FastAPI and React</p>
        
        {user ? (
          <div className="hero-actions">
            <Link to="/dashboard" className="button">
              Go to Dashboard
            </Link>
            <Link to="/items" className="button button-secondary">
              View Items
            </Link>
          </div>
        ) : (
          <div className="hero-actions">
            <Link to="/login" className="button">
              Get Started
            </Link>
          </div>
        )}
      </div>

      <div className="features">
        <div className="feature-card">
          <h3>FastAPI Backend</h3>
          <p>High-performance Python web framework with automatic API documentation</p>
        </div>
        
        <div className="feature-card">
          <h3>React Frontend</h3>
          <p>Modern JavaScript library for building user interfaces</p>
        </div>
        
        <div className="feature-card">
          <h3>JWT Authentication</h3>
          <p>Secure token-based authentication system</p>
        </div>
        
        <div className="feature-card">
          <h3>Database Integration</h3>
          <p>SQLAlchemy ORM with PostgreSQL database support</p>
        </div>
      </div>
    </div>
  );
};

export default Home; 