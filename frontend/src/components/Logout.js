import React from 'react';
import { logout } from '../authService'; // Import logout function from authService

const Logout = () => {
  const handleLogout = async () => {
    try {
      await logout();  // Use logout function from authService
      window.location.href = '/login'; // Redirect to login after logout
    } catch (error) {
      console.error('Logout failed');
    }
  };

  return (
    <div>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Logout;
