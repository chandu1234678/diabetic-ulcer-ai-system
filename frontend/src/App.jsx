import { useMemo, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import Signup from './pages/Signup'
import ForgotPassword from './pages/ForgotPassword'
import ResetPassword from './pages/ResetPassword'
import Dashboard from './pages/Dashboard'
import FootScanAnalysis from './pages/FootScanAnalysis'
import ScanResults from './pages/ScanResults'
import HealthMetricsResults from './pages/HealthMetricsResults'
import AccountSettings from './pages/AccountSettings'
import ChatbotWorkspace from './pages/ChatbotWorkspace'
import History from './pages/History'

function ProtectedRoute({ isAuthenticated, children }) {
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  return children
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem('access_token')),
  )

  const authApi = useMemo(
    () => ({
      login: () => setIsAuthenticated(true),
      logout: () => {
        localStorage.removeItem('access_token')
        localStorage.removeItem('user_data')
        localStorage.removeItem('patient_profile')
        setIsAuthenticated(false)
      },
    }),
    [],
  )

  return (
    <Routes>
      <Route
        path="/login"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Login onLogin={authApi.login} />
          )
        }
      />
      <Route
        path="/forgot-password"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <ForgotPassword />
          )
        }
      />
      <Route
        path="/signup"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <Signup onLogin={authApi.login} />
          )
        }
      />
      <Route
        path="/reset-password"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <ResetPassword />
          )
        }
      />
      <Route
        path="/dashboard"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <Dashboard onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/foot-scan-analysis"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <FootScanAnalysis onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/scan-results"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <ScanResults onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/health-metrics-results"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <HealthMetricsResults onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/account-settings"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <AccountSettings onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/chatbot"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <ChatbotWorkspace onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/history"
        element={
          <ProtectedRoute isAuthenticated={isAuthenticated}>
            <History onLogout={authApi.logout} />
          </ProtectedRoute>
        }
      />
      <Route
        path="/image-analysis"
        element={<Navigate to="/chatbot" replace />}
      />
      <Route
        path="/"
        element={
          <Navigate to={isAuthenticated ? '/dashboard' : '/login'} replace />
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
