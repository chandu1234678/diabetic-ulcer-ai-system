import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { applyDarkMode, toggleDarkMode } from '../utils/darkMode'

// Sample history data - replace with API call to backend
const sampleHistory = [
  {
    id: 1,
    patientId: 'PT-2024-001',
    timestamp: '2024-03-05 14:23',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+1',
    heatmapImage: 'https://via.placeholder.com/300x300/ff6b6b/fff?text=Heatmap+1',
    prediction: 'Diabetic Foot Ulcer Detected',
    confidence: 94.2,
    riskLevel: 'High Risk',
    aiSuggestion: 'Immediate intervention recommended. Grade 3 ulcer detected with signs of infection. Recommend wound care specialist consultation within 24 hours.',
    severity: 'Critical',
    location: 'Left Plantar',
  },
  {
    id: 2,
    patientId: 'PT-2024-002',
    timestamp: '2024-03-05 11:15',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+2',
    heatmapImage: 'https://via.placeholder.com/300x300/ffd93d/fff?text=Heatmap+2',
    prediction: 'Early Stage Ulceration',
    confidence: 87.5,
    riskLevel: 'Moderate Risk',
    aiSuggestion: 'Monitor closely. Early signs of tissue breakdown detected. Recommend offloading pressure and improved glycemic control.',
    severity: 'Moderate',
    location: 'Right Heel',
  },
  {
    id: 3,
    patientId: 'PT-2024-003',
    timestamp: '2024-03-04 16:47',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+3',
    heatmapImage: 'https://via.placeholder.com/300x300/6bcf7f/fff?text=Heatmap+3',
    prediction: 'No Abnormalities Detected',
    confidence: 96.8,
    riskLevel: 'Low Risk',
    aiSuggestion: 'Healthy tissue detected. Continue regular monitoring and preventive care. No immediate intervention required.',
    severity: 'Normal',
    location: 'Bilateral Feet',
  },
  {
    id: 4,
    patientId: 'PT-2024-004',
    timestamp: '2024-03-04 09:32',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+4',
    heatmapImage: 'https://via.placeholder.com/300x300/ff9999/fff?text=Heatmap+4',
    prediction: 'Chronic Wound with Infection',
    confidence: 91.3,
    riskLevel: 'High Risk',
    aiSuggestion: 'Active infection markers detected. Bacterial culture recommended. Consider antibiotic therapy and aggressive wound management.',
    severity: 'Critical',
    location: 'Left Toe',
  },
  {
    id: 5,
    patientId: 'PT-2024-005',
    timestamp: '2024-03-03 13:58',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+5',
    heatmapImage: 'https://via.placeholder.com/300x300/ffb84d/fff?text=Heatmap+5',
    prediction: 'Pre-Ulcerative Changes',
    confidence: 83.7,
    riskLevel: 'Moderate Risk',
    aiSuggestion: 'Tissue changes indicate increased risk. Implement preventive measures including specialized footwear and regular inspection.',
    severity: 'Moderate',
    location: 'Right Ball',
  },
  {
    id: 6,
    patientId: 'PT-2024-006',
    timestamp: '2024-03-02 10:21',
    originalImage: 'https://via.placeholder.com/300x300/e0e0e0/666?text=Scan+6',
    heatmapImage: 'https://via.placeholder.com/300x300/6bcf7f/fff?text=Heatmap+6',
    prediction: 'Healthy Tissue',
    confidence: 98.1,
    riskLevel: 'Low Risk',
    aiSuggestion: 'No pathological findings. Maintain current preventive care routine.',
    severity: 'Normal',
    location: 'Both Feet',
  },
]

