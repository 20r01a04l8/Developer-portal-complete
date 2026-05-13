import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import { Button } from '../common';

export const Header = () => {
  const navigate = useNavigate();

  return (
    <AppBar position="static">
      <Toolbar>
        <Typography
          variant="h6"
          component="div"
          sx={{ flexGrow: 1, cursor: 'pointer' }}
          onClick={() => navigate('/')}
        >
          Developer Portal
        </Typography>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button color="inherit" onClick={() => navigate('/projects')}>
            Projects
          </Button>
          <Button color="inherit" onClick={() => navigate('/tasks')}>
            Tasks
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};
