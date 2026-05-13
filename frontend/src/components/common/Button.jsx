import { Button as MuiButton, CircularProgress } from '@mui/material';

export const Button = ({ children, loading, disabled, ...props }) => {
  return (
    <MuiButton disabled={disabled || loading} {...props}>
      {loading ? <CircularProgress size={24} /> : children}
    </MuiButton>
  );
};
