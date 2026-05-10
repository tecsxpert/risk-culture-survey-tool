import axios from "axios";

export const getSurveys = async (
    page = 0
) => {

    const response =
        await axios.get(
            `http://localhost:8081/surveys?page=${page}&size=5`
        );

    return response.data;
};