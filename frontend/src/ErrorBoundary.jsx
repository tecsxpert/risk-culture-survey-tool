import React from "react";

class ErrorBoundary extends React.Component {

    constructor(props) {

        super(props);

        this.state = {

            hasError: false
        };
    }

    static getDerivedStateFromError() {

        return {

            hasError: true
        };
    }

    componentDidCatch(

        error,

        errorInfo

    ) {

        console.error(

            error,

            errorInfo
        );
    }

    render() {

        if (

            this.state.hasError

        ) {

            return (

                <div
                    style={{
                        minHeight: "100vh",

                        display: "flex",

                        justifyContent: "center",

                        alignItems: "center",

                        background: "#0f172a",

                        color: "white",

                        flexDirection: "column"
                    }}
                >

                    <h1>
                        Something went wrong
                    </h1>

                    <p>
                        Please refresh
                        the page.
                    </p>

                </div>
            );
        }

        return this.props.children;
    }
}

export default ErrorBoundary;