export default function History({ onLogout }) {
  const navigate = useNavigate()
  const [selectedEntry, setSelectedEntry] = useState(null)
  const [filterRisk, setFilterRisk] = useState('all')
  const [searchQuery, setSearchQuery] = useState('')
  const [viewMode, setViewMode] = useState('grid') // grid or list
  const [isDarkMode, setIsDarkMode] = useState(false)

  // Apply dark mode on mount - default to light mode
  useEffect(() => {
    const savedDarkMode = localStorage.getItem('darkMode') === 'true'
    setIsDarkMode(savedDarkMode)
    applyDarkMode()
  }, [])

  const handleDarkModeToggle = () => {
    const newMode = !isDarkMode
    setIsDarkMode(newMode)
    toggleDarkMode(newMode)
  }

  const handleLogout = () => {
    if (onLogout) onLogout()
    navigate('/login', { replace: true })
  }

  const filteredHistory = sampleHistory.filter((entry) => {
    const matchesRisk = filterRisk === 'all' || entry.riskLevel === filterRisk
    const matchesSearch =
      searchQuery === '' ||
      entry.patientId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      entry.prediction.toLowerCase().includes(searchQuery.toLowerCase())
    return matchesRisk && matchesSearch
  })

  const getRiskColor = (risk) => {
    switch (risk) {
      case 'High Risk':
        return 'bg-red-100 text-red-800 border-red-200'
      case 'Moderate Risk':
        return 'bg-yellow-100 text-yellow-800 border-yellow-200'
      case 'Low Risk':
        return 'bg-green-100 text-green-800 border-green-200'
      default:
        return 'bg-gray-100 text-gray-800 border-gray-200'
    }
  }

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'Critical':
        return 'text-red-600'
      case 'Moderate':
        return 'text-yellow-600'
      case 'Normal':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="min-h-screen bg-light dark:bg-slate-950 text-slate-900 dark:text-white font-display">
      {/* Header */}
      <header className="sticky top-0 z-20 border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur">
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3">
          <button 
            onClick={() => navigate('/dashboard')} 
            className="text-xl font-extrabold tracking-tight text-slate-900 dark:text-white hover:opacity-80 transition-opacity"
          >
            MedVision <span className="text-primary">AI</span>
          </button>
          <div className="flex items-center gap-3">
            <button
              onClick={handleDarkModeToggle}
              className="size-10 flex items-center justify-center rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-600 dark:text-slate-300 transition-colors"
              title={isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode'}
            >
              <span className="material-symbols-outlined">{isDarkMode ? 'light_mode' : 'dark_mode'}</span>
            </button>
            <button
              onClick={() => navigate('/chatbot')}
              className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              ← Back to Analysis
            </button>
            <button
              onClick={handleLogout}
              className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto w-full max-w-7xl px-4 py-6">
        {/* Page Title */}
        <div className="mb-6">
          <h2 className="text-3xl font-bold text-slate-900">Analysis History</h2>
          <p className="mt-1 text-sm text-slate-500">
            View all past medical image analyses and AI recommendations
          </p>
        </div>

        {/* Filters and Search */}
        <div className="mb-6 flex flex-col gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm sm:flex-row sm:items-center sm:justify-between">
          <div className="flex flex-wrap items-center gap-3">
            <span className="text-sm font-semibold text-slate-700">Filter by Risk:</span>
            <button
              onClick={() => setFilterRisk('all')}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
                filterRisk === 'all'
                  ? 'bg-primary text-white'
                  : 'border border-slate-300 text-slate-700 hover:bg-slate-50'
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilterRisk('High Risk')}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
                filterRisk === 'High Risk'
                  ? 'bg-red-600 text-white'
                  : 'border border-slate-300 text-slate-700 hover:bg-slate-50'
              }`}
            >
              High Risk
            </button>
            <button
              onClick={() => setFilterRisk('Moderate Risk')}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
                filterRisk === 'Moderate Risk'
                  ? 'bg-yellow-600 text-white'
                  : 'border border-slate-300 text-slate-700 hover:bg-slate-50'
              }`}
            >
              Moderate Risk
            </button>
            <button
              onClick={() => setFilterRisk('Low Risk')}
              className={`rounded-lg px-3 py-1.5 text-sm font-semibold transition ${
                filterRisk === 'Low Risk'
                  ? 'bg-green-600 text-white'
                  : 'border border-slate-300 text-slate-700 hover:bg-slate-50'
              }`}
            >
              Low Risk
            </button>
          </div>

          <div className="flex items-center gap-3">
            <input
              type="text"
              placeholder="Search patient ID or diagnosis..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full rounded-lg border border-slate-300 px-4 py-2 text-sm focus:border-primary focus:outline-none focus:ring-2 focus:ring-primary/20 sm:w-64"
            />
            <div className="flex gap-1 rounded-lg border border-slate-300 p-1">
              <button
                onClick={() => setViewMode('grid')}
                className={`rounded px-2 py-1 text-sm ${
                  viewMode === 'grid' ? 'bg-primary text-white' : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                Grid
              </button>
              <button
                onClick={() => setViewMode('list')}
                className={`rounded px-2 py-1 text-sm ${
                  viewMode === 'list' ? 'bg-primary text-white' : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                List
              </button>
            </div>
          </div>
        </div>

        {/* Results Count */}
        <div className="mb-4 text-sm text-slate-600">
          Showing <span className="font-semibold">{filteredHistory.length}</span> of{' '}
          <span className="font-semibold">{sampleHistory.length}</span> analyses
        </div>

        {/* History Grid/List */}
        {viewMode === 'grid' ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {filteredHistory.map((entry) => (
              <div
                key={entry.id}
                onClick={() => setSelectedEntry(entry)}
                className="group cursor-pointer overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-lg hover:shadow-primary/10"
              >
                {/* Images */}
                <div className="grid grid-cols-2 gap-0.5 bg-slate-100">
                  <div className="relative aspect-square overflow-hidden">
                    <img
                      src={entry.originalImage}
                      alt="Original scan"
                      className="h-full w-full object-cover transition group-hover:scale-105"
                    />
                    <div className="absolute bottom-2 left-2 rounded bg-black/60 px-2 py-0.5 text-xs font-semibold text-white">
                      Original
                    </div>
                  </div>
                  <div className="relative aspect-square overflow-hidden">
                    <img
                      src={entry.heatmapImage}
                      alt="AI Heatmap"
                      className="h-full w-full object-cover transition group-hover:scale-105"
                    />
                    <div className="absolute bottom-2 left-2 rounded bg-black/60 px-2 py-0.5 text-xs font-semibold text-white">
                      Heatmap
                    </div>
                  </div>
                </div>

                {/* Details */}
                <div className="p-4">
                  <div className="mb-2 flex items-start justify-between">
                    <div>
                      <p className="text-xs font-semibold text-primary">{entry.patientId}</p>
                      <p className="text-xs text-slate-500">{entry.timestamp}</p>
                    </div>
                    <span
                      className={`rounded-full border px-2 py-0.5 text-xs font-bold ${getRiskColor(
                        entry.riskLevel
                      )}`}
                    >
                      {entry.riskLevel}
                    </span>
                  </div>

                  <h3 className={`mb-1 font-bold ${getSeverityColor(entry.severity)}`}>
                    {entry.prediction}
                  </h3>
                  <p className="mb-2 text-xs text-slate-600">Location: {entry.location}</p>

                  <div className="mb-3 rounded-lg bg-slate-50 p-2">
                    <p className="text-xs text-slate-700 line-clamp-2">{entry.aiSuggestion}</p>
                  </div>

                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-xs text-slate-500">Confidence</p>
                      <p className="text-lg font-bold text-slate-900">{entry.confidence}%</p>
                    </div>
                    <button className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white transition hover:bg-primary/90">
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <div className="space-y-3">
            {filteredHistory.map((entry) => (
              <div
                key={entry.id}
                onClick={() => setSelectedEntry(entry)}
                className="group cursor-pointer overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm transition hover:shadow-lg hover:shadow-primary/10"
              >
                <div className="flex gap-4 p-4">
                  {/* Thumbnail Images */}
                  <div className="flex gap-2">
                    <div className="relative h-24 w-24 overflow-hidden rounded-lg">
                      <img
                        src={entry.originalImage}
                        alt="Original"
                        className="h-full w-full object-cover transition group-hover:scale-105"
                      />
                      <div className="absolute bottom-1 left-1 rounded bg-black/60 px-1.5 py-0.5 text-xs font-semibold text-white">
                        Original
                      </div>
                    </div>
                    <div className="relative h-24 w-24 overflow-hidden rounded-lg">
                      <img
                        src={entry.heatmapImage}
                        alt="Heatmap"
                        className="h-full w-full object-cover transition group-hover:scale-105"
                      />
                      <div className="absolute bottom-1 left-1 rounded bg-black/60 px-1.5 py-0.5 text-xs font-semibold text-white">
                        Heatmap
                      </div>
                    </div>
                  </div>

                  {/* Details */}
                  <div className="flex flex-1 flex-col justify-between">
                    <div>
                      <div className="mb-2 flex items-start justify-between">
                        <div>
                          <p className="text-sm font-semibold text-primary">{entry.patientId}</p>
                          <p className="text-xs text-slate-500">{entry.timestamp}</p>
                        </div>
                        <span
                          className={`rounded-full border px-3 py-1 text-xs font-bold ${getRiskColor(
                            entry.riskLevel
                          )}`}
                        >
                          {entry.riskLevel}
                        </span>
                      </div>
                      <h3 className={`mb-1 text-lg font-bold ${getSeverityColor(entry.severity)}`}>
                        {entry.prediction}
                      </h3>
                      <p className="mb-2 text-sm text-slate-600">Location: {entry.location}</p>
                      <p className="text-sm text-slate-700">{entry.aiSuggestion}</p>
                    </div>
                  </div>

                  {/* Actions */}
                  <div className="flex flex-col items-end justify-between">
                    <div className="text-right">
                      <p className="text-xs text-slate-500">Confidence</p>
                      <p className="text-2xl font-bold text-slate-900">{entry.confidence}%</p>
                    </div>
                    <button className="rounded-lg bg-primary px-5 py-2 text-sm font-semibold text-white transition hover:bg-primary/90">
                      View Details
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {/* No Results */}
        {filteredHistory.length === 0 && (
          <div className="rounded-2xl border-2 border-dashed border-slate-300 bg-white p-12 text-center">
            <p className="text-lg font-semibold text-slate-700">No analyses found</p>
            <p className="mt-2 text-sm text-slate-500">
              Try adjusting your filters or search query
            </p>
          </div>
        )}
      </main>

      {/* Detail Modal */}
      {selectedEntry && (
        <div
          className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4"
          onClick={() => setSelectedEntry(null)}
        >
          <div
            className="relative max-h-[90vh] w-full max-w-4xl overflow-y-auto rounded-2xl border border-slate-200 bg-white shadow-2xl"
            onClick={(e) => e.stopPropagation()}
          >
            {/* Modal Header */}
            <div className="sticky top-0 z-10 flex items-center justify-between border-b border-slate-200 bg-white px-6 py-4">
              <div>
                <h3 className="text-xl font-bold text-slate-900">Analysis Details</h3>
                <p className="text-sm text-slate-500">
                  {selectedEntry.patientId} • {selectedEntry.timestamp}
                </p>
              </div>
              <button
                onClick={() => setSelectedEntry(null)}
                className="rounded-lg p-2 text-slate-500 hover:bg-slate-100"
              >
                <svg
                  className="h-6 w-6"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M6 18L18 6M6 6l12 12"
                  />
                </svg>
              </button>
            </div>

            {/* Modal Content */}
            <div className="p-6">
              {/* Images */}
              <div className="mb-6 grid gap-4 md:grid-cols-2">
                <div className="overflow-hidden rounded-xl border border-slate-200">
                  <img
                    src={selectedEntry.originalImage}
                    alt="Original scan"
                    className="h-full w-full object-cover"
                  />
                  <div className="border-t border-slate-200 bg-slate-50 p-2 text-center text-sm font-semibold text-slate-700">
                    Original Scan
                  </div>
                </div>
                <div className="overflow-hidden rounded-xl border border-slate-200">
                  <img
                    src={selectedEntry.heatmapImage}
                    alt="AI Heatmap"
                    className="h-full w-full object-cover"
                  />
                  <div className="border-t border-slate-200 bg-slate-50 p-2 text-center text-sm font-semibold text-slate-700">
                    AI Attention Heatmap
                  </div>
                </div>
              </div>

              {/* Analysis Results */}
              <div className="mb-6 rounded-xl border border-slate-200 bg-slate-50 p-4">
                <h4 className="mb-3 font-bold text-slate-900">Analysis Results</h4>
                <div className="grid gap-3 md:grid-cols-2">
                  <div>
                    <p className="text-xs text-slate-500">Diagnosis</p>
                    <p className={`text-lg font-bold ${getSeverityColor(selectedEntry.severity)}`}>
                      {selectedEntry.prediction}
                    </p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Risk Level</p>
                    <span
                      className={`inline-block rounded-full border px-3 py-1 text-sm font-bold ${getRiskColor(
                        selectedEntry.riskLevel
                      )}`}
                    >
                      {selectedEntry.riskLevel}
                    </span>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Confidence Score</p>
                    <p className="text-lg font-bold text-slate-900">{selectedEntry.confidence}%</p>
                  </div>
                  <div>
                    <p className="text-xs text-slate-500">Location</p>
                    <p className="text-lg font-bold text-slate-900">{selectedEntry.location}</p>
                  </div>
                </div>
              </div>

              {/* AI Recommendation */}
              <div className="rounded-xl border border-primary/20 bg-primary/5 p-4">
                <h4 className="mb-2 font-bold text-slate-900">AI Clinical Recommendation</h4>
                <p className="text-slate-700">{selectedEntry.aiSuggestion}</p>
              </div>

              {/* Action Buttons */}
              <div className="mt-6 flex gap-3">
                <button className="flex-1 rounded-lg bg-primary px-6 py-3 font-semibold text-white hover:bg-primary/90">
                  Download Report
                </button>
                <button className="flex-1 rounded-lg border border-slate-300 px-6 py-3 font-semibold text-slate-700 hover:bg-slate-50">
                  Share with Specialist
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
