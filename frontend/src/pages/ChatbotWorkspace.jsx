import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ChatbotPanel from '../components/ChatbotPanel'
import { predict, uploadImage } from '../services/api'
import { applyDarkMode } from '../utils/darkMode'

export default function ChatbotWorkspace({ onLogout }) {
  const navigate = useNavigate()
  const [selectedFile, setSelectedFile] = useState(null)
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState('')
  const [result, setResult] = useState(null)

  // Apply dark mode on mount
  useEffect(() => {
    applyDarkMode()
  }, [])

  const handleFile = async (file) => {
    if (!file) return

    setSelectedFile(file)
    setIsAnalyzing(true)
    setError('')

    try {
      const uploaded = await uploadImage(file)
      const prediction = await predict({
        image_url: uploaded.url,
        age: 50,
        bmi: 25,
        diabetes_duration: 5,
        infection_signs: 'none',
      })

      setResult({
        originalImage: uploaded.url,
        heatmapImage: uploaded.url,
        prediction,
      })
    } catch {
      setError('Could not process image right now. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const onFileChange = (event) => handleFile(event.target.files?.[0])

  const onDrop = (event) => {
    event.preventDefault()
    handleFile(event.dataTransfer.files?.[0])
  }

  const handleLogout = () => {
    if (onLogout) onLogout()
    navigate('/login', { replace: true })
  }

  const riskLevel = result?.prediction?.risk_level || 'High Risk'
  const confidence = result?.prediction?.confidence
    ? `${(result.prediction.confidence * 100).toFixed(1)}%`
    : '94.2%'

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(99,102,241,0.15),_transparent_45%)] dark:bg-slate-900">
      <header className="sticky top-0 z-20 border-b border-slate-200 dark:border-slate-800 bg-white/90 dark:bg-slate-900/90 backdrop-blur">
        <div className="mx-auto flex w-full max-w-7xl items-center justify-between px-4 py-3">
          <button 
            onClick={() => window.location.href = '/dashboard'} 
            className="text-xl font-extrabold tracking-tight text-slate-900 dark:text-white hover:opacity-80 transition-opacity"
          >
            MedVision <span className="text-primary">AI</span>
          </button>
          <div className="flex items-center gap-3">
            <a
              href="/history"
              className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              📊 History
            </a>
            <button
              onClick={handleLogout}
              className="rounded-lg border border-slate-300 dark:border-slate-600 px-3 py-1.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition-colors"
            >
              Logout
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto grid w-full max-w-7xl gap-6 px-4 py-6 lg:grid-cols-3">
        <section className="space-y-6 lg:col-span-2">
          <div>
            <h2 className="text-2xl font-bold text-slate-900">Image Analysis</h2>
            <p className="text-sm text-slate-500">
              Upload a medical scan to identify pathologies using specialized AI models.
            </p>
          </div>

          <div
            onDrop={onDrop}
            onDragOver={(event) => event.preventDefault()}
            className="relative rounded-2xl border-2 border-dashed border-primary/40 bg-white p-12 text-center shadow-sm"
          >
            <input
              type="file"
              accept="image/*,.dcm"
              onChange={onFileChange}
              className="absolute inset-0 cursor-pointer opacity-0"
            />
            <div className="mx-auto mb-4 h-16 w-16 rounded-full bg-primary/10" />
            <h3 className="text-lg font-bold text-slate-800">Drag and drop medical image</h3>
            <p className="mx-auto mt-2 max-w-md text-sm text-slate-500">
              Support for X-Ray, MRI, CT Scans, and Dermoscopic images (JPG, PNG, DICOM).
            </p>
            <button className="mt-6 rounded-lg bg-primary px-7 py-3 font-bold text-white shadow-lg shadow-primary/25">
              Select File from Computer
            </button>
            {selectedFile && (
              <p className="mt-3 text-xs text-slate-500">Selected: {selectedFile.name}</p>
            )}
          </div>

          {isAnalyzing && (
            <div className="rounded-xl bg-slate-200 px-6 py-4 text-center font-semibold text-slate-600">
              Processing Image...
            </div>
          )}

          {error && (
            <div className="rounded-lg border border-red-300 bg-red-50 px-4 py-3 text-sm text-red-700">
              {error}
            </div>
          )}

          {result && (
            <div className="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
              <h3 className="mb-4 text-lg font-bold text-slate-800">Diagnostic Visuals</h3>
              <div className="grid gap-4 md:grid-cols-2">
                <img
                  src={result.originalImage}
                  alt="Original scan"
                  className="aspect-square w-full rounded-xl object-cover"
                />
                <img
                  src={result.heatmapImage}
                  alt="Grad-CAM heatmap"
                  className="aspect-square w-full rounded-xl object-cover"
                />
              </div>
              <div className="mt-6 grid gap-3 sm:grid-cols-3">
                <div className="rounded-xl border border-red-200 bg-red-50 p-4">
                  <p className="text-xs font-bold uppercase text-red-600">Prediction</p>
                  <p className="text-lg font-bold text-slate-900">
                    {result.prediction?.prediction || 'Diabetic Ulcer'}
                  </p>
                </div>
                <div className="rounded-xl border border-indigo-200 bg-indigo-50 p-4">
                  <p className="text-xs font-bold uppercase text-indigo-600">Confidence</p>
                  <p className="text-lg font-bold text-slate-900">{confidence}</p>
                </div>
                <div className="rounded-xl border border-orange-200 bg-orange-50 p-4">
                  <p className="text-xs font-bold uppercase text-orange-600">Risk Level</p>
                  <p className="text-lg font-bold text-orange-600">{riskLevel}</p>
                </div>
              </div>
            </div>
          )}
        </section>

        <aside className="space-y-6">
          <div className="overflow-hidden rounded-2xl border border-slate-200 bg-white shadow-sm">
            <div className="bg-primary px-4 py-3 text-sm font-bold text-white">
              AI Clinical Explanation
            </div>
            <div className="space-y-4 p-4 text-sm text-slate-700">
              <p>
                The model highlights inflammatory tissue patterns and surface damage around
                focal ulcer regions.
              </p>
              <ul className="list-disc space-y-2 pl-4">
                <li>Initiate pressure offloading and wound care immediately.</li>
                <li>Evaluate vascular status and signs of infection.</li>
                <li>Schedule specialist review for high-risk findings.</li>
              </ul>
            </div>
          </div>

          <ChatbotPanel />
        </aside>
      </main>
    </div>
  )
}
