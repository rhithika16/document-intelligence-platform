import axios from "axios";

const API = axios.create({
    baseURL: "http://127.0.0.1:8000"
});

export const uploadDocument = async (formData) => {
    return await API.post(
        "/documents/upload",
        formData,
        {
            headers: {
                "Content-Type": "multipart/form-data"
            }
        }
    );
};