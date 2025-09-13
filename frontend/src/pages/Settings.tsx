// frontend/src/pages/Settings.tsx
import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './Settings.css';

interface User {
  id: number;
  email: string;
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
  created_at: string;
  updated_at?: string;
}

interface Organization {
  id: number;
  name: string;
  description?: string;
  website?: string;
  email?: string;
  phone?: string;
  address?: string;
  is_active: boolean;
  created_at: string;
  updated_at?: string;
}

const Settings: React.FC = () => {
  const [user, setUser] = useState<User | null>(null);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    full_name: '',
    email: '',
    password: ''
  });

  useEffect(() => {
    fetchUserData();
    fetchOrganizations();
  }, []);

  const fetchUserData = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/users/me', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
      setFormData({
        full_name: response.data.full_name,
        email: response.data.email,
        password: ''
      });
    } catch (error) {
      console.error('Error fetching user data:', error);
    }
  };

  const fetchOrganizations = async () => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get('/api/v1/organizations/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setOrganizations(response.data);
    } catch (error) {
      console.error('Error fetching organizations:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const token = localStorage.getItem('token');
      const response = await axios.put('/api/v1/users/me', formData, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setUser(response.data);
      setEditing(false);
    } catch (error) {
      console.error('Error updating user:', error);
    }
  };

  if (loading) return <div className="settings-container">Loading...</div>;

  return (
    <div className="settings-container">
      <h1>Settings</h1>
      
      {/* User Information Section */}
      <div className="settings-section">
        <h2>User Information</h2>
        {editing ? (
          <form onSubmit={handleSubmit} className="settings-form">
            <div className="form-group">
              <label>Full Name:</label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({...formData, full_name: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>Email:</label>
              <input
                type="email"
                value={formData.email}
                onChange={(e) => setFormData({...formData, email: e.target.value})}
                required
              />
            </div>
            <div className="form-group">
              <label>New Password (optional):</label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({...formData, password: e.target.value})}
              />
            </div>
            <div className="form-actions">
              <button type="submit" className="btn-primary">Save Changes</button>
              <button type="button" onClick={() => setEditing(false)} className="btn-secondary">Cancel</button>
            </div>
          </form>
        ) : (
          <div className="user-info">
            <p><strong>Name:</strong> {user?.full_name}</p>
            <p><strong>Email:</strong> {user?.email}</p>
            <p><strong>Status:</strong> {user?.is_active ? 'Active' : 'Inactive'}</p>
            <p><strong>Role:</strong> {user?.is_superuser ? 'Super User' : 'User'}</p>
            <p><strong>Member since:</strong> {new Date(user?.created_at || '').toLocaleDateString()}</p>
            <button onClick={() => setEditing(true)} className="btn-primary">Edit Profile</button>
          </div>
        )}
      </div>

      {/* Organizations Section */}
      <div className="settings-section">
        <h2>Organizations</h2>
        {organizations.length === 0 ? (
          <p>No organizations found.</p>
        ) : (
          <div className="organizations-list">
            {organizations.map((org) => (
              <div key={org.id} className="organization-card">
                <h3>{org.name}</h3>
                {org.description && <p>{org.description}</p>}
                {org.website && <p><strong>Website:</strong> <a href={org.website} target="_blank" rel="noopener noreferrer">{org.website}</a></p>}
                {org.email && <p><strong>Email:</strong> {org.email}</p>}
                {org.phone && <p><strong>Phone:</strong> {org.phone}</p>}
                {org.address && <p><strong>Address:</strong> {org.address}</p>}
                <p><strong>Status:</strong> {org.is_active ? 'Active' : 'Inactive'}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default Settings;