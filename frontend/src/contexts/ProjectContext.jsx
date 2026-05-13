import { createContext, useContext, useState, useCallback } from 'react';
import { projectService } from '../services/projectService';
import { useApp } from './AppContext';

const ProjectContext = createContext();

export const useProject = () => {
  const context = useContext(ProjectContext);
  if (!context) {
    throw new Error('useProject must be used within ProjectProvider');
  }
  return context;
};

export const ProjectProvider = ({ children }) => {
  const [projects, setProjects] = useState([]);
  const [selectedProject, setSelectedProject] = useState(null);
  const { setLoading, showNotification } = useApp();

  const fetchProjects = useCallback(async () => {
    try {
      setLoading(true);
      const data = await projectService.getAll();
      setProjects(data);
    } catch (error) {
      showNotification(error.message || 'Failed to fetch projects', 'error');
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const fetchProjectById = useCallback(async (id) => {
    try {
      setLoading(true);
      const data = await projectService.getById(id);
      setSelectedProject(data);
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to fetch project', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const createProject = useCallback(async (projectData) => {
    try {
      setLoading(true);
      const data = await projectService.create(projectData);
      setProjects((prev) => [...prev, data]);
      showNotification('Project created successfully', 'success');
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to create project', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const updateProject = useCallback(async (id, projectData) => {
    try {
      setLoading(true);
      const data = await projectService.update(id, projectData);
      setProjects((prev) => prev.map((p) => (p.id === id ? data : p)));
      showNotification('Project updated successfully', 'success');
      return data;
    } catch (error) {
      showNotification(error.message || 'Failed to update project', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const deleteProject = useCallback(async (id) => {
    try {
      setLoading(true);
      await projectService.delete(id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
      showNotification('Project deleted successfully', 'success');
    } catch (error) {
      showNotification(error.message || 'Failed to delete project', 'error');
      throw error;
    } finally {
      setLoading(false);
    }
  }, [setLoading, showNotification]);

  const value = {
    projects,
    selectedProject,
    fetchProjects,
    fetchProjectById,
    createProject,
    updateProject,
    deleteProject,
  };

  return <ProjectContext.Provider value={value}>{children}</ProjectContext.Provider>;
};
