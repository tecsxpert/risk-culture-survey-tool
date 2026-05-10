import { useEffect, useState } from "react";

import axios from "axios";
import {
    useSearchParams,

    Link
} from "react-router-dom";
import {
    BarChart,
    Bar,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer
} from "recharts";

const DashboardPage = () => {

    const [surveys, setSurveys] =
        useState([]);
    const [

    loading,

    setLoading

] = useState(true);
        const [searchText, setSearchText] =
    useState("");

const [debouncedSearch, setDebouncedSearch] =
    useState("");

const [statusFilter, setStatusFilter] =
    useState("");

const [startDate, setStartDate] =
    useState("");

const [endDate, setEndDate] =
    useState("");

const [searchParams, setSearchParams] =
    useSearchParams();

    useEffect(() => {

        fetchData();


    }, []);
    useEffect(() => {

    const timer = setTimeout(() => {

        setDebouncedSearch(
            searchText
        );

    }, 300);

    return () =>
        clearTimeout(timer);

}, [searchText]);
useEffect(() => {

    setSearchParams({

        search:
            searchText,

        status:
            statusFilter,

        startDate:
            startDate,

        endDate:
            endDate
    });

}, [

    searchText,

    statusFilter,

    startDate,

    endDate

]);
    const downloadCSV = () => {

    const headers = [

        "ID",

        "Title",

        "Employee",

        "Department",

        "Status"

    ];

    const rows = filteredSurveys.map(

        (survey) => [

            survey.id,

            survey.title,

            survey.employeeName,

            survey.department,

            survey.status
        ]
    );

    const csvContent = [

        headers,

        ...rows

    ]

        .map((row) =>
            row.join(",")
        )

        .join("\n");

    const blob = new Blob(

        [csvContent],

        {
            type:
                "text/csv"
        }
    );

    const url =
        window.URL.createObjectURL(
            blob
        );

    const link =
        document.createElement(
            "a"
        );

    link.href = url;

    link.download =
        "surveys.csv";

    link.click();
};
    const fetchData = async () => {

        try {
            setLoading(true);

            const response =
                await axios.get(
                    "http://localhost:8081/surveys"
                );

            setSurveys(
                response.data
            );
            setLoading(false);

        } catch (error) {
            setLoading(false);
            console.error(error);
        }
    };
    const filteredSurveys =

    surveys.filter((survey) => {

        const matchesSearch =

            survey.title
                ?.toLowerCase()
                .includes(

                    debouncedSearch
                        .toLowerCase()

                );

        const matchesStatus =

            statusFilter === ""

                ? true

                : survey.status ===
                  statusFilter;

        const surveyDate =
            survey.createdAt
                ?.split("T")[0];

        const matchesStartDate =

            startDate === ""

                ? true

                : surveyDate >=
                  startDate;

        const matchesEndDate =

            endDate === ""

                ? true

                : surveyDate <=
                  endDate;

        return (

            matchesSearch &&

            matchesStatus &&

            matchesStartDate &&

            matchesEndDate

        );
    });
    const totalSurveys =
    filteredSurveys.length;
    if (

    !loading &&

    totalSurveys === 0

) {

    return (

        <div
            style={{

                minHeight: "100vh",

                background:
                    "#0f172a",

                display: "flex",

                justifyContent:
                    "center",

                alignItems:
                    "center",

                color: "white",

                fontSize: "28px",

                fontWeight: "bold"
            }}
        >

            No dashboard data found

        </div>
    );
}
    const approvedCount =
        filteredSurveys.filter(
            (survey) =>
                survey.status ===
                "APPROVED"
        ).length;

    const pendingCount =
        filteredSurveys.filter(
            (survey) =>
                survey.status !==
                "APPROVED"
        ).length;

    const averageScore =
        filteredSurveys.length > 0

            ? (
                  filteredSurveys.reduce(
                      (sum, survey) =>
                          sum +
                          (survey.score || 0),
                      0
                  ) /
                  filteredSurveys.length
              ).toFixed(1)

            : 0;

    const statusData = [
        {
            name: "Approved",
            value: approvedCount
        },
        {
            name: "Pending",
            value: pendingCount
        }
    ];
    
    const categoryMap = {};

    filteredSurveys.forEach((survey) => {
        const category =
            survey.riskCategory ||
            "Unknown";

        categoryMap[category] =
            (categoryMap[
                category
            ] || 0) + 1;
    });

    const categoryData =
        Object.keys(categoryMap).map(
            (key) => ({
                name: key,
                value:
                    categoryMap[key]
            })
        );
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

            Loading dashboard...

        </div>
    );
}

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

        display: "flex",

        gap: "20px",

        padding: "20px",

        marginBottom: "20px"
    }}
>

    <Link
        to="/dashboard"

        style={{

            color: "white",

            textDecoration:
                "none",

            fontWeight: "bold"
        }}
    >
        Dashboard
    </Link>

    <Link
        to="/surveys"

        style={{

            color: "white",

            textDecoration:
                "none",

            fontWeight: "bold"
        }}
    >
        Surveys
    </Link>

    <Link
        to="/analytics"

        style={{

            color: "white",

            textDecoration:
                "none",

            fontWeight: "bold"
        }}
    >
        Analytics
    </Link>

