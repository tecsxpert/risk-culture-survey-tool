console.log("NEW UI LOADED");

import { useEffect, useState } from "react";

import {
    useNavigate
} from "react-router-dom";

import {
    getSurveys
} from "../services/surveyService";

const SurveyListPage = () => {

    const navigate =
        useNavigate();

    const [surveys, setSurveys] =
        useState([]);
    const [

    loading,

    setLoading

] = useState(true);

    const [page, setPage] =
        useState(0);

    const [hasMore, setHasMore] =
        useState(true);

    const [sortField, setSortField] =
        useState("id");

    const [sortOrder, setSortOrder] =
        useState("asc");

    useEffect(() => {

        fetchSurveys();

    }, [page]);

    const fetchSurveys = async () => {

        try {
            setLoading(true);
            
            

            const data =
                await getSurveys(page);

            setSurveys(data);

            setHasMore(
                data.length >= 5
            );
            setLoading(false);

        } catch (error) {
            setLoading(false);

            console.error(
                "Error fetching surveys:",
                error
            );
        }
    };

    const handleNext = () => {

        if (
            hasMore
        ) {

            setPage(
                (prev) =>
                    prev + 1
            );
        }
    };

    const handlePrevious = () => {

        if (
            page > 0
        ) {

            setPage(
                (prev) =>
                    prev - 1
            );
        }
    };

    const handleSort = (
        field
    ) => {

        let order =
            "asc";

        if (

            sortField ===
                field &&

            sortOrder ===
                "asc"

        ) {

            order =
                "desc";
        }

        setSortField(
            field
        );

        setSortOrder(
            order
        );

        const sorted =
            [...surveys].sort(
                (
                    a,
                    b
                ) => {

                    const valueA =
                        a[
                            field
                        ] ?? "";

                    const valueB =
                        b[
                            field
                        ] ?? "";

                    if (

                        typeof valueA ===
                            "number" &&

                        typeof valueB ===
                            "number"

                    ) {

                        return order ===
                            "asc"

                            ? valueA -
                                  valueB

                            : valueB -
                                  valueA;
                    }

                    return order ===
                        "asc"

                        ? valueA
                              .toString()
                              .localeCompare(
                                  valueB.toString()
                              )

                        : valueB
                              .toString()
                              .localeCompare(
                                  valueA.toString()
                              );
                }
            );

        setSurveys(
            sorted
        );
    };
    if (loading) {

    return (

        <div
            style={{

                minHeight: "100vh",

                display: "flex",

                justifyContent: "center",

                alignItems: "center",

                background:
                    "#0f172a",

                color: "white",

                fontSize: "28px",

                fontWeight: "bold"
            }}
        >

            Loading surveys...

        </div>
    );
}

    return (

        <div
            style={{
                minHeight:
                    "100vh",

                background:
                    "linear-gradient(to right, #0f172a, #1e293b)",

                padding:
                    "40px",

                fontFamily:
                    "'Segoe UI', sans-serif"
            }}
        >

            <div
                style={{
                    maxWidth:
                        "1300px",

                    margin:
                        "0 auto",

                    background:
                        "#ffffff",

                    borderRadius:
                        "20px",

                    padding:
                        "35px",

                    boxShadow:
                        "0 10px 40px rgba(0,0,0,0.25)"
                }}
            >

                <div
                    style={{
                        display:
                            "flex",

                        justifyContent:
                            "space-between",

                        alignItems:
                            "center",

                        marginBottom:
                            "30px"
                    }}
                >

                    <div>

                        <h1
                            style={{
                                fontSize:
                                    "38px",

                                color:
                                    "#0f172a",

                                marginBottom:
                                    "10px"
                            }}
                        >
                            Risk Culture Dashboard
                        </h1>

                        <p
                            style={{
                                color:
                                    "#64748b"
                            }}
                        >
                            Manage and monitor employee risk surveys
                        </p>

                    </div>

                    <div
                        style={{
                            background:
                                "#eff6ff",

                            padding:
                                "18px 24px",

                            borderRadius:
                                "14px",

                            textAlign:
                                "center"
                        }}
                    >

                        <h2
                            style={{
                                margin: 0,

                                color:
                                    "#2563eb",

                                fontSize:
                                    "30px"
                            }}
                        >
                            {
                                surveys.length
                            }
                        </h2>

                        <p
                            style={{
                                margin: 0,

                                color:
                                    "#475569"
                            }}
                        >
                            Surveys
                        </p>

                    </div>

                </div>

                <div
                    style={{
                        overflowX:
                            "auto"
                    }}
                >

                    <table
                        style={{
                            width:
                                "100%",

                            borderCollapse:
                                "collapse"
                        }}
                    >

                        <thead>

                            <tr
                                style={{
                                    background:
                                        "#2563eb",

                                    color:
                                        "white"
                                }}
                            >

                                {[
                                    "id",
                                    "title",
                                    "employeeName",
                                    "department",
                                    "riskCategory",
                                    "score",
                                    "status"
                                ].map(
                                    (
                                        field
                                    ) => (

                                        <th
                                            key={
                                                field
                                            }

                                            onClick={() =>
                                                handleSort(
                                                    field
                                                )
                                            }

                                            style={{
                                                padding:
                                                    "18px",

                                                cursor:
                                                    "pointer",

                                                textAlign:
                                                    "left"
                                            }}
                                        >

                                            {

                                                field ===
                                                "employeeName"

                                                    ? "Employee"

                                                    : field

                                            }

                                        </th>

                                    )
                                )}

                                <th
                                    style={{
                                        padding:
                                            "18px",

                                        textAlign:
                                            "left"
                                    }}
                                >
                                    Actions
                                </th>

                            </tr>

                        </thead>

                        <tbody>

                            {

    surveys.length === 0

        ? (

            <tr>

                <td
                    colSpan="8"

                    style={{

                        textAlign:
                            "center",

                        padding:
                            "40px",

                        color:
                            "#64748b",

                        fontSize:
                            "20px",

                        fontWeight:
                            "bold"
                    }}
                >

                    No surveys found

                </td>

            </tr>

        )

        : (

            surveys.map(

                (
                    survey,
                    index
                ) => (

                    <tr
                        key={
                            survey.id
                        }

                        style={{
                            background:
                                index %
                                    2 ===
                                0

                                    ? "#f8fafc"

                                    : "#ffffff"
                        }}
                    >

                        <td style={tdStyle}>
                            {survey.id}
                        </td>

                        <td style={tdStyle}>
                            {survey.title}
                        </td>

                        <td style={tdStyle}>
                            {survey.employeeName}
                        </td>

                        <td style={tdStyle}>
                            {survey.department}
                        </td>

                        <td style={tdStyle}>
                            {survey.riskCategory}
                        </td>

                        <td
                            style={{
                                ...tdStyle,

                                fontWeight:
                                    "bold",

                                color:
                                    "#2563eb"
                            }}
                        >
                            {

                                survey.score ??

                                survey.riskScore ??

                                "N/A"

                            }
                        </td>

                        <td style={tdStyle}>

                            <span
                                style={{
                                    background:

                                        survey.status ===
                                        "APPROVED"

                                            ? "#dcfce7"

                                            : "#fee2e2",

                                    color:

                                        survey.status ===
                                        "APPROVED"

                                            ? "#166534"

                                            : "#991b1b",

                                    padding:
                                        "8px 16px",

                                    borderRadius:
                                        "30px",

                                    fontSize:
                                        "12px",

                                    fontWeight:
                                        "bold"
                                }}
                            >

                                {
                                    survey.status
                                }

                            </span>

                        </td>

                        <td style={tdStyle}>

                            <button

                                onClick={() =>
                                    navigate(
                                        `/survey/${survey.id}`
                                    )
                                }

                                style={{
                                    padding:
                                        "10px 18px",

                                    background:
                                        "#3b82f6",

                                    color:
                                        "white",

                                    border:
                                        "none",

                                    borderRadius:
                                        "10px",

                                    cursor:
                                        "pointer",

                                    fontWeight:
                                        "bold"
                                }}
                            >
                                View
                            </button>

                        </td>

                    </tr>
                )
            )
        )
}
                        </tbody>

                    </table>

                </div>

                <div
                    style={{
                        display:
                            "flex",

                        justifyContent:
                            "space-between",

                        alignItems:
                            "center",

                        marginTop:
                            "30px"
                    }}
                >

                    <button
                        onClick={
                            handlePrevious
                        }

                        disabled={
                            page === 0
                        }

                        style={
                            buttonStyle(
                                page === 0
                            )
                        }
                    >
                        Previous
                    </button>

                    <div
                        style={{
                            fontWeight:
                                "bold",

                            color:
                                "#0f172a"
                        }}
                    >
                        Page {
                            page + 1
                        }
                    </div>

                    <button
                        onClick={
                            handleNext
                        }

                        disabled={
                            !hasMore
                        }

                        style={
                            buttonStyle(
                                !hasMore
                            )
                        }
                    >
                        Next
                    </button>

                </div>

            </div>

        </div>
    );
};

const tdStyle = {

    padding:
        "18px"
};

const buttonStyle = (
    disabled
) => ({

    padding:
        "12px 24px",

    background:
        "#2563eb",

    color:
        "white",

    border:
        "none",

    borderRadius:
        "10px",

    cursor:
        "pointer",

    opacity:
        disabled
            ? 0.5
            : 1,

    fontWeight:
        "bold"
});

export default SurveyListPage;