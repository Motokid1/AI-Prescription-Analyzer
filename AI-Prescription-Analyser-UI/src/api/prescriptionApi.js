import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

export const analyzePrescription = async ({ file, text }) => {
  const formData = new FormData();

  if (file) {
    formData.append("file", file);
  }

  if (text && text.trim()) {
    formData.append("text", text.trim());
  }

  const response = await axios.post(`${API_BASE_URL}/analyze`, formData);

  return response.data;
};
