// src/services/api.js


import axios from "axios";

const apiClient = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 30000, // 30s — generous enough for large file uploads
});

/**
 * Uploads a document to POST /documents/upload
 *
 * @param {File} file - the file selected by the user
 * @returns {Promise<object>} parsed JSON response from FastAPI
 *   (expected shape: { id, filename, file_size, status, ... })
 */
export async function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await apiClient.post("/documents/upload", formData, {
    headers: { "Content-Type": "multipart/form-data" },
  });

  return response.data;
}

export default apiClient;