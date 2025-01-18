import React, { useState } from "react";
import { TextField, Button, Container, Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { login, getUserData } from "../authService"; // Import login and getUserData functions

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [message, setMessage] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Call login function from authService to log the user in
      const response = await login(email, password);

      // Show login success message
      setMessage(response.message);

      // Fetch user data to verify authentication
      const userData = await getUserData(); // This will make a request to the protected route

      // If user data is fetched successfully, navigate to home page
      if (userData) {
        navigate("/home"); // Redirect to the home page
      }
    } catch (error) {
      setMessage(error.message || "Login failed");
    }
  };

  const handleRegisterRedirect = () => {
    navigate("/register"); // Redirect to the register page
  };

  return (
    <Container maxWidth="xs">
      <Box
        sx={{
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          justifyContent: "center",
          height: "100vh",
        }}
      >
        <Typography variant="h4" gutterBottom>
          Login
        </Typography>
        <form onSubmit={handleSubmit} style={{ width: "100%" }}>
          <TextField
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            label="Email"
            variant="outlined"
            fullWidth
            margin="normal"
            required
          />
          <TextField
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            label="Password"
            variant="outlined"
            fullWidth
            margin="normal"
            required
          />
          <Button
            type="submit"
            variant="contained"
            color="primary"
            fullWidth
            style={{ marginTop: "1rem" }}
          >
            Login
          </Button>
        </form>

        {message && <Typography color="error" variant="body2">{message}</Typography>}

        <Button
          variant="outlined"
          color="secondary"
          fullWidth
          onClick={handleRegisterRedirect}
          style={{ marginTop: "1rem" }}
        >
          Register
        </Button>
      </Box>
    </Container>
  );
};

export default Login;
