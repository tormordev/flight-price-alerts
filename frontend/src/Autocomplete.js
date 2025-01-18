import React, { useState } from 'react';
import { Autocomplete, TextField, CircularProgress } from '@mui/material';
import axios from 'axios';

const AirportAutocomplete = ({ onSelect }) => {
  const [options, setOptions] = useState([]);
  const [loading, setLoading] = useState(false);

  // Handles input change and fetches autocomplete data
  const handleInputChange = async (event, value) => {
    if (value.length < 2) {
      setOptions([]);
      return;
    }

    setLoading(true);
    try {
      // Fetch airport data from API
      const response = await axios.get('http://localhost:8000/api/airport_autocomplete', {
        params: { term: value },
        withCredentials: true,
      });

      // Map API response to options format
      setOptions(
        response.data.map((item) => ({
          label: `${item.iataCode}, ${item.name} (${item.cityName})`,
          value: item.iataCode,
        }))
      );
    } catch (error) {
      console.error('Error fetching autocomplete data:', error);
    }
    setLoading(false);
  };

  return (
    <Autocomplete
      options={options}
      getOptionLabel={(option) => option.label || ''}
      onInputChange={(_, value) => handleInputChange(_, value)} // Handle user input
      onChange={(event, value) => {
        if (onSelect) {
          onSelect(value);
        } else {
          console.warn('onSelect function is not provided.');
        }
      }} // Pass selected value to parent or warn if not provided
      loading={loading}
      renderInput={(params) => (
        <TextField
          {...params}
          label="Search Airport/City"
          variant="outlined"
          fullWidth
          InputProps={{
            ...params.InputProps,
            endAdornment: (
              <>
                {loading ? <CircularProgress color="inherit" size={20} /> : null}
                {params.InputProps.endAdornment}
              </>
            ),
          }}
        />
      )}
    />
  );
};

export default AirportAutocomplete;
