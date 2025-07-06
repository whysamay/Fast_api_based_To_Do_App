import React, { useState, useEffect } from 'react';
import api from '../services/api';
import TodoItem from './TodoItem';
import TodoForm from './TodoForm';
import './TodoList.css';

const TodoList = () => {
  const [todos, setTodos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // all, active, completed
  const [showForm, setShowForm] = useState(false);

  useEffect(() => {
    fetchTodos();
  }, []);

  const fetchTodos = async () => {
    try {
      setLoading(true);
      const response = await api.get('/todos/');
      setTodos(response.data);
      setError(null);
    } catch (error) {
      setError('Failed to fetch todos');
      console.error('Error fetching todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (todoData) => {
    try {
      // Transform the data to match backend expectations
      const todoRequest = {
        title: todoData.title,
        description: todoData.description,
        priority: todoData.priority,
        complete: false // Default to incomplete
      };
      
      const response = await api.post('/todos/', todoRequest);
      setTodos([...todos, response.data]);
      setShowForm(false);
      setError(null);
    } catch (error) {
      setError('Failed to add todo');
      console.error('Error adding todo:', error);
    }
  };

  const updateTodo = async (id, todoData) => {
    try {
      // Find the current todo to get its existing data
      const currentTodo = todos.find(todo => todo.id === id);
      if (!currentTodo) return;
      
      // Merge the updated data with existing data
      const todoRequest = {
        title: todoData.title,
        description: todoData.description,
        priority: todoData.priority || currentTodo.priority || 1,
        complete: todoData.complete !== undefined ? todoData.complete : currentTodo.complete || false
      };
      
      const response = await api.put(`/todos/${id}`, todoRequest);
      setTodos(todos.map(todo => todo.id === id ? response.data : todo));
      setError(null);
    } catch (error) {
      setError('Failed to update todo');
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id) => {
    try {
      await api.delete(`/todos/${id}`);
      setTodos(todos.filter(todo => todo.id !== id));
      setError(null);
    } catch (error) {
      setError('Failed to delete todo');
      console.error('Error deleting todo:', error);
    }
  };

  const toggleTodo = async (id, completed) => {
    try {
      // Find the current todo to get its data
      const currentTodo = todos.find(todo => todo.id === id);
      if (!currentTodo) return;
      
      const todoRequest = {
        title: currentTodo.title,
        description: currentTodo.description,
        priority: currentTodo.priority,
        complete: !completed
      };
      
      const response = await api.put(`/todos/${id}`, todoRequest);
      setTodos(todos.map(todo => todo.id === id ? response.data : todo));
      setError(null);
    } catch (error) {
      setError('Failed to update todo');
      console.error('Error updating todo:', error);
    }
  };

  const filteredTodos = todos.filter(todo => {
    if (filter === 'active') return !todo.complete;
    if (filter === 'completed') return todo.complete;
    return true;
  }).sort((a, b) => {
    // Sort by priority (1 is highest) then by completion status
    if (a.priority !== b.priority) {
      return a.priority - b.priority;
    }
    // Completed todos go to the bottom
    if (a.complete !== b.complete) {
      return a.complete ? 1 : -1;
    }
    return 0;
  });

  const completedCount = todos.filter(todo => todo.complete).length;
  const activeCount = todos.length - completedCount;

  if (loading) {
    return <div className="loading">Loading todos...</div>;
  }

  return (
    <div className="todo-container">
      <div className="todo-header">
        <h1>My Todos</h1>
        <button 
          onClick={() => setShowForm(!showForm)} 
          className="btn btn-primary"
        >
          {showForm ? 'Cancel' : 'Add Todo'}
        </button>
      </div>

      {error && <div className="error">{error}</div>}

      {showForm && (
        <TodoForm 
          onSubmit={addTodo} 
          onCancel={() => setShowForm(false)}
        />
      )}

      <div className="todo-filters">
        <button 
          onClick={() => setFilter('all')} 
          className={`filter-btn ${filter === 'all' ? 'active' : ''}`}
        >
          All ({todos.length})
        </button>
        <button 
          onClick={() => setFilter('active')} 
          className={`filter-btn ${filter === 'active' ? 'active' : ''}`}
        >
          Active ({activeCount})
        </button>
        <button 
          onClick={() => setFilter('completed')} 
          className={`filter-btn ${filter === 'completed' ? 'active' : ''}`}
        >
          Completed ({completedCount})
        </button>
      </div>

      <div className="todo-list">
        {filteredTodos.length === 0 ? (
          <div className="empty-state">
            <p>No todos found. {filter !== 'all' && `No ${filter} todos.`}</p>
          </div>
        ) : (
          filteredTodos.map(todo => (
            <TodoItem
              key={todo.id}
              todo={todo}
              onUpdate={updateTodo}
              onDelete={deleteTodo}
              onToggle={toggleTodo}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default TodoList; 