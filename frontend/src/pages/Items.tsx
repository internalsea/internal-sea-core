import React, { useState, useEffect } from 'react';
import { useAuth } from '../contexts/AuthContext';
import axios from 'axios';
import './Items.css';

interface Item {
  id: number;
  title: string;
  description: string;
  created_at: string;
}

const Items: React.FC = () => {
  const { token } = useAuth();
  const [items, setItems] = useState<Item[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [newItem, setNewItem] = useState({ title: '', description: '' });

  useEffect(() => {
    fetchItems();
  }, []);

  const fetchItems = async () => {
    try {
      const response = await axios.get('/api/v1/items/', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setItems(response.data);
    } catch (err: any) {
      setError('Failed to load items');
      console.error('Items error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await axios.post('/api/v1/items/', newItem, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setNewItem({ title: '', description: '' });
      setShowForm(false);
      fetchItems();
    } catch (err: any) {
      setError('Failed to create item');
      console.error('Create item error:', err);
    }
  };

  const handleDelete = async (id: number) => {
    if (window.confirm('Are you sure you want to delete this item?')) {
      try {
        await axios.delete(`/api/v1/items/${id}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchItems();
      } catch (err: any) {
        setError('Failed to delete item');
        console.error('Delete item error:', err);
      }
    }
  };

  if (loading) {
    return (
      <div className="items">
        <div className="loading">Loading items...</div>
      </div>
    );
  }

  return (
    <div className="items">
      <div className="items-header">
        <h1>Items</h1>
        <button 
          className="button"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? 'Cancel' : 'Add New Item'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <div className="add-item-form">
          <h3>Add New Item</h3>
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label htmlFor="title">Title</label>
              <input
                type="text"
                id="title"
                value={newItem.title}
                onChange={(e) => setNewItem({ ...newItem, title: e.target.value })}
                required
                placeholder="Enter item title"
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="description">Description</label>
              <textarea
                id="description"
                value={newItem.description}
                onChange={(e) => setNewItem({ ...newItem, description: e.target.value })}
                placeholder="Enter item description"
                rows={3}
              />
            </div>
            
            <button type="submit" className="button">
              Create Item
            </button>
          </form>
        </div>
      )}

      <div className="items-grid">
        {items.length > 0 ? (
          items.map((item) => (
            <div key={item.id} className="item-card">
              <h3>{item.title}</h3>
              <p>{item.description}</p>
              <small>Created: {new Date(item.created_at).toLocaleDateString()}</small>
              <div className="item-actions">
                <button 
                  className="button button-danger"
                  onClick={() => handleDelete(item.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          ))
        ) : (
          <p>No items found. Create your first item!</p>
        )}
      </div>
    </div>
  );
};

export default Items; 