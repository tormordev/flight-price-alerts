import React from 'react';
import { Button, Grid, Typography } from '@mui/material';
import { useNavigate } from 'react-router-dom'; // Import useNavigate for navigation
import { logout } from '../authService';

const TopMenu = ({ isNotificationsPage }) => { // Add prop for differentiating pages
  const navigate = useNavigate(); // Use useNavigate for navigation

  const handleLogout = () => {
    // Implement your logout logic here
    logout();
    navigate('/login'); // Redirect to login page after logout
  };

  const handleNotifications = () => {
    navigate('/notifications'); // Navigate to notifications page
  };

  const handleHome = () => {
    navigate('/home'); // Navigate to home page
  };

  return (
    <Grid container alignItems="center" justifyContent="space-between" sx={{ width: '100%' }}>
      <Typography variant="h3" gutterBottom sx={{ fontSize: { xs: '1.8rem', sm: '2.4rem' } }}>
        TravelBuddy
      </Typography>
      <div>
        {isNotificationsPage ? (
          // On notifications page, show "Search Flight" button and logout
          <>
            <Button variant="contained" color="primary" onClick={handleHome} sx={{ marginRight: 2 }}>
              Search Flight
            </Button>
            <Button variant="contained" color="primary" onClick={handleLogout}>
              Logout
            </Button>
          </>
        ) : (
          // On home page, show "Notifications" and logout
          <>
            <Button variant="contained" color="primary" onClick={handleNotifications} sx={{ marginRight: 2 }}>
              Notifications
            </Button>
            <Button variant="contained" color="primary" onClick={handleLogout}>
              Logout
            </Button>
          </>
        )}
      </div>
    </Grid>
  );
};

export default TopMenu;
