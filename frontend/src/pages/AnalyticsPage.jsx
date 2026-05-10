
import {

    useEffect,

    useState

} from "react";

import axios from "axios";

import {

    PieChart,

    Pie,

    Cell,

    Tooltip,

    ResponsiveContainer,

    BarChart,
    LineChart,

    Line,

    Legend,

    Bar,

    XAxis,

    YAxis,

    CartesianGrid

} from "recharts";

const AnalyticsPage = () => {

    const [

        surveys,

        setSurveys

    ] = useState([]);
    const [

    loading,

    setLoading

] = useState(true);
    
    const [

    selectedPeriod,

    setSelectedPeriod

] = useState(6);
    const [

    liveReports,

    setLiveReports

] = useState([]);

    useEffect(() => {

        fetchData();

    }, []);
    useEffect(() => {

    const eventSource =

        new EventSource(

            "http://localhost:8081/stream"
        );

    eventSource.onmessage = (

        event

    ) => {

        setLiveReports(

            (prev) => [

                ...prev,

                event.data
            ]
        );
    };

    return () => {

        eventSource.close();
    };

}, []);

    const fetchData = async () => {

        try {
           
            
            const response =
                await axios.get(
                    "http://localhost:8081/surveys"
                );

            setSurveys(
                response.data
            );
            setLoading(false);
            
           

        } catch (error) {

            console.error(error);
            setLoading(false);
            
        }
    };

    const statusData = [

    {

        name: "Approved",

        value:

            surveys.filter(

                (survey) =>

                    survey.status
                        ?.trim()
                        .toUpperCase()

                    ===

                    "APPROVED"

            ).length
    },

    {

        name: "Pending",

        value:

            surveys.filter(

                (survey) =>

                    survey.status
                        ?.trim()
                        .toUpperCase()

                    ===

                    "PENDING"

            ).length
    }
];
    const categoryMap = {};

    surveys.forEach((survey) => {

        const category =

            survey.riskCategory ||

            "Unknown";

        categoryMap[category] =

            (

                categoryMap[
                    category
                ] || 0

            ) + 1;
    });

    const categoryData =

        Object.keys(categoryMap)

            .map((key) => ({

                name: key,

                value:
                    categoryMap[key]
            }));

    const COLORS = [

    "#1B4F8A",

    "#3B82F6",

    "#60A5FA",

    "#93C5FD"
];
    const monthlyData = [];

for (

    let i =

        selectedPeriod - 1;

    i >= 0;

    i--

) {

    const date =
        new Date();

    date.setMonth(

        date.getMonth() - i
    );

    const monthName =

        date.toLocaleString(

            "default",

            {
                month: "short"
            }
        );

    const year =
        date.getFullYear();

    const count =

        surveys.filter(

            (survey) => {

                const surveyDate =

                    new Date(
                        survey.createdAt
                    );

                return (

                    surveyDate.getMonth() ===

                        date.getMonth()

                    &&

                    surveyDate.getFullYear() ===
                    year
                );
            }

        ).length;

    monthlyData.push({

        month: monthName,

        surveys: count
    });
}
if (loading) {

    return (

        <div
            style={{
                minHeight: "100vh",

                background: "#0f172a",

                color: "white",

                display: "flex",

                justifyContent: "center",

                alignItems: "center"
            }}
        >

            <h1>
                Loading analytics...
            </h1>

        </div>
    );
}


   return (

    <div
        className="min-h-screen p-4 md:p-10 font-[Arial]"
        style={{
            backgroundColor: "#0f172a"
        }}
    >
           <h1
    style={{

        color: "#FFFFFF",

        marginBottom: "32px",

        fontSize: "32px",

        fontWeight: "bold"
    }}
>
    Analytics Dashboard
</h1>
            {

    surveys.length === 0 && (

        <div
            style={{

                background: "white",

                padding: "40px",

                borderRadius: "20px",

                textAlign: "center",

                marginBottom: "30px"
            }}
        >

            <h2>
                No Surveys Found
            </h2>

            <p>
                Please add surveys
                to view analytics.
            </p>

        </div>
    )
}
            <select

    value={selectedPeriod}

    onChange={(e) =>

        setSelectedPeriod(

            Number(
                e.target.value
            )
        )
    }

    style={{

    padding: "12px 16px",

    marginBottom: "24px",

    borderRadius: "8px",

    minHeight: "44px"
}}
>

    <option value={3}>
        Last 3 Months
    </option>

    <option value={6}>
        Last 6 Months
    </option>

    <option value={12}>
        Last 12 Months
    </option>

</select>
           <div
    style={{

        background: "white",

        padding: "24px",

        borderRadius: "20px",

        marginBottom: "24px"
    }}
>
    <h2
    style={{

        marginBottom: "16px",

        color: "#1B4F8A"
    }}
>
    Live Reports
</h2>
    {

        liveReports.map(

            (

                report,

                index

            ) => (

                <p key={index}>

                    {report}

                </p>
            )
        )
    }

</div>

            <div
    style={{
        display: "grid",

        gridTemplateColumns:

            window.innerWidth < 768

                ? "1fr"

                : "1fr 1fr",

        gap: "20px"
    }}
>

               <div
    style={{

        background: "white",

        borderRadius: "20px",

        padding: "20px",

        overflow: "hidden"
    }}
>

                   <h2
    style={{

        marginBottom: "16px",

        color: "#1B4F8A"
    }}
>
    Survey Status
</h2>
                    <ResponsiveContainer
                        width="100%"
                        height={300}
                    >

                        <PieChart>

                            <Pie

                                data={statusData}

                                dataKey="value"

                                nameKey="name"

                                outerRadius={100}

                                label={({ name, value }) =>

    `${name}: ${value}`
}
                            >

                                {

                                    statusData.map(

                                        (

                                            entry,

                                            index

                                        ) => (

                                            <Cell

                                                key={index}

                                                fill={

                                                    COLORS[
                                                        index %
                                                        COLORS.length
                                                    ]
                                                }
                                            />

                                        )
                                    )
                                }

                            </Pie>

                            <Tooltip />

                        </PieChart>

                    </ResponsiveContainer>

                </div>

                <div
    style={{

        background: "white",

        borderRadius: "20px",

        padding: "20px",

        overflow: "hidden"
    }}
>

                    <h2
    style={{

        marginBottom: "16px",

        color: "#1B4F8A"
    }}
>
    Risk Categories
</h2>

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

                                fill="#1B4F8A"
                            />

                        </BarChart>

                    </ResponsiveContainer>

                </div>
                <div
    style={{

        background: "white",

        borderRadius: "20px",

        padding: "20px",

        overflow: "hidden"
    }}
>
    <h2
    style={{

        marginBottom: "16px",

        color: "#1B4F8A"
    }}
>
    Survey Trend
</h2>

    <ResponsiveContainer
        width="100%"
        height={300}
    >

        <LineChart
            data={monthlyData}
        >

            <CartesianGrid
                strokeDasharray="3 3"
            />

            <XAxis
                dataKey="month"
            />

            <YAxis />

            <Tooltip />

            <Legend />

            <Line

                type="monotone"

                dataKey="surveys"

                stroke="#1B4F8A"

                strokeWidth={3}
            />

        </LineChart>

    </ResponsiveContainer>

</div>

            </div>

        </div>
    );
};

export default AnalyticsPage;

