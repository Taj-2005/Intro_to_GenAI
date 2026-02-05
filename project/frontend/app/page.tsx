'use client'

import { useState, useEffect } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

interface AnalysisResult {
  prediction: string
  confidence: number
  reasons: string[]
}

interface Statistics {
  total_analyzed: number
  fake_count: number
  real_count: number
  fake_percentage: number
  real_percentage: number
  common_patterns: { pattern: string; count: number }[]
}

interface RecentJob {
  id: string
  job_title: string
  company_name: string
  prediction: string
  confidence: number
  analyzed_at: string
}

export default function Home() {
  const [jobTitle, setJobTitle] = useState('')
  const [companyName, setCompanyName] = useState('')
  const [salary, setSalary] = useState('')
  const [description, setDescription] = useState('')
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState<AnalysisResult | null>(null)
  const [error, setError] = useState('')
  const [statistics, setStatistics] = useState<Statistics | null>(null)
  const [recentJobs, setRecentJobs] = useState<RecentJob[]>([])
  const [activeTab, setActiveTab] = useState<'analyze' | 'history' | 'analytics'>('analyze')

  useEffect(() => {
    fetchStatistics()
    fetchRecentJobs()
  }, [])

  const fetchStatistics = async () => {
    try {
      const response = await axios.get(`${API_URL}/statistics`)
      setStatistics(response.data)
    } catch (error) {
      console.error('Error fetching statistics:', error)
    }
  }

  const fetchRecentJobs = async () => {
    try {
      const response = await axios.get(`${API_URL}/recent`)
      setRecentJobs(response.data.jobs || [])
    } catch (error) {
      console.error('Error fetching recent jobs:', error)
    }
  }

  const handleAnalyze = async () => {
    if (!description.trim()) {
      setError('Please enter a job description')
      return
    }

    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await axios.post(`${API_URL}/analyze`, {
        job_title: jobTitle,
        company_name: companyName,
        salary: salary,
        description: description,
        source: 'web_dashboard'
      })

      setResult(response.data)
      fetchStatistics()
      fetchRecentJobs()
    } catch (error: any) {
      setError(error.response?.data?.detail || 'Error analyzing job posting. Make sure the backend is running.')
    } finally {
      setLoading(false)
    }
  }

  const isFake = result?.prediction === 'FAKE'
  const trustScore = result ? (isFake ? 100 - result.confidence : result.confidence) : 0

  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-500 via-purple-600 to-indigo-700">
      <div className="container mx-auto px-4 py-8">
        <header className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🔍 Fake Job Posting Detector</h1>
          <p className="text-purple-100">AI-Powered Detection System</p>
        </header>

        {/* Tabs */}
        <div className="bg-white rounded-lg shadow-xl mb-6">
          <div className="flex border-b">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                activeTab === 'analyze'
                  ? 'text-purple-600 border-b-2 border-purple-600'
                  : 'text-gray-600 hover:text-purple-600'
              }`}
            >
              Analyze Job
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                activeTab === 'history'
                  ? 'text-purple-600 border-b-2 border-purple-600'
                  : 'text-gray-600 hover:text-purple-600'
              }`}
            >
              History
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`flex-1 px-6 py-4 font-semibold transition-colors ${
                activeTab === 'analytics'
                  ? 'text-purple-600 border-b-2 border-purple-600'
                  : 'text-gray-600 hover:text-purple-600'
              }`}
            >
              Analytics
            </button>
          </div>

          <div className="p-6">
            {/* Analyze Tab */}
            {activeTab === 'analyze' && (
              <div className="space-y-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Title (Optional)
                  </label>
                  <input
                    type="text"
                    value={jobTitle}
                    onChange={(e) => setJobTitle(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Software Engineer"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Company Name (Optional)
                  </label>
                  <input
                    type="text"
                    value={companyName}
                    onChange={(e) => setCompanyName(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., Tech Corp"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Salary (Optional)
                  </label>
                  <input
                    type="text"
                    value={salary}
                    onChange={(e) => setSalary(e.target.value)}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="e.g., $50k-$80k"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Job Description *
                  </label>
                  <textarea
                    value={description}
                    onChange={(e) => setDescription(e.target.value)}
                    rows={10}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-purple-500 focus:border-transparent"
                    placeholder="Paste the job description here..."
                  />
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg">
                    {error}
                  </div>
                )}

                <button
                  onClick={handleAnalyze}
                  disabled={loading}
                  className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-semibold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-indigo-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  {loading ? 'Analyzing...' : 'Analyze Job Posting'}
                </button>

                {result && (
                  <div className="mt-6 p-6 bg-gradient-to-r from-purple-50 to-indigo-50 rounded-lg border-2 border-purple-200">
                    <div className="text-center mb-6">
                      <div className={`inline-block px-6 py-3 rounded-full text-lg font-bold ${
                        isFake ? 'bg-red-100 text-red-700' : 'bg-green-100 text-green-700'
                      }`}>
                        {isFake ? '⚠️ High Risk Scam' : '✅ Likely Genuine'}
                      </div>
                      <div className="mt-4">
                        <div className="text-4xl font-bold text-purple-700">{trustScore}%</div>
                        <div className="text-sm text-gray-600">{isFake ? 'likely scam' : 'trust score'}</div>
                      </div>
                    </div>

                    <div>
                      <h3 className="font-semibold text-gray-800 mb-3">Key Reasons:</h3>
                      <ul className="space-y-2">
                        {result.reasons.map((reason, index) => (
                          <li key={index} className="flex items-start">
                            <span className="text-purple-600 mr-2">•</span>
                            <span className="text-gray-700">{reason}</span>
                          </li>
                        ))}
                      </ul>
                    </div>
                  </div>
                )}
              </div>
            )}

            {/* History Tab */}
            {activeTab === 'history' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-4">Recently Analyzed Jobs</h2>
                {recentJobs.length === 0 ? (
                  <p className="text-gray-500">No jobs analyzed yet.</p>
                ) : (
                  <div className="space-y-4">
                    {recentJobs.map((job) => (
                      <div
                        key={job.id}
                        className="p-4 border border-gray-200 rounded-lg hover:shadow-md transition-shadow"
                      >
                        <div className="flex justify-between items-start">
                          <div>
                            <h3 className="font-semibold text-gray-800">{job.job_title || 'Untitled'}</h3>
                            <p className="text-sm text-gray-600">{job.company_name || 'Unknown Company'}</p>
                            <p className="text-xs text-gray-500 mt-1">
                              {new Date(job.analyzed_at).toLocaleString()}
                            </p>
                          </div>
                          <div className="text-right">
                            <span
                              className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                                job.prediction === 'FAKE'
                                  ? 'bg-red-100 text-red-700'
                                  : 'bg-green-100 text-green-700'
                              }`}
                            >
                              {job.prediction}
                            </span>
                            <p className="text-xs text-gray-500 mt-1">{job.confidence}% confidence</p>
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {/* Analytics Tab */}
            {activeTab === 'analytics' && (
              <div>
                <h2 className="text-2xl font-bold text-gray-800 mb-6">Analytics Dashboard</h2>
                {statistics ? (
                  <div className="space-y-6">
                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                      <div className="bg-purple-50 p-6 rounded-lg border border-purple-200">
                        <div className="text-3xl font-bold text-purple-700">{statistics.total_analyzed}</div>
                        <div className="text-sm text-gray-600 mt-1">Total Analyzed</div>
                      </div>
                      <div className="bg-red-50 p-6 rounded-lg border border-red-200">
                        <div className="text-3xl font-bold text-red-700">{statistics.fake_count}</div>
                        <div className="text-sm text-gray-600 mt-1">Fake Jobs ({statistics.fake_percentage}%)</div>
                      </div>
                      <div className="bg-green-50 p-6 rounded-lg border border-green-200">
                        <div className="text-3xl font-bold text-green-700">{statistics.real_count}</div>
                        <div className="text-sm text-gray-600 mt-1">Real Jobs ({statistics.real_percentage}%)</div>
                      </div>
                    </div>

                    <div>
                      <h3 className="text-xl font-semibold text-gray-800 mb-4">Common Scam Patterns</h3>
                      {statistics.common_patterns.length > 0 ? (
                        <div className="space-y-2">
                          {statistics.common_patterns.map((pattern, index) => (
                            <div
                              key={index}
                              className="flex justify-between items-center p-3 bg-gray-50 rounded-lg"
                            >
                              <span className="text-gray-700">{pattern.pattern}</span>
                              <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                                {pattern.count}
                              </span>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <p className="text-gray-500">No patterns detected yet.</p>
                      )}
                    </div>
                  </div>
                ) : (
                  <p className="text-gray-500">Loading statistics...</p>
                )}
              </div>
            )}
          </div>
        </div>

        <footer className="text-center text-white text-sm mt-8">
          <p>⚠️ Predictions are AI-based and not legal verdicts. Always verify job postings independently.</p>
        </footer>
      </div>
    </div>
  )
}
