import { useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { useNavigate, useParams } from 'react-router-dom';
import { useTask } from '../contexts/TaskContext';
import { Card, Button, Loader } from '../components/common';
import { useApp } from '../contexts/AppContext';

export const TaskDetailPage = () => {
  const navigate = useNavigate();
  const { id } = useParams();
  const { selectedTask, fetchTaskById } = useTask();
  const { loading } = useApp();

  useEffect(() => {
    fetchTaskById(id);
  }, [id, fetchTaskById]);

  if (loading) return <Loader />;

  if (!selectedTask) return null;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">{selectedTask.title}</Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button variant="contained" onClick={() => navigate(`/tasks/${id}/edit`)}>
            Edit
          </Button>
          <Button variant="outlined" onClick={() => navigate('/tasks')}>
            Back
          </Button>
        </Box>
      </Box>

      <Card>
        <Typography variant="h6" gutterBottom>
          Description
        </Typography>
        <Typography variant="body1" color="text.secondary">
          {selectedTask.description || 'No description provided'}
        </Typography>
      </Card>
    </Box>
  );
};
