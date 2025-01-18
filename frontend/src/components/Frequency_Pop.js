import React, { useState } from 'react';
import { Modal, Backdrop, Fade, Box, Typography, Grid, TextField, Select, MenuItem, Button } from '@mui/material';

const Frequency_Pop = ({ isOpen, onClose, onSubmit, notificationData, onNotificationDataChange, backdropOpacity = 0.5 }) => {

  const handleNotificationChange = (field, value) => {
    onNotificationDataChange(field, value);
  };

  const handleSubmit = () => {
    onSubmit(notificationData); // Pass data back to the parent component
    onClose(); // Close the modal
  };

  return (
    <Modal
      open={isOpen}
      onClose={onClose}
      closeAfterTransition
      BackdropComponent={Backdrop}
      BackdropProps={{ 
        timeout: 500, 
        sx: { bgcolor: `rgba(0, 0, 0, ${backdropOpacity})` }  // Dynamically adjust backdrop color opacity
      }}
    >
      <Fade in={isOpen}>
        <Box sx={{ 
          width: 400, 
          padding: 3, 
          bgcolor: 'white',  // Set modal content background to white
          borderRadius: 2, 
          boxShadow: 24, 
          position: 'absolute',  // Centering modal
          top: '50%', 
          left: '50%', 
          transform: 'translate(-50%, -50%)',  // Ensures the modal is perfectly centered
          zIndex: 1301  // Ensure the modal content appears above the backdrop
        }}>
          <Typography variant="h6" gutterBottom>
            Set Notification
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12}>
              <TextField
                label="Frequency"
                type="number"
                value={notificationData.frequency}
                onChange={(e) => handleNotificationChange('frequency', e.target.value)}
                fullWidth
              />
            </Grid>
            <Grid item xs={12}>
              <Select
                value={notificationData.frequency_unit}
                onChange={(e) => handleNotificationChange('frequency_unit', e.target.value)}
                fullWidth
              >
                <MenuItem value="minutes">Minutes</MenuItem>
                <MenuItem value="hours">Hours</MenuItem>
                <MenuItem value="days">Days</MenuItem>
                <MenuItem value="weeks">Weeks</MenuItem>
              </Select>
            </Grid>
            <Grid item xs={12}>
              <Button
                variant="contained"
                color="primary"
                fullWidth
                onClick={handleSubmit}
              >
                Create Notification
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Fade>
    </Modal>
  );
};

export default Frequency_Pop;
