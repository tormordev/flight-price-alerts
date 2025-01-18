import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/", // URL of your FastAPI backend
  withCredentials: true, // Important to send cookies with every request
});

export default api;