</div>

            <div
                style={{
                    maxWidth: "1400px",

                    margin: "0 auto"
                }}
            >

                <h1
                    style={{
                        color: "white",

                        fontSize: "40px",

                        marginBottom:
                            "10px"
                    }}
                >
                    Risk Culture Analytics
                </h1>

                <p
                    style={{
                        color: "#cbd5e1",

                        marginBottom:
                            "35px"
                    }}
                >
                    Professional survey analytics dashboard
                </p>
                <div
    style={{
        display: "flex",

        gap: "15px",

        marginBottom: "30px",

        flexWrap: "wrap"
    }}
>

    <input
        type="text"

        placeholder="Search by title"

        value={searchText}

        onChange={(e) =>
            setSearchText(
                e.target.value
            )
        }

        style={{
            padding: "12px",

            borderRadius: "10px",

            border: "none",

            width: "250px"
        }}
    />

    <select

        value={statusFilter}

        onChange={(e) =>
            setStatusFilter(
                e.target.value
            )
        }

        style={{
            padding: "12px",

            borderRadius: "10px",

            border: "none"
        }}
    >

        <option value="">
            All Status
        </option>

        <option value="APPROVED">
            Approved
        </option>

        <option value="PENDING">
            Pending
        </option>

    </select>

    <input
        type="date"

        value={startDate}

        onChange={(e) =>
            setStartDate(
                e.target.value
            )
        }

        style={{
            padding: "12px",

            borderRadius: "10px",

            border: "none"
        }}
    />

    <input
        type="date"

        value={endDate}

        onChange={(e) =>
            setEndDate(
                e.target.value
            )
        }

        style={{
            padding: "12px",

            borderRadius: "10px",

            border: "none"
        }}
    />
    <button

    onClick={downloadCSV}

    style={{

        padding: "12px 20px",

        background: "#22c55e",

        color: "white",

        border: "none",

        borderRadius: "10px",

        cursor: "pointer",

        fontWeight: "bold"
    }}
>

    Download CSV

</button>

</div>

                <div
                    style={{
                        display: "grid",

                        gridTemplateColumns:
                            "repeat(auto-fit, minmax(250px, 1fr))",

                        gap: "20px",

                        marginBottom:
                            "40px"
                    }}
                >

                    <Card
                        title="Total Surveys"
                        value={totalSurveys}
                        color="#3b82f6"
                    />

                    <Card
                        title="Approved"
                        value={approvedCount}
                        color="#22c55e"
                    />

                    <Card
                        title="Pending"
                        value={pendingCount}
                        color="#ef4444"
                    />

                    <Card
                        title="Average Score"
                        value={averageScore}
                        color="#a855f7"
                    />

                </div>

                <div
                    style={{
                        display: "grid",

                        gridTemplateColumns:

    window.innerWidth < 768

        ? "1fr"

        : "1fr 1fr",
                        gap: "25px",
                        width: "100%"
                    }}
                >

                    <ChartCard
                        title="Survey Status"
                    >

                        <ResponsiveContainer
                            width="100%"
                            height={300}
                        >

                            <BarChart
                                data={statusData}
                            >

                                <CartesianGrid strokeDasharray="3 3" />

                                <XAxis dataKey="name" />

                                <YAxis />

                                <Tooltip />

                                <Bar
                                    dataKey="value"
                                    fill="#3b82f6"
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </ChartCard>

                    <ChartCard
                        title="Risk Categories"
                    >

                        <ResponsiveContainer
                            width="100%"
                            height={300}
                        >

                            <BarChart
                                data={categoryData}
                            >

                                <CartesianGrid strokeDasharray="3 3" />

                                <XAxis dataKey="name" />

                                <YAxis />

                                <Tooltip />

                                <Bar
                                    dataKey="value"
                                    fill="#8b5cf6"
                                />

                            </BarChart>

                        </ResponsiveContainer>

                    </ChartCard>

                </div>

            </div>

        </div>
    );
};

const Card = ({
    title,
    value,
    color
}) => {

    return (

        <div
            style={{
                background: "white",

                borderRadius: "20px",

                padding: "25px",

                boxShadow:
                    "0 8px 25px rgba(0,0,0,0.2)",

                borderTop:
                    `6px solid ${color}`
            }}
        >

            <h3
                style={{
                    color: "#64748b",

                    marginBottom:
                        "15px"
                }}
            >
                {title}
            </h3>

            <h1
                style={{
                    color: "#0f172a",

                    fontSize: "38px",

                    margin: 0
                }}
            >
                {value}
            </h1>

        </div>
    );
};

const ChartCard = ({
    title,
    children
}) => {

    return (

        <div
            style={{
                background: "white",

                borderRadius: "20px",

                padding: "25px",

                boxShadow:
                    "0 8px 25px rgba(0,0,0,0.2)"
            }}
        >

            <h2
                style={{
                    marginBottom:
                        "20px",

                    color: "#0f172a"
                }}
            >
                {title}
            </h2>

            {children}

        </div>
    );
};

export default DashboardPage;