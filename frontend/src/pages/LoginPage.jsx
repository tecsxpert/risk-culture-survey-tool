import { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";

const LoginPage = () => {

    const navigate = useNavigate();

    const [username, setUsername] =
        useState("");

    const [password, setPassword] =
        useState("");

    const [error, setError] =
        useState("");

    const handleLogin = async (
        e
    ) => {

        e.preventDefault();

        setError("");

        try {

            const response =
                await axios.post(
                    "http://localhost:8081/auth/login",
                    {
                        username,
                        password
                    }
                );

            const token =
                response.data;

            if (
                token ===
                    "Invalid password" ||

                token ===
                    "User not found"
            ) {

                setError(token);

                return;
            }

            localStorage.setItem(
                "token",
                token
            );

            navigate(
                "/dashboard"
            );

        } catch {

            setError(
                "Login failed"
            );
        }
    };

    return (

        <div
            style={{
                height: "100vh",

                display: "flex",

                justifyContent:
                    "center",

                alignItems:
                    "center",

                background:
                    "linear-gradient(135deg,#0f172a,#1e3a8a)",

                fontFamily:
                    "Segoe UI"
            }}
        >

            <form
                onSubmit={
                    handleLogin
                }

                style={{
                    width: "360px",

                    background:
                        "white",

                    padding: "40px",

                    borderRadius:
                        "20px",

                    boxShadow:
                        "0 10px 30px rgba(0,0,0,0.3)"
                }}
            >

                <h1
                    style={{
                        textAlign:
                            "center",

                        marginBottom:
                            "30px",

                        color:
                            "#0f172a"
                    }}
                >
                    Risk Culture Login
                </h1>

                <input
                    type="text"

                    placeholder="Username"

                    value={username}

                    onChange={(e) =>
                        setUsername(
                            e.target
                                .value
                        )
                    }

                    style={
                        inputStyle
                    }
                />

                <input
                    type="password"

                    placeholder="Password"

                    value={password}

                    onChange={(e) =>
                        setPassword(
                            e.target
                                .value
                        )
                    }

                    style={
                        inputStyle
                    }
                />

                {error && (

                    <p
                        style={{
                            color:
                                "red",

                            marginBottom:
                                "15px",

                            textAlign:
                                "center"
                        }}
                    >
                        {error}
                    </p>

                )}

                <button
                    type="submit"

                    style={{
                        width: "100%",

                        padding:
                            "14px",

                        background:
                            "#2563eb",

                        color:
                            "white",

                        border:
                            "none",

                        borderRadius:
                            "10px",

                        fontWeight:
                            "bold",

                        fontSize:
                            "16px",

                        cursor:
                            "pointer"
                    }}
                >
                    Login
                </button>

            </form>

        </div>
    );
};

const inputStyle = {

    width: "100%",

    padding: "14px",

    marginBottom: "18px",

    borderRadius: "10px",

    border:
        "1px solid #cbd5e1",

    fontSize: "15px",

    boxSizing:
        "border-box"
};

export default LoginPage;