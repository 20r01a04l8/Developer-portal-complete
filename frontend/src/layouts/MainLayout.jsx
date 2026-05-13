import { Box, Container } from '@mui/material';
import { Outlet } from 'react-router-dom';
import { Header, Footer } from '../components/layout';
import { Notification } from '../components/common';

export const MainLayout = () => {
  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      <Header />
      <Container component="main" sx={{ flex: 1, py: 4 }} maxWidth="lg">
        <Outlet />
      </Container>
      <Footer />
      <Notification />
    </Box>
  );
};
