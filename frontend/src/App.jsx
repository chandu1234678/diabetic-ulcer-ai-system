import { useMemo, useState } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import Login from './pages/Login'
import ChatbotWorkspace from './pages/ChatbotWorkspace'

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
            <Navigate to="/chatbot" replace />
          ) : (
            <Login onLogin={authApi.login} />
          )
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
        path="/image-analysis"
        element={<Navigate to="/chatbot" replace />}
      />
      <Route
        path="/"
        element={
          <Navigate to={isAuthenticated ? '/chatbot' : '/login'} replace />
        }
      />
      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}

export default App
