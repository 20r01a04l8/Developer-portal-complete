import { Snackbar, Alert } from '@mui/material';
import { useApp } from '../../contexts/AppContext';

export const Notification = () => {
  const { notification, hideNotification } = useApp();

  if (!notification) return null;

  return (
    <Snackbar
      open={!!notification}
      autoHideDuration={6000}
      onClose={hideNotification}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
    >
      <Alert onClose={hideNotification} severity={notification.severity} sx={{ width: '100%' }}>
        {notification.message}
      </Alert>
    </Snackbar>
  );
};
