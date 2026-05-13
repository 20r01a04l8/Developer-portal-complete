import { useEffect } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useProject } from '../contexts/ProjectContext';
import { Card, Button, Loader } from '../components/common';
import { useApp } from '../contexts/AppContext';

export const ProjectListPage = () => {
  const navigate = useNavigate();
  const { projects, fetchProjects, deleteProject } = useProject();
  const { loading } = useApp();

  useEffect(() => {
    fetchProjects();
  }, [fetchProjects]);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this project?')) {
      await deleteProject(id);
    }
  };

  if (loading) return <Loader />;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Projects</Typography>
        <Button variant="contained" onClick={() => navigate('/projects/create')}>
          Create Project
        </Button>
      </Box>

      {projects.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          No projects found. Create your first project!
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {projects.map((project) => (
            <Grid item xs={12} md={6} key={project.id}>
              <Card>
                <Typography variant="h6" gutterBottom>
                  {project.name}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {project.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button size="small" onClick={() => navigate(`/projects/${project.id}`)}>
                    View
                  </Button>
                  <Button size="small" onClick={() => navigate(`/projects/${project.id}/edit`)}>
                    Edit
                  </Button>
                  <Button size="small" color="error" onClick={() => handleDelete(project.id)}>
                    Delete
                  </Button>
                </Box>
              </Card>
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
};
