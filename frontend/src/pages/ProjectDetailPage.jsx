import { useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { useProject } from '../contexts/ProjectContext';
import { Card, Button, Loader } from '../components/common';
import { useApp } from '../contexts/AppContext';

export const ProjectDetailPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { selectedProject, fetchProjectById } = useProject();
  const { loading } = useApp();

  useEffect(() => {
    fetchProjectById(id);
  }, [id, fetchProjectById]);

  if (loading) return <Loader />;

  if (!selectedProject) return null;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">{selectedProject.name}</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="contained" onClick={() => navigate(`/projects/${id}/edit`)}>
            Edit
          </Button>
          <Button variant="outlined" onClick={() => navigate('/projects')}>
            Back
          </Button>
        </Box>
      </Box>

      <Card>
        <Typography variant="h6" gutterBottom>
          Description
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {selectedProject.description || 'No description provided'}
        </Typography>
      </Card>
    </Box>
  );
};
