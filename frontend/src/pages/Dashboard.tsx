import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import './Dashboard.css';

interface DashboardStats {
  totalUsers: number;
  totalItems: number;
  recentItems: any[];
}

const Dashboard: React.FC = () => {
  const { user, token } = useAuth();
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [usersResponse, itemsResponse] = await Promise.all([
        axios.get('/api/v1/users/', {
          headers: { Authorization: `Bearer ${token}` }
        }),
        axios.get('/api/v1/items/', {
          headers: { Authorization: `Bearer ${token}` }
        })
      ]);

      setStats({
        totalUsers: usersResponse.data.length,
        totalItems: itemsResponse.data.length,
        recentItems: itemsResponse.data.slice(0, 5)
      });
    } catch (err: any) {
      setError('Failed to load dashboard data');
      console.error('Dashboard error:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="dashboard">
        <div className="loading">Loading dashboard...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="dashboard">
        <div className="error">{error}</div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <div className="dashboard-header">
        <h1>Dashboard</h1>
        <p>Welcome back, {user?.full_name}!</p>
      </div>

      <div className="stats-grid">
        <div className="stat-card">
          <h3>Total Users</h3>
          <div className="stat-value">{stats?.totalUsers || 0}</div>
        </div>
        
        <div className="stat-card">
          <h3>Total Items</h3>
          <div className="stat-value">{stats?.totalItems || 0}</div>
        </div>
      </div>

      <div className="recent-items">
        <h2>Recent Items</h2>
        {stats?.recentItems && stats.recentItems.length > 0 ? (
          <div className="items-list">
            {stats.recentItems.map((item: any) => (
              <div key={item.id} className="item-card">
                <h4>{item.title}</h4>
                <p>{item.description}</p>
                <small>Created: {new Date(item.created_at).toLocaleDateString()}</small>
              </div>
            ))}
          </div>
        ) : (
          <p>No items found.</p>
        )}
      </div>
    </div>
  );
};

export default Dashboard; 