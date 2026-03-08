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
  // No login restriction: always render children
  return children
}

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(
    Boolean(localStorage.getItem('access_token'))
  )
  return (
    <Routes>
      <Route path="/login" element={<Login onLogin={authApi.login} />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/signup" element={<Signup onLogin={authApi.login} />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/dashboard" element={<Dashboard onLogout={authApi.logout} />} />
      <Route path="/foot-scan-analysis" element={<FootScanAnalysis onLogout={authApi.logout} />} />
      <Route path="/scan-results" element={<ScanResults onLogout={authApi.logout} />} />
      <Route path="/health-metrics-results" element={<HealthMetricsResults onLogout={authApi.logout} />} />
      <Route path="/account-settings" element={<AccountSettings onLogout={authApi.logout} />} />
      <Route path="/chatbot" element={<ChatbotWorkspace onLogout={authApi.logout} />} />
      <Route path="/history" element={<History onLogout={authApi.logout} />} />
      <Route path="/image-analysis" element={<Navigate to="/chatbot" replace />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default App
