import React, { useState } from 'react';
import { useAuth } from '../contexts/AuthContext';
import './Profile.css';

const Profile = () => {
  const { user, updateProfile, error, setError } = useAuth();
  const [isEditing, setIsEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    phone_number: user?.phone_number || ''
  });
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleEdit = () => {
    setIsEditing(true);
    setError(null);
  };

  const handleSave = async () => {
    setLoading(true);
    
    // Prepare the data for the backend
    const updateData = {};
    if (formData.first_name) updateData.first_name = formData.first_name;
    if (formData.last_name) updateData.last_name = formData.last_name;
    if (formData.phone_number) updateData.phone_number = formData.phone_number;
    
    const result = await updateProfile(updateData);
    
    if (result.success) {
      setIsEditing(false);
    }
    
    setLoading(false);
  };

  const handleCancel = () => {
    setFormData({
      first_name: user?.first_name || '',
      last_name: user?.last_name || '',
      phone_number: user?.phone_number || ''
    });
    setIsEditing(false);
    setError(null);
  };

  // Get full name for display
  const getFullName = () => {
    const firstName = user?.first_name || '';
    const lastName = user?.last_name || '';
    return `${firstName} ${lastName}`.trim() || 'Not provided';
  };

  if (!user) {
    return <div className="loading">Loading profile...</div>;
  }

  return (
    <div className="profile-container">
      <div className="profile-card">
        <h1>Profile</h1>
        
        {error && <div className="error-message">{error}</div>}
        
        <div className="profile-info">
          <div className="info-group">
            <label>Email</label>
            <p className="info-value">{user.email}</p>
          </div>
          
          <div className="info-group">
            <label>First Name</label>
            {isEditing ? (
              <input
                type="text"
                name="first_name"
                value={formData.first_name}
                onChange={handleChange}
                className="form-control"
                placeholder="Enter first name"
              />
            ) : (
              <p className="info-value">{user.first_name || 'Not provided'}</p>
            )}
          </div>
          
          <div className="info-group">
            <label>Last Name</label>
            {isEditing ? (
              <input
                type="text"
                name="last_name"
                value={formData.last_name}
                onChange={handleChange}
                className="form-control"
                placeholder="Enter last name"
              />
            ) : (
              <p className="info-value">{user.last_name || 'Not provided'}</p>
            )}
          </div>
          
          <div className="info-group">
            <label>Phone Number</label>
            {isEditing ? (
              <input
                type="tel"
                name="phone_number"
                value={formData.phone_number}
                onChange={handleChange}
                className="form-control"
                placeholder="Enter phone number"
              />
            ) : (
              <p className="info-value">{user.phone_number || 'Not provided'}</p>
            )}
          </div>
          
          <div className="info-group">
            <label>Role</label>
            <p className="info-value">{user.role || 'User'}</p>
          </div>
        </div>
        
        <div className="profile-actions">
          {isEditing ? (
            <div className="edit-actions">
              <button 
                onClick={handleSave} 
                className="btn btn-primary"
                disabled={loading}
              >
                {loading ? 'Saving...' : 'Save Changes'}
              </button>
              <button 
                onClick={handleCancel} 
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
            </div>
          ) : (
            <button onClick={handleEdit} className="btn btn-primary">
              Edit Profile
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile; 