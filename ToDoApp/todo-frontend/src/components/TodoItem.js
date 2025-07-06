import React, { useState } from 'react';
import './TodoItem.css';

const TodoItem = ({ todo, onUpdate, onDelete, onToggle }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(todo.title);
  const [editDescription, setEditDescription] = useState(todo.description || '');
  const [editPriority, setEditPriority] = useState(todo.priority || 3);

  const handleEdit = () => {
    setIsEditing(true);
  };

  const handleSave = () => {
    if (editTitle.trim()) {
      onUpdate(todo.id, {
        title: editTitle.trim(),
        description: editDescription.trim(),
        priority: editPriority,
        complete: todo.complete || false
      });
      setIsEditing(false);
    }
  };

  const handleCancel = () => {
    setEditTitle(todo.title);
    setEditDescription(todo.description || '');
    setEditPriority(todo.priority || 3);
    setIsEditing(false);
  };

  const handleToggle = () => {
    onToggle(todo.id, todo.complete || false);
  };

  const handleDelete = () => {
    if (window.confirm('Are you sure you want to delete this todo?')) {
      onDelete(todo.id);
    }
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

  const getPriorityColor = (priority) => {
    const colors = {
      1: 'priority-very-high',
      2: 'priority-high',
      3: 'priority-medium',
      4: 'priority-low',
      5: 'priority-very-low'
    };
    return colors[priority] || 'priority-medium';
  };

  if (isEditing) {
    return (
      <div className="todo-item editing">
        <div className="todo-content">
          <input
            type="text"
            value={editTitle}
            onChange={(e) => setEditTitle(e.target.value)}
            className="form-control edit-title"
            placeholder="Todo title"
          />
          <textarea
            value={editDescription}
            onChange={(e) => setEditDescription(e.target.value)}
            className="form-control edit-description"
            placeholder="Description (optional)"
            rows="3"
            maxLength="100"
          />
          <select
            value={editPriority}
            onChange={(e) => setEditPriority(parseInt(e.target.value))}
            className="form-control edit-priority"
          >
            <option value={1}>1 - Very High</option>
            <option value={2}>2 - High</option>
            <option value={3}>3 - Medium</option>
            <option value={4}>4 - Low</option>
            <option value={5}>5 - Very Low</option>
          </select>
        </div>
        <div className="todo-actions">
          <button onClick={handleSave} className="btn btn-success">
            Save
          </button>
          <button onClick={handleCancel} className="btn btn-secondary">
            Cancel
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className={`todo-item ${todo.complete ? 'completed' : ''}`}>
      <div className="todo-content">
        <div className="todo-header">
          <label className="checkbox-container">
            <input
              type="checkbox"
              checked={todo.complete || false}
              onChange={handleToggle}
            />
            <span className="checkmark"></span>
          </label>
          <h3 className="todo-title">{todo.title}</h3>
          <span className={`priority-badge ${getPriorityColor(todo.priority)}`}>
            {todo.priority} - {getPriorityLabel(todo.priority)}
          </span>
        </div>
        {todo.description && (
          <p className="todo-description">{todo.description}</p>
        )}
        <div className="todo-meta">
          {todo.complete && (
            <span className="completed-status">✓ Completed</span>
          )}
        </div>
      </div>
      <div className="todo-actions">
        <button onClick={handleEdit} className="btn btn-secondary">
          Edit
        </button>
        <button onClick={handleDelete} className="btn btn-danger">
          Delete
        </button>
      </div>
    </div>
  );
};

export default TodoItem; 