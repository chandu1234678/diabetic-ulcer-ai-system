import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { uploadImage, predict, logout } from '../services/api'
import { getHealthMetricsAssessment } from '../services/api'
import HealthMetricsForm from '../components/HealthMetricsForm'
import DashboardHeader from '../components/DashboardHeader'

export default function FootScanAnalysis({ onLogout }) {
  const navigate = useNavigate()
  const [uploadedImage, setUploadedImage] = useState(null)
  const [previewImage, setPreviewImage] = useState(null)
  const [activeNav, setActiveNav] = useState('scan')
  const [isAnalyzing, setIsAnalyzing] = useState(false)
  const [error, setError] = useState('')
  const [age, setAge] = useState('')
  const [bmi, setBmi] = useState('')
  const [sugarBeforeFast, setSugarBeforeFast] = useState('')
  const [uploadProgress, setUploadProgress] = useState(0)
  const [uploadStartTime, setUploadStartTime] = useState(null)
  const [analysisSuccess, setAnalysisSuccess] = useState(false)

  // Load health metrics defaults from localStorage on mount
  useEffect(() => {
    const savedMetrics = JSON.parse(localStorage.getItem('health_metrics_defaults') || '{}')
    if (savedMetrics.age) setAge(String(savedMetrics.age))
    if (savedMetrics.bmi) setBmi(String(savedMetrics.bmi))
    if (savedMetrics.blood_sugar) setSugarBeforeFast(String(savedMetrics.blood_sugar))
  }, [])

  const handleFileUpload = (file) => {
    if (file && file.type.startsWith('image/')) {
      const reader = new FileReader()
      reader.onload = (e) => {
        setUploadedImage(file)
        setPreviewImage(e.target.result)
        setError('')
      }
      reader.readAsDataURL(file)
    }
  }

  const handleDragDrop = (e) => {
    e.preventDefault()
    const file = e.dataTransfer.files[0]
    handleFileUpload(file)
  }

  const handleBrowseClick = () => {
    const input = document.getElementById('file-input')
    input?.click()
  }

  const handleStartAnalysis = async () => {
    if (!uploadedImage || !previewImage) {
      setError('Please upload an image first')
      return
    }

    if (!age || !bmi || !sugarBeforeFast) {
      setError('Please fill in all health metrics before analyzing')
      return
    }

    setIsAnalyzing(true)
    setError('')
    setUploadProgress(0)
    setUploadStartTime(Date.now())
    setAnalysisSuccess(false)

    try {
      // Simulate upload progress
      const uploadInterval = setInterval(() => {
        setUploadProgress((prev) => {
          if (prev >= 90) {
            clearInterval(uploadInterval)
            return 90
          }
          return prev + Math.random() * 20
        })
      }, 300)

      const uploadResponse = await uploadImage(uploadedImage)
      clearInterval(uploadInterval)
      setUploadProgress(100)
      
      const imageUrl = uploadResponse.url

      const patientProfile = JSON.parse(localStorage.getItem('patient_profile') || '{}')
      
      const predictionResponse = await predict({
        image_url: imageUrl,
        age: parseInt(age),
        bmi: parseFloat(bmi),
        diabetes_duration: parseInt(patientProfile.diabetes_duration) || 0,
        infection_signs: 'none',
        patient_id: patientProfile.id || null
      })

      setAnalysisSuccess(true)
      
      setTimeout(() => {
        navigate('/scan-results', {
          state: { 
            previewImage,
            prediction: predictionResponse,
            healthMetrics: {
              age: parseInt(age),
              bmi: parseFloat(bmi),
              bloodSugar: parseInt(sugarBeforeFast)
            }
          }
        })
      }, 1500)
    } catch (err) {
      console.error('Analysis error:', err)
      setError(err.response?.data?.detail || 'Failed to analyze image. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleViewHealthMetrics = async () => {
    if (!age || !bmi || !sugarBeforeFast) {
      setError('Please fill in all health metrics')
      return
    }

    try {
      setIsAnalyzing(true)
      const assessment = await getHealthMetricsAssessment({
        age: parseInt(age),
        bmi: parseFloat(bmi),
        blood_sugar: parseInt(sugarBeforeFast),
      })

      navigate('/health-metrics-results', {
        state: {
          assessment,
          healthMetrics: {
            age: parseInt(age),
            bmi: parseFloat(bmi),
            bloodSugar: parseInt(sugarBeforeFast)
          },
          previewImage
        }
      })
    } catch (err) {
      console.error('Error fetching assessment:', err)
      setError('Failed to calculate health metrics. Please try again.')
    } finally {
      setIsAnalyzing(false)
    }
  }

  const handleLogout = () => {
    if (onLogout) {
      onLogout()
    }
    navigate('/login', { replace: true })
  }

  const patientProfile = JSON.parse(localStorage.getItem('patient_profile') || '{}')
  const userName = patientProfile.full_name || 'Alex Johnson'

  return (
    <div className="min-h-screen flex flex-col bg-background-light text-slate-900 font-display">
      <DashboardHeader 
        title="HealthScan AI" 
        onLogout={onLogout}
      />

      <div className="flex min-h-[calc(100vh-4rem)]">
        {/* Sidebar */}
        <aside className="hidden lg:flex w-64 flex-col border-r border-slate-200 bg-white p-6">
          <nav className="flex flex-col gap-2">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-600 hover:bg-slate-100 transition-all text-left"
            >
              <span className="material-symbols-outlined">dashboard</span>
              <span className="font-medium">Dashboard</span>
            </button>
            <button
              onClick={() => setActiveNav('scan')}
              className="flex items-center gap-3 rounded-lg px-4 py-3 bg-primary/10 text-primary transition-all text-left"
            >
              <span className="material-symbols-outlined">camera</span>
              <span className="font-medium">New Analysis</span>
            </button>
            <button
              onClick={() => navigate('/history')}
              className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-600 hover:bg-slate-100 transition-all text-left"
            >
              <span className="material-symbols-outlined">history</span>
              <span className="font-medium">History</span>
            </button>
            <button className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-600 hover:bg-slate-100 transition-all text-left">
              <span className="material-symbols-outlined">medical_information</span>
              <span className="font-medium">Records</span>
            </button>
            <div className="my-4 h-px bg-slate-200"></div>
            <button className="flex items-center gap-3 rounded-lg px-4 py-3 text-slate-600 hover:bg-slate-100 transition-all text-left">
              <span className="material-symbols-outlined">settings</span>
              <span className="font-medium">Settings</span>
            </button>
          </nav>
          <div className="mt-auto rounded-2xl bg-slate-50 p-4 border border-slate-200">
            <p className="text-xs font-bold uppercase tracking-wider text-slate-400">Health Tip</p>
            <p className="mt-2 text-sm leading-relaxed text-slate-600">Regular foot checks can help detect early signs of vascular issues.</p>
          </div>
        </aside>

        {/* Main Content */}
        <main className="flex-1 p-4 lg:p-8 pb-24 lg:pb-8">
          <div className="mx-auto max-w-4xl">
            <div className="mb-8 text-center lg:text-left">
              <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-slate-900">Upload Foot Image</h2>
              <p className="mt-3 text-lg text-slate-600">Get an instant AI-powered preliminary assessment of your foot health.</p>
            </div>
            <div className="grid gap-8 lg:grid-cols-12">
              {/* Uploader Section */}
              <div className="lg:col-span-8">
                <div
                  className="rounded-xl border-2 border-dashed border-primary/30 bg-white p-12 transition-all hover:border-primary/60 hover:shadow-xl hover:shadow-primary/5 cursor-pointer"
                  onDragOver={(e) => e.preventDefault()}
                  onDrop={handleDragDrop}
                  onClick={handleBrowseClick}
                >
                  <div className="flex flex-col items-center justify-center text-center">
                    <div className="mb-6 flex size-20 items-center justify-center rounded-full bg-primary/10 text-primary">
                      <span className="material-symbols-outlined text-4xl">cloud_upload</span>
                    </div>
                    <h3 className="mb-2 text-xl font-bold text-slate-900">Drag and drop your image</h3>
                    <p className="mb-8 text-slate-500">Supports JPG, PNG (Max 10MB)</p>
                    <button
                      type="button"
                      onClick={handleBrowseClick}
                      className="rounded-full bg-primary px-8 py-3 font-bold text-white shadow-lg shadow-primary/30 transition-transform hover:bg-primary/90 active:scale-95"
                    >
                      Browse Files
                    </button>
                    <input
                      id="file-input"
                      type="file"
                      accept="image/*"
                      className="hidden"
                      onChange={(e) => handleFileUpload(e.target.files?.[0])}
                    />
                  </div>
                </div>

                {/* Analysis Instructions */}
                <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-3">
                  <div className="flex items-start gap-3 rounded-xl bg-white p-4 shadow-sm border border-slate-200">
                    <span className="material-symbols-outlined text-primary flex-shrink-0">light_mode</span>
                    <div>
                      <p className="text-sm font-bold text-slate-900">Good Lighting</p>
                      <p className="text-xs text-slate-500">Ensure area is well-lit</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 rounded-xl bg-white p-4 shadow-sm border border-slate-200">
                    <span className="material-symbols-outlined text-primary flex-shrink-0">center_focus_strong</span>
                    <div>
                      <p className="text-sm font-bold text-slate-900">Clear Focus</p>
                      <p className="text-xs text-slate-500">Keep camera steady</p>
                    </div>
                  </div>
                  <div className="flex items-start gap-3 rounded-xl bg-white p-4 shadow-sm border border-slate-200">
                    <span className="material-symbols-outlined text-primary flex-shrink-0">straighten</span>
                    <div>
                      <p className="text-sm font-bold text-slate-900">Angle</p>
                      <p className="text-xs text-slate-500">Top or side views</p>
                    </div>
                  </div>
                </div>
              </div>

              {/* Preview Section */}
              <div className="lg:col-span-4">
                <div className="sticky top-24 space-y-6">
                  {/* Health Metrics Card */}
                  <div className="rounded-xl bg-white p-5 shadow-lg ring-1 ring-slate-200">
                    <h4 className="mb-4 text-sm font-bold uppercase tracking-wider text-slate-500 flex items-center gap-2">
                      <span className="material-symbols-outlined text-primary">favorite</span>
                      Health Metrics
                    </h4>
                    <HealthMetricsForm
                      age={age}
                      setAge={setAge}
                      bmi={bmi}
                      setBmi={setBmi}
                      sugarBeforeFast={sugarBeforeFast}
                      setSugarBeforeFast={setSugarBeforeFast}
                      compact={true}
                    />
                    {age && bmi && sugarBeforeFast && (
                      <button
                        onClick={handleViewHealthMetrics}
                        disabled={isAnalyzing}
                        className="w-full mt-4 px-4 py-2.5 rounded-lg bg-gradient-to-r from-primary to-blue-600 text-white font-semibold hover:from-primary/90 hover:to-blue-600/90 transition-all disabled:opacity-50 flex items-center justify-center gap-2"
                      >
                        <span className="material-symbols-outlined text-base">assessment</span>
                        View Health Assessment
                      </button>
                    )}
                  </div>

                  {/* Image Preview Card */}
                  <div className="rounded-xl bg-white p-4 shadow-lg ring-1 ring-slate-200">
                    <h4 className="mb-4 text-sm font-bold uppercase tracking-wider text-slate-500">Preview</h4>
                    <div className="relative aspect-square overflow-hidden rounded-lg bg-slate-100 border-2 border-dashed border-slate-200">
                      {previewImage ? (
                        <div>
                          <img
                            alt="Uploaded foot scan"
                            className="h-full w-full object-cover"
                            src={previewImage}
                          />
                          <div className="absolute top-2 right-2 flex items-center gap-1.5 rounded-lg bg-green-500/90 text-white px-3 py-1.5 text-xs font-bold">
                            <span className="material-symbols-outlined text-sm">check_circle</span>
                            Uploaded
                          </div>
                          <p className="absolute bottom-2 left-2 right-2 text-xs font-bold text-white bg-slate-900/70 px-2 py-1 rounded truncate">
                            {uploadedImage?.name || 'Image uploaded'}
                          </p>
                        </div>
                      ) : (
                        <div className="absolute inset-0 flex items-center justify-center">
                          <p className="text-sm text-slate-400">No image selected</p>
                        </div>
                      )}
                    </div>

                    {/* Upload Progress */}
                    {isAnalyzing && (
                      <div className="mt-4">
                        <div className="flex items-center justify-between mb-2">
                          <p className="text-xs font-semibold text-slate-600">Analyzing...</p>
                          <p className="text-xs font-bold text-primary">{Math.round(uploadProgress)}%</p>
                        </div>
                        <div className="relative w-full h-2 rounded-full bg-slate-200 overflow-hidden">
                          <div
                            className="absolute inset-y-0 left-0 bg-gradient-to-r from-primary to-blue-400 rounded-full transition-all duration-300 shadow-lg shadow-primary/50"
                            style={{ width: `${uploadProgress}%` }}
                          ></div>
                        </div>
                      </div>
                    )}

                    {/* Error Message */}
                    {error && (
                      <div className="mt-4 flex items-start gap-3 rounded-lg bg-red-50 border border-red-200 p-3">
                        <span className="material-symbols-outlined text-red-600 flex-shrink-0 text-lg">error</span>
                        <p className="text-xs text-red-700">{error}</p>
                      </div>
                    )}

                    {/* Success Message */}
                    {analysisSuccess && (
                      <div className="mt-4 flex items-start gap-3 rounded-lg bg-green-50 border border-green-200 p-3">
                        <span className="material-symbols-outlined text-green-600 flex-shrink-0 text-lg">check_circle</span>
                        <p className="text-xs text-green-700">Analysis complete! Redirecting to results...</p>
                      </div>
                    )}

                    {/* Analyze Button */}
                    <button
                      onClick={handleStartAnalysis}
                      disabled={!uploadedImage || !age || !bmi || !sugarBeforeFast || isAnalyzing || analysisSuccess}
                      className={`mt-6 w-full rounded-xl py-4 font-bold text-white shadow-lg transition-all duration-300 flex items-center justify-center gap-2 relative overflow-hidden group ${
                        isAnalyzing || analysisSuccess || !uploadedImage || !age || !bmi || !sugarBeforeFast
                          ? 'bg-slate-300 cursor-not-allowed'
                          : 'bg-gradient-to-r from-primary to-blue-500 hover:shadow-primary/50 hover:-translate-y-0.5 active:scale-95'
                      }`}
                    >
                      {isAnalyzing && (
                        <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
                      )}
                      <span className="relative flex items-center gap-2">
                        {analysisSuccess ? (
                          <>
                            <span className="material-symbols-outlined">check</span>
                            <span>Analysis Complete</span>
                          </>
                        ) : isAnalyzing ? (
                          <>
                            <span className="inline-block animate-spin">
                              <span className="material-symbols-outlined">hourglass_bottom</span>
                            </span>
                            <span>Analyzing Image...</span>
                          </>
                        ) : (
                          <>
                            <span className="material-symbols-outlined">search</span>
                            <span>Start Analysis</span>
                          </>
                        )}
                      </span>
                    </button>

                    <p className="mt-3 text-center text-xs text-slate-400">
                      By clicking "Start Analysis", you agree to our <a className="underline hover:text-primary transition-colors" href="#">Terms of Service</a>.
                    </p>
                  </div>

                  {/* Privacy Notice */}
                  <div className="rounded-xl border border-primary/20 bg-primary/5 p-4">
                    <div className="flex gap-3 text-primary">
                      <span className="material-symbols-outlined flex-shrink-0">shield</span>
                      <p className="text-xs font-medium leading-relaxed">
                        <strong>Privacy & Security:</strong> Your data is encrypted with 256-bit SSL. We comply with HIPAA regulations.
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile Navigation */}
      <nav className="lg:hidden fixed bottom-0 left-0 right-0 z-50 border-t border-slate-200 bg-white/90 backdrop-blur-md">
        <div className="flex items-center justify-around p-2 pb-6">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex flex-col items-center gap-1 p-2 text-slate-400 hover:text-slate-900 transition-colors"
          >
            <span className="material-symbols-outlined">home</span>
            <span className="text-[10px] font-bold">Home</span>
          </button>
          <button
            onClick={() => setActiveNav('scan')}
            className="flex flex-col items-center gap-1 p-2 text-primary"
          >
            <span className="material-symbols-outlined">camera</span>
            <span className="text-[10px] font-bold">Scan</span>
          </button>
          <button
            onClick={() => navigate('/history')}
            className="flex flex-col items-center gap-1 p-2 text-slate-400 hover:text-slate-900 transition-colors"
          >
            <span className="material-symbols-outlined">history</span>
            <span className="text-[10px] font-bold">History</span>
          </button>
          <button className="flex flex-col items-center gap-1 p-2 text-slate-400 hover:text-slate-900 transition-colors">
            <span className="material-symbols-outlined">person</span>
            <span className="text-[10px] font-bold">Profile</span>
          </button>
        </div>
      </nav>

      {/* Footer */}
      <footer className="lg:hidden border-t border-slate-200 bg-white py-12 px-4 mb-20">
        <div className="mx-auto max-w-7xl grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center gap-2 mb-4">
              <span className="material-symbols-outlined text-primary">health_metrics</span>
              <span className="text-lg font-bold">HealthScan AI</span>
            </div>
            <p className="text-slate-500 max-w-sm">
              Advanced podiatry analysis powered by artificial intelligence. Supporting your mobility through proactive screening.
            </p>
          </div>
          <div>
            <h5 className="font-bold mb-4 text-slate-900">Resources</h5>
            <ul className="space-y-2 text-sm text-slate-500">
              <li><a className="hover:text-primary transition-colors" href="#">Privacy Policy</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">How it Works</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Help Center</a></li>
            </ul>
          </div>
          <div>
            <h5 className="font-bold mb-4 text-slate-900">Support</h5>
            <ul className="space-y-2 text-sm text-slate-500">
              <li><a className="hover:text-primary transition-colors" href="#">Contact Us</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Feedback</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Accessibility</a></li>
            </ul>
          </div>
        </div>
        <div className="mx-auto max-w-7xl mt-12 pt-8 border-t border-slate-100 text-center text-xs text-slate-400">
          <p>© 2024 HealthScan AI. This tool is for screening purposes and not a substitute for professional medical advice.</p>
        </div>
      </footer>

      {error && (
        <div className="fixed bottom-32 left-4 right-4 max-w-sm mx-auto p-4 bg-red-100 border border-red-300 text-red-700 rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  )
}
