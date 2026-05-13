import { createContext, useContext, useState, useCallback } from 'react';
import { taskService } from '../services/taskService';
import { useApp } from './AppContext';

const TaskContext = createContext();

export const useTask = () => {
  const context = useContext(TaskContext);
  if (!context) {
    throw new Error('useTask must be used within TaskProvider');
  }
  return context;
};

export const TaskProvider = ({ children }) => {
  const [tasks, setTasks] = useState([]);
  const [selectedTask, setSelectedTask] = useState(null);
  const { setLoading, showNotification } = useApp();

  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const data = await taskService.getAll();
      setTasks(data);
    } catch (error) {
      showNotification(error.message || 'Failed to fetch tasks', 'error');
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const fetchTaskById = useCallback(async (id) => {
    try {
      setLoading(true);
      const data = await taskService.getById(id);
      setSelectedTask(data);
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to fetch task', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const createTask = useCallback(async (taskData) => {
    try {
      setLoading(true);
      const data = await taskService.create(taskData);
      setTasks((prev) => [...prev, data]);
      showNotification('Task created successfully', 'success');
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to create task', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const updateTask = useCallback(async (id, taskData) => {
    try {
      setLoading(true);
      const data = await taskService.update(id, taskData);
      setTasks((prev) => prev.map((t) => (t.id === id ? data : t)));
      showNotification('Task updated successfully', 'success');
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to update task', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const deleteTask = useCallback(async (id) => {
    try {
      setLoading(true);
      await taskService.delete(id);
      setTasks((prev) => prev.filter((t) => t.id !== id));
      showNotification('Task deleted successfully', 'success');
    } catch (error) {
      showNotification(error.message || 'Failed to delete task', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const value = {
    tasks,
    selectedTask,
    fetchTasks,
    fetchTaskById,
    createTask,
    updateTask,
    deleteTask,
  };

  return <TaskContext.Provider value={value}>{children}</TaskContext.Provider>;
};
