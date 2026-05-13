import { Box, Typography, Grid } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Card, Button } from '../components/common';

export const HomePage = () => {
  const navigate = useNavigate();

  return (
    <Box>
      <Typography variant="h3" gutterBottom>
        Welcome to Developer Portal
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Manage your projects and tasks efficiently
      </Typography>

      <Grid container spacing={3} sx={{ mt: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <Typography variant="h5" gutterBottom>
              Projects
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Create and manage your development projects
            </Typography>
            <Button variant="contained" onClick={() => navigate('/projects')}>
              View Projects
            </Button>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <Typography variant="h5" gutterBottom>
              Tasks
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              Track and organize your tasks
            </Typography>
            <Button variant="contained" onClick={() => navigate('/tasks')}>
              View Tasks
            </Button>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};
