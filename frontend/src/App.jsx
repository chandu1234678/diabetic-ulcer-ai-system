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
import { login, logout } from './services/api'

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
      <Route path="/login" element={<Login onLogin={login} />} />
      <Route path="/forgot-password" element={<ForgotPassword />} />
      <Route path="/signup" element={<Signup onLogin={login} />} />
      <Route path="/reset-password" element={<ResetPassword />} />
      <Route path="/dashboard" element={<Dashboard onLogout={logout} />} />
      <Route path="/foot-scan-analysis" element={<FootScanAnalysis onLogout={logout} />} />
      <Route path="/scan-results" element={<ScanResults onLogout={logout} />} />
      <Route path="/health-metrics-results" element={<HealthMetricsResults onLogout={logout} />} />
      <Route path="/account-settings" element={<AccountSettings onLogout={logout} />} />
      <Route path="/chatbot" element={<ChatbotWorkspace onLogout={logout} />} />
      <Route path="/history" element={<History onLogout={logout} />} />
      <Route path="/image-analysis" element={<Navigate to="/chatbot" replace />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="*" element={<Navigate to="/dashboard" replace />} />
    </Routes>
  )
}

export default App
