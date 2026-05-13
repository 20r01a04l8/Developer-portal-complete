import { Card as MuiCard, CardContent, CardActions } from '@mui/material';

export const Card = ({ children, actions, sx, ...props }) => {
  return (
    <MuiCard sx={{ ...sx }} {...props}>
      <CardContent>{children}</CardContent>
      {actions && <CardActions>{actions}</CardActions>}
    </MuiCard>
  );
};
