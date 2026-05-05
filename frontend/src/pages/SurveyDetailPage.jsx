import { useEffect, useState } from "react";

import axios from "axios";

import {
    useParams,
    useNavigate
} from "react-router-dom";

const SurveyDetailPage = () => {

    const { id } = useParams();

    const navigate =
        useNavigate();

    const [survey, setSurvey] =
        useState(null);
    const [aiResponse, setAiResponse] =
        useState("");

    const [loadingAi, setLoadingAi] =
        useState(false);

    const [aiError, setAiError] =
        useState(false);
    

    useEffect(() => {

        fetchSurvey();

    }, []);

    const fetchSurvey = async () => {

        try {

            const response =
                await axios.get(
                    `http://localhost:8081/surveys/${id}`
                );

            setSurvey(
                response.data
            );

        } catch (error) {

            console.error(error);
        }
    };
    const handleAskAi = async () => {

    setLoadingAi(true);

    setAiError(false);

    try {

        await new Promise(
            resolve =>
                setTimeout(
                    resolve,
                    2000
                )
        );

        const responseText =

            score >= 80

                ? "AI Analysis: Employee demonstrates excellent awareness of organizational risks and follows strong compliance practices."

                : score >= 50

                ? "AI Analysis: Employee has moderate understanding of risk culture but needs additional awareness training."

                : "AI Analysis: Employee shows poor risk awareness and requires immediate risk management guidance.";

        setAiResponse(
            responseText
        );

    } catch (error) {

        setAiError(true);

    } finally {

        setLoadingAi(false);
    }
};
    
    const handleDelete = async () => {

        const confirmDelete =
            window.confirm(
                "Delete this survey?"
            );

        if (!confirmDelete) return;

        try {

            await axios.delete(
                `http://localhost:8081/surveys/${id}`
            );

            alert(
                "Survey deleted successfully"
            );

            navigate(
                "/dashboard"
            );

        } catch (error) {

            console.error(error);

            alert(
                "Delete failed"
            );
        }
    };

    if (!survey) {

        return (

            <h1
                style={{
                    color: "white",
                    padding: "40px"
                }}
            >
                Loading...
            </h1>
        );
    }

    const score =
    survey.score ||
    survey.riskScore ||
    0;

const scoreColor =

    score >= 80

        ? "#22c55e"

        : score >= 50

        ? "#f59e0b"

        : "#ef4444";

    return (

        <div
            style={{
                minHeight: "100vh",

                background:
                    "#0f172a",

                padding: "40px",

                fontFamily:
                    "Segoe UI"
            }}
        >

            <div
                style={{
                    maxWidth: "1200px",

                    margin: "0 auto"
                }}
            >

                <h1
                    style={{
                        color: "white",

                        marginBottom:
                            "30px",

                        fontSize: "40px"
                    }}
                >
                    Survey Details
                </h1>

                <div
                    style={{
                        background:
                            "white",

                        borderRadius:
                            "20px",

                        padding: "35px",

                        marginBottom:
                            "30px",

                        boxShadow:
                            "0 10px 30px rgba(0,0,0,0.3)"
                    }}
                >

                    <div
                        style={{
                            display: "grid",

                            gridTemplateColumns:
                                "1fr 1fr",

                            gap: "25px"
                        }}
                    >

                        <DetailItem
                            label="ID"
                            value={survey.id}
                        />

                        <DetailItem
                            label="Title"
                            value={survey.title}
                        />

                        <DetailItem
                            label="Employee"
                            value={
                                survey.employeeName
                            }
                        />

                        <DetailItem
                            label="Department"
                            value={
                                survey.department
                            }
                        />

                        <DetailItem
                            label="Risk Category"
                            value={
                                survey.riskCategory
                            }
                        />

                        <div>

                            <p
                                style={{
                                    color:
                                        "#64748b",

                                    marginBottom:
                                        "8px"
                                }}
                            >
                                Score
                            </p>
                             <div
    style={{
        background:
            scoreColor,

        color:
            "white",

        width: "70px",

        height: "70px",

        borderRadius:
            "50%",

        display: "flex",

        justifyContent:
            "center",

        alignItems:
            "center",

        fontWeight:
            "bold",

        fontSize: "22px"
    }}
>
    {score}
</div>
                            
                              
                        </div>

                        <div>

                            <p
                                style={{
                                    color:
                                        "#64748b",

                                    marginBottom:
                                        "8px"
                                }}
                            >
                                Status
                            </p>

                            <span
                                style={{
                                    background:
                                        survey.status ===
                                        "APPROVED"

                                            ? "#22c55e"

                                            : "#ef4444",

                                    color:
                                        "white",

                                    padding:
                                        "10px 18px",

                                    borderRadius:
                                        "30px",

                                    fontWeight:
                                        "bold"
                                }}
                            >
                                {
                                    survey.status
                                }
                            </span>

                        </div>

                    </div>

                </div>

                <div
                    style={{
                        background:
                            "white",

                        borderRadius:
                            "20px",

                        padding: "30px",

                        marginBottom:
                            "30px",

                        boxShadow:
                            "0 10px 30px rgba(0,0,0,0.3)"
                    }}
                >

                    <h2
                        style={{
                            marginBottom:
                                "20px"
                        }}
                    >
                        AI Risk Analysis
                    </h2>

                    <p
                        style={{
                            color: "#475569",

                            lineHeight: "1.8"
                        }}
                    >

                        Based on survey responses,
                        this employee shows

                        {

                            score >= 80

                                ? " strong risk awareness and compliance understanding."

                                : score >= 50

                                ? " moderate awareness but may require additional training."

                                : " low awareness and may require immediate risk management training."

                        }

                    </p>

                </div>
                {

    loadingAi && (

        <div
            style={{
                background: "white",

                padding: "20px",

                borderRadius: "20px",

                marginBottom: "20px"
            }}
        >

            <h3>
                AI is analyzing...
            </h3>

        </div>
    )
}

{

    aiResponse && (

        <div
            style={{
                background: "#1e293b",

                color: "white",

                padding: "25px",

                borderRadius: "20px",

                marginBottom: "20px"
            }}
        >

            <h2>
                AI Response
            </h2>

            <p
                style={{
                    lineHeight: "1.8"
                }}
            >
                {aiResponse}
            </p>

        </div>
    )
}

{

    aiError && (

        <div>

            <p
                style={{
                    color: "red"
                }}
            >
                AI request failed
            </p>

            <button
                onClick={handleAskAi}
            >
                Retry
            </button>

        </div>
    )
}
                

                <div
                    style={{
                        display: "flex",

                        gap: "20px"
                    }}
                >

                    <button
    onClick={handleAskAi}

    style={{
        padding: "14px 28px",

        background: "#8b5cf6",

        color: "white",

        border: "none",

        borderRadius: "12px",

        cursor: "pointer",

        fontWeight: "bold"
    }}
>

    Ask AI

</button>

<button
    onClick={() =>
        navigate(
            `/edit/${id}`
        )
    }

    style={{
        padding:
            "14px 28px",

        background:
            "#3b82f6",

        color:
            "white",

        border:
            "none",

        borderRadius:
            "12px",

        cursor:
            "pointer",

        fontWeight:
            "bold"
    }}
>
    Edit
</button>
                    <button
                        onClick={
                            handleDelete
                        }

                        style={{
                            padding:
                                "14px 28px",

                            background:
                                "#ef4444",

                            color:
                                "white",

                            border:
                                "none",

                            borderRadius:
                                "12px",

                            cursor:
                                "pointer",

                            fontWeight:
                                "bold"
                        }}
                    >
                        Delete
                    </button>

                </div>

            </div>

        </div>
    );
};

const DetailItem = ({
    label,
    value
}) => (

    <div>

        <p
            style={{
                color: "#64748b",

                marginBottom: "8px"
            }}
        >
            {label}
        </p>

        <h3
            style={{
                color: "#0f172a"
            }}
        >
            {value}
        </h3>

    </div>
);

export default SurveyDetailPage;