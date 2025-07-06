import React, { useState } from 'react';
import './TodoForm.css';

const TodoForm = ({ onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    priority: 3 // Default medium priority
  });
  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'priority' ? parseInt(value) : value
    }));
    
    // Clear error when user starts typing
    if (errors[name]) {
      setErrors(prev => ({
        ...prev,
        [name]: ''
      }));
    }
  };

  const validateForm = () => {
    const newErrors = {};
    
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    
    if (formData.description.length > 100) {
      newErrors.description = 'Description must be 100 characters or less';
    }
    
    if (formData.priority < 1 || formData.priority > 5) {
      newErrors.priority = 'Priority must be between 1 and 5';
    }
    
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    
    if (validateForm()) {
      onSubmit({
        title: formData.title.trim(),
        description: formData.description.trim(),
        priority: formData.priority
      });
      
      // Reset form
      setFormData({ title: '', description: '', priority: 3 });
      setErrors({});
    }
  };

  const handleCancel = () => {
    setFormData({ title: '', description: '', priority: 3 });
    setErrors({});
    onCancel();
  };

  const getPriorityLabel = (priority) => {
    const labels = {
      1: 'Very High',
      2: 'High', 
      3: 'Medium',
      4: 'Low',
      5: 'Very Low'
    };
    return labels[priority] || 'Medium';
  };

  return (
    <div className="todo-form-container">
      <form onSubmit={handleSubmit} className="todo-form">
        <h3>Add New Todo</h3>
        
        <div className="form-group">
          <label htmlFor="title">Title *</label>
          <input
            type="text"
            id="title"
            name="title"
            value={formData.title}
            onChange={handleChange}
            className={`form-control ${errors.title ? 'error' : ''}`}
            placeholder="Enter todo title"
            maxLength="100"
          />
          {errors.title && <span className="error-text">{errors.title}</span>}
        </div>
        
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <textarea
            id="description"
            name="description"
            value={formData.description}
            onChange={handleChange}
            className={`form-control ${errors.description ? 'error' : ''}`}
            placeholder="Enter description (optional)"
            rows="4"
            maxLength="100"
          />
          <div className="char-count">
            {formData.description.length}/100 characters
          </div>
          {errors.description && <span className="error-text">{errors.description}</span>}
        </div>

        <div className="form-group">
          <label htmlFor="priority">Priority</label>
          <select
            id="priority"
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className={`form-control ${errors.priority ? 'error' : ''}`}
          >
            <option value={1}>1 - Very High</option>
            <option value={2}>2 - High</option>
            <option value={3}>3 - Medium</option>
            <option value={4}>4 - Low</option>
            <option value={5}>5 - Very Low</option>
          </select>
          {errors.priority && <span className="error-text">{errors.priority}</span>}
        </div>
        
        <div className="form-actions">
          <button type="submit" className="btn btn-primary">
            Add Todo
          </button>
          <button 
            type="button" 
            onClick={handleCancel}
            className="btn btn-secondary"
          >
            Cancel
          </button>
        </div>
      </form>
    </div>
  );
};

export default TodoForm; 