import React, { useState, useEffect } from 'react'; 
import { Button, Container, Box, Typography, TextField, Alert, Switch, FormControlLabel, Grid, MenuItem, Select } from '@mui/material';
import Autocomplete from '../Autocomplete'; 
import { logout } from '../authService';
import axios from 'axios';
import { useNavigate } from 'react-router-dom'; // To handle navigation
import Frequency_Pop from './Frequency_Pop'; 

const TopMenu = ({ onLogout }) => {
  const navigate = useNavigate();

  const handleNotificationsClick = () => {
    navigate('/notifications');
  };

  return (
    <Grid container alignItems="center" justifyContent="space-between" sx={{ width: '100%' }}>
      <Typography variant="h3" gutterBottom sx={{ fontSize: { xs: '1.8rem', sm: '2.4rem' } }}>
        TravelBuddy
      </Typography>
      <div>
        <Button
          variant="contained"
          color="primary"
          onClick={handleNotificationsClick}
          sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}
        >
          Notifications
        </Button>
        <Button
          variant="contained"
          color="secondary"
          onClick={onLogout}
          sx={{ fontSize: { xs: '0.8rem', sm: '1rem' } }}
        >
          Logout
        </Button>
      </div>
    </Grid>
  );
};

const Home = () => {
  const [locations, setLocations] = useState([]);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [departure, setDeparture] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [isOneWay, setIsOneWay] = useState(false);
  const [duration, setDuration] = useState('');
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);
  const [sortOption, setSortOption] = useState('price');
  const [notificationData, setNotificationData] = useState({
    origin: '',
    destination: '',
    departure_date: '',
    max_price: 0,
    frequency: 0,
    frequency_unit: '',
  });

  const [showNotificationSettings, setShowNotificationSettings] = useState(false); // State to toggle notification settings visibility
  const [selectedFlight, setSelectedFlight] = useState(null); // To hold the selected flight data
  const [showOfferMessage, setShowOfferMessage] = useState(false); // State to handle "View Offer" messages

  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      await logout();
      navigate('/login');
    } catch (error) {
      console.error('Logout failed:', error);
    }
  };

  const handleSearch = async (event) => {
    event.preventDefault();
    setPage(1);
    setLocations([]);
    setLoading(true);
    setError('');
    try {
      const parsedMaxPrice = parseInt(maxPrice, 10);
      const requestPayload = {
        origin: departure,
        departureDate: isOneWay ? startDate : `${startDate},${endDate}`,
        oneWay: isOneWay,
        maxPrice: parsedMaxPrice,
        viewBy: isOneWay ? 'DATE' : 'DURATION',
      };
      if (!isOneWay && duration) {
        requestPayload.duration = duration;
      }
      const response = await axios.post('http://localhost:8000/api/flight_destinations', requestPayload, { withCredentials: true });
      setLocations(response.data.data);
      setHasMore(response.data.data.length > 0);
      setLoading(false);
    } catch (err) {
      setError('Failed to fetch flight destinations.');
      setLoading(false);
      console.error(err);
    }
  };

  const loadMoreResults = async () => {
    setLoading(true);
    try {
      const parsedMaxPrice = parseInt(maxPrice, 10);
      const requestPayload = {
        origin: departure,
        departureDate: isOneWay ? startDate : `${startDate},${endDate}`,
        oneWay: isOneWay,
        maxPrice: parsedMaxPrice,
        viewBy: isOneWay ? 'DATE' : 'DURATION',
      };
      if (!isOneWay && duration) {
        requestPayload.duration = duration;
      }
      const response = await axios.post('http://localhost:8000/api/flight_destinations', requestPayload, { withCredentials: true });
      setLocations((prevLocations) => [...prevLocations, ...response.data.data]);
      setPage((prevPage) => prevPage + 1);
      setHasMore(response.data.data.length > 0);
      setLoading(false);
    } catch (err) {
      setError('Failed to load more results.');
      setLoading(false);
      console.error(err);
    }
  };

  const handleShowOffer = () => {
    setShowOfferMessage(true);
    setTimeout(() => setShowOfferMessage(false), 5000);
  };

  const handleNotificationChange = (field, value) => {
    setNotificationData({
      ...notificationData,
      [field]: value,
    });
  };

  const handleCreateNotification = async (data) => {
    const notificationPayload = {
      origin: data.origin,
      destination: data.destination,
      departure_date: data.departure_date,
      max_price: data.max_price,
      frequency: data.frequency,
      frequency_unit: data.frequency_unit,
    };
    try {
      await axios.post('http://localhost:8000/notify/notify/notifications/', notificationPayload, { withCredentials: true });
      alert('Notification created successfully');
      setShowNotificationSettings(false);
    } catch (error) {
      console.error('Error creating notification:', error);
    }
  };

  const handleShowNotificationSettings = (flight) => {
    setSelectedFlight(flight);
    setNotificationData({
      ...notificationData,
      origin: flight.origin,
      destination: flight.destination,
      departure_date: flight.departureDate,
      max_price: flight.price.total,
    });
    setShowNotificationSettings(true);
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', height: '100vh', position: 'relative', padding: { xs: 2, sm: 4 } }}>
        <TopMenu onLogout={handleLogout} />
        <Box sx={{ width: '100%', marginBottom: '16px' }}>
          <Typography variant="h6">Search for Flights</Typography>
          <form onSubmit={handleSearch}>
            <Autocomplete
              label="Departure City"
              value={departure}
              onSelect={(newValue) => setDeparture(newValue?.value || '')}
              placeholder="Enter departure city"
            />
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, gap: 2, mb: 3 }}>
              <TextField
                label="Start Range Date"
                variant="outlined"
                type="date"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
                required
                fullWidth
                InputLabelProps={{ shrink: true }}
              />
              {!isOneWay && (
                <TextField
                  label="End Range Date"
                  variant="outlined"
                  type="date"
                  value={endDate}
                  onChange={(e) => setEndDate(e.target.value)}
                  required
                  fullWidth
                  InputLabelProps={{ shrink: true }}
                />
              )}
            </Box>
            <TextField
              label="Max Price EUR"
              variant="outlined"
              value={maxPrice}
              onChange={(e) => setMaxPrice(e.target.value)}
              required
              fullWidth
              sx={{ mb: 3 }}
            />
            <FormControlLabel
              control={<Switch checked={isOneWay} onChange={() => setIsOneWay(!isOneWay)} />}
              label="One Way"
              sx={{ mb: 2 }}
            />
            {!isOneWay && (
              <TextField
                label="Duration (Days) (Optional)"
                variant="outlined"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                fullWidth
                sx={{ mb: 2 }}
                type="number"
                inputProps={{ min: 1, max: 15 }}
              />
            )}
            <Button type="submit" variant="contained" color="secondary" fullWidth>
              Search Flights
            </Button>
          </form>
        </Box>

        {locations.length > 0 && (
          <Box sx={{ mt: 3, maxHeight: '600px', overflowY: 'scroll', width: '100%' }}>
            <Typography variant="h6">Flight Destinations:</Typography>
            {locations.map((flight, index) => (
              <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #ddd', padding: '8px 0', gap: 2 }}>
                <Box>
                  <Typography variant="body1">
                    {flight.origin} ➔ {flight.destination}
                  </Typography>
                  <Typography variant="body2" color="textSecondary">
                    Date: {flight.departureDate} - Price: ${flight.price.total}
                  </Typography>
                </Box>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    size="small"
                    color="primary"
                    onClick={() => handleShowNotificationSettings(flight)}
                  >
                    Create Notification
                  </Button>
                  <Button
                    variant="text"
                    size="small"
                    color="secondary"
                    onClick={handleShowOffer}
                    sx={{ fontSize: '0.8rem', textDecoration: 'underline' }}
                  >
                    View Offer
                  </Button>
                </Box>
              </Box>
            ))}
            {hasMore && (
              <Button variant="outlined" color="primary" onClick={loadMoreResults} fullWidth>
                Load More
              </Button>
            )}
          </Box>
        )}

        {showOfferMessage && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Amadeus está en un ambiente de pruebas. Para comprar el vuelo, necesitas pagar el servicio.
          </Alert>
        )}

        <Frequency_Pop
          isOpen={showNotificationSettings}
          onClose={() => setShowNotificationSettings(false)}
          onSubmit={handleCreateNotification}
          notificationData={notificationData}
          onNotificationDataChange={handleNotificationChange}
        />

        {loading && <Typography variant="body1">Loading...</Typography>}
        {error && <Alert severity="error">{error}</Alert>}
      </Box>
    </Container>
  );
};

export default Home;
