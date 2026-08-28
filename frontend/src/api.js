import axios from "axios";

// Set VITE_API_BASE_URL in a .env file when the backend is deployed elsewhere.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function screenResume(resumeFile, jobDescription) {
  const formData = new FormData();
  formData.append("resume", resumeFile);
  formData.append("job_description", jobDescription);

  const response = await axios.post(`${API_BASE_URL}/api/screen`, formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });
  return response.data;
}

export async function fetchScreeningHistory() {
  const response = await axios.get(`${API_BASE_URL}/api/history`);
  return response.data;
}
