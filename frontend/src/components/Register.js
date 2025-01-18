import React from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { Formik, Field, Form, ErrorMessage } from "formik";
import * as Yup from "yup";
import { useNavigate } from "react-router-dom";
import api from "../api"; // Use the configured axios instance

const validationSchema = Yup.object({
  email: Yup.string().email("Invalid email address").required("Required"),
  password: Yup.string()
    .min(8, "Password must be at least 8 characters")
    .required("Required"),
  confirmPassword: Yup.string()
    .oneOf([Yup.ref("password"), null], "Passwords must match")
    .required("Required"),
});

const Register = () => {
  const navigate = useNavigate();

  const handleSubmit = async (values, { setSubmitting, setErrors }) => {
    try {
      const response = await api.post("/auth/register", {
        email: values.email,
        password: values.password,
      });
      console.log(response.data.message); // Log success message
      navigate("/login"); // Redirect to login page
    } catch (error) {
      if (error.response && error.response.data.detail) {
        setErrors({ email: error.response.data.detail }); // Handle validation errors
      } else {
        console.error("An unexpected error occurred:", error);
      }
    } finally {
      setSubmitting(false);
    }
  };

  const handleLoginRedirect = () => {
    navigate("/login"); // Redirect to the login page
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
          Register
        </Typography>
        <Formik
          initialValues={{ email: "", password: "", confirmPassword: "" }}
          validationSchema={validationSchema}
          onSubmit={handleSubmit}
        >
          {({ isSubmitting }) => (
            <Form style={{ width: "100%" }}>
              <Field
                name="email"
                as={TextField}
                label="Email"
                variant="outlined"
                fullWidth
                margin="normal"
              />
              <ErrorMessage name="email" component="div" style={{ color: "red" }} />
              <Field
                name="password"
                type="password"
                as={TextField}
                label="Password"
                variant="outlined"
                fullWidth
                margin="normal"
              />
              <ErrorMessage name="password" component="div" style={{ color: "red" }} />
              <Field
                name="confirmPassword"
                type="password"
                as={TextField}
                label="Confirm Password"
                variant="outlined"
                fullWidth
                margin="normal"
              />
              <ErrorMessage name="confirmPassword" component="div" style={{ color: "red" }} />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
                disabled={isSubmitting}
                style={{ marginTop: "1rem" }}
              >
                {isSubmitting ? "Registering..." : "Register"}
              </Button>
            </Form>
          )}
        </Formik>

        <Button
          variant="outlined"
          color="secondary"
          fullWidth
          onClick={handleLoginRedirect}
          style={{ marginTop: "1rem" }}
        >
          Go to Login
        </Button>
      </Box>
    </Container>
  );
};

export default Register;
