import {
  Routes,
  Route,
  Navigate
} from "react-router-dom";

import DashboardPage from "./pages/DashboardPage";
import AnalyticsPage from "./pages/AnalyticsPage";

import EditSurveyPage from "./pages/EditSurveyPage";

import SurveyDetailPage from "./pages/SurveyDetailPage";

import LoginPage from "./pages/LoginPage";

import SurveyListPage from "./pages/SurveyListPage";
import ErrorBoundary from "./ErrorBoundary";

function App() {

  const token =
    localStorage.getItem(
      "token"
    );

  return (
    <ErrorBoundary>

    <Routes>

      <Route
        path="/login"
        element={<LoginPage />}
      />

      <Route
        path="/dashboard"
        element={
          token
            ? <DashboardPage />
            : <Navigate to="/login" />
        }
      />
      <Route
  path="/analytics"

  element={
    token
      ? <AnalyticsPage />
      : <Navigate to="/login" />
  }
/>

      <Route
        path="/surveys"
        element={
          token
            ? <SurveyListPage />
            : <Navigate to="/login" />
        }
      />

      <Route
        path="/survey/:id"
        element={
          token
            ? <SurveyDetailPage />
            : <Navigate to="/login" />
        }
      />

      <Route
        path="/edit/:id"
        element={
          token
            ? <EditSurveyPage />
            : <Navigate to="/login" />
        }
      />

      <Route
        path="*"
        element={
          <Navigate to="/login" />
        }
      />

    </Routes>
    </ErrorBoundary>

  );
}

export default App;