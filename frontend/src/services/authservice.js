import axios from "axios";

const API_URL = "http://localhost:8081/auth";

export const loginUser = async (
    username,
    password
) => {

    const response = await axios.post(
        `${API_URL}/login`,
        {
            username,
            password
        }
    );

    return response.data;
};