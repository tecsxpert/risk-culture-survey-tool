import { useEffect, useState } from "react";

import axios from "axios";

import {
  useParams,
  useNavigate
} from "react-router-dom";

const EditSurveyPage = () => {

  const { id } = useParams();

  const navigate = useNavigate();

  const [survey, setSurvey] = useState({
    title: "",
    employeeName: "",
    department: "",
    riskCategory: "",
    status: ""
  });

  useEffect(() => {
    fetchSurvey();
  }, []);

  const fetchSurvey = async () => {

    try {

      const response =
        await axios.get(
          `http://localhost:8081/surveys/${id}`
        );

      setSurvey(response.data);

    } catch (error) {

      console.error(error);
    }
  };

  const handleChange = (e) => {

    setSurvey({
      ...survey,
      [e.target.name]:
        e.target.value
    });
  };

  const handleUpdate = async (e) => {

    e.preventDefault();

    try {

      await axios.put(
        `http://localhost:8081/surveys/${id}`,
        survey
      );

      alert("Survey Updated");

      navigate(`/survey/${id}`);

    } catch (error) {

      console.error(error);

      alert("Update failed");
    }
  };

  return (

    <div
      style={{
        minHeight: "100vh",
        background: "#0f172a",
        padding: "40px"
      }}
    >

      <div
        style={{
          maxWidth: "700px",
          margin: "0 auto",
          background: "white",
          padding: "40px",
          borderRadius: "20px"
        }}
      >

        <h1>Edit Survey</h1>

        <form onSubmit={handleUpdate}>

          <input
            type="text"
            name="title"
            value={survey.title}
            onChange={handleChange}
            placeholder="Title"
            style={inputStyle}
          />

          <input
            type="text"
            name="employeeName"
            value={survey.employeeName}
            onChange={handleChange}
            placeholder="Employee Name"
            style={inputStyle}
          />

          <input
            type="text"
            name="department"
            value={survey.department}
            onChange={handleChange}
            placeholder="Department"
            style={inputStyle}
          />

          <input
            type="text"
            name="riskCategory"
            value={survey.riskCategory}
            onChange={handleChange}
            placeholder="Risk Category"
            style={inputStyle}
          />

          <input
            type="text"
            name="status"
            value={survey.status}
            onChange={handleChange}
            placeholder="Status"
            style={inputStyle}
          />

          <button
            type="submit"
            style={{
              width: "100%",
              padding: "14px",
              background: "#2563eb",
              color: "white",
              border: "none",
              borderRadius: "10px"
            }}
          >
            Update Survey
          </button>

        </form>

      </div>

    </div>
  );
};

const inputStyle = {

  width: "100%",
  padding: "14px",
  marginBottom: "20px",
  border: "1px solid #cbd5e1",
  borderRadius: "10px"
};

export default EditSurveyPage;