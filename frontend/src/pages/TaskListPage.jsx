import { useEffect } from 'react';
import { Box, Typography, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { useTask } from '../contexts/TaskContext';
import { Card, Button, Loader } from '../components/common';
import { useApp } from '../contexts/AppContext';

export const TaskListPage = () => {
  const navigate = useNavigate();
  const { tasks, fetchTasks, deleteTask } = useTask();
  const { loading } = useApp();

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleDelete = async (id) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      await deleteTask(id);
    }
  };

  if (loading) return <Loader />;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h4">Tasks</Typography>
        <Button variant="contained" onClick={() => navigate('/tasks/create')}>
          Create Task
        </Button>
      </Box>

      {tasks.length === 0 ? (
        <Typography variant="body1" color="text.secondary">
          No tasks found. Create your first task!
        </Typography>
      ) : (
        <Grid container spacing={3}>
          {tasks.map((task) => (
            <Grid item xs={12} md={6} key={task.id}>
              <Card>
                <Typography variant="h6" gutterBottom>
                  {task.title}
                </Typography>
                <Typography variant="body2" color="text.secondary" paragraph>
                  {task.description}
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button size="small" onClick={() => navigate(`/tasks/${task.id}`)}>
                    View
                  </Button>
                  <Button size="small" onClick={() => navigate(`/tasks/${task.id}/edit`)}>
                    Edit
                  </Button>
                  <Button size="small" color="error" onClick={() => handleDelete(task.id)}>
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
