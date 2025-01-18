import React, { useEffect, useState } from 'react';
import { Box, Button, Typography, List, ListItem, ListItemText, CircularProgress, Alert, Container, IconButton } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import axios from 'axios';
import TopMenu from './TopMenu';

const Notifications = () => {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchNotifications = async () => {
      try {
        const response = await axios.get('http://localhost:8000/notify/notifications/', { withCredentials: true });
        setNotifications(response.data);
      } catch (error) {
        setError('Failed to load notifications.');
      } finally {
        setLoading(false);
      }
    };

    fetchNotifications();
  }, []);

  // Handle the deletion of a notification
  const handleDelete = async (notificationId) => {
    try {
      const delId=parseInt(notificationId);
      await axios.delete(`http://localhost:8000/notify/notifications/${delId}/`, { withCredentials: true });
      setNotifications(prevNotifications => prevNotifications.filter(notification => notification.id !== delId));
    } catch (error) {
      setError('Failed to delete notification.');
    }
  };

  const handleSearchFlight = () => {
    window.location.href = '/home'; // Redirect to Home page
  };

  return (
    <>
      <TopMenu isNotificationsPage={true} />
      <Container maxWidth="md">
        <Box sx={{ padding: { xs: 2, sm: 4 }, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
          <Typography variant="h4" gutterBottom sx={{ fontSize: { xs: '1.8rem', sm: '2.4rem' } }}>
            My Notifications
          </Typography>

          {loading ? (
            <CircularProgress />
          ) : error ? (
            <Alert severity="error">{error}</Alert>
          ) : notifications.length === 0 ? (
            <Typography variant="h6" sx={{ mt: 2 }}>
              No subscriptions at the moment.
            </Typography>
          ) : (
            <List sx={{ width: '100%' }}>
              {notifications.map((notification, index) => (
                <ListItem key={index} sx={{ borderBottom: '1px solid #ddd', padding: '8px 0', display: 'flex', justifyContent: 'space-between' }}>
                  <ListItemText
                    primary={`${notification.origin} ➔ ${notification.destination}`}
                    secondary={`Departure Date: ${notification.departure_date} | Max Price: $${notification.max_price} | Frequency: every ${notification.frequency} ${notification.frequency_unit}`}
                  />
                  <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(notification.id)}>
                    <DeleteIcon />
                  </IconButton>
                </ListItem>
              ))}
            </List>
          )}
        </Box>
      </Container>
    </>
  );
};

export default Notifications;
