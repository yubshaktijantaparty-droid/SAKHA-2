import React, { useState, useEffect } from 'react'
import { settingsAPI } from '../services/api'
import { openRouterService } from '../services/openrouter-service'

export default function Settings() {
  const [apiKey, setApiKey] = useState('')
  const [showApiKey, setShowApiKey] = useState(false)
  const [saved, setSaved] = useState(false)
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    // Load current API key on mount
    const settings = settingsAPI.getApiKey()
    if (settings.apiKey) {
      // Show only last 4 characters for security
      setApiKey(settings.apiKey.slice(-4))
    }
  }, [])

  const handleSaveApiKey = async () => {
    if (!apiKey.trim()) {
      setError('API key cannot be empty')
      return
    }

    setLoading(true)
    setError('')
    setSaved(false)

    try {
      // If they're pasting a full key
      if (apiKey.length > 4 && apiKey.includes('sk-')) {
        settingsAPI.setApiKey(apiKey)
        setSaved(true)
        setApiKey(apiKey.slice(-4))
      } else if (apiKey.length === 4) {
        // They're using the partial key (already saved)
        setSaved(true)
      } else {
        setError('Invalid API key format. Please enter your full OpenRouter API key (sk-...)')
      }
    } catch (err) {
      setError('Failed to save API key')
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteApiKey = () => {
    if (window.confirm('Are you sure you want to delete your API key? This cannot be undone.')) {
      settingsAPI.deleteApiKey()
      setApiKey('')
      setSaved(false)
      setError('')
    }
  }

  return (
    <div className="flex-1 overflow-auto bg-white dark:bg-gray-950 p-4 sm:p-6">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            ⚙️ Settings
          </h1>
          <p className="text-gray-600 dark:text-gray-400">
            Configure SAKHA AI to work completely on GitHub Pages
          </p>
        </div>

        {/* API Key Configuration */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 mb-6 border border-gray-200 dark:border-gray-800">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            🔑 OpenRouter API Key
          </h2>
          
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            SAKHA AI uses OpenRouter to provide real AI responses. To get started:
          </p>

          <ol className="list-decimal list-inside text-sm text-gray-600 dark:text-gray-400 mb-6 space-y-2">
            <li>Go to <a 
              href="https://openrouter.ai" 
              target="_blank" 
              rel="noopener noreferrer"
              className="text-blue-600 dark:text-blue-400 hover:underline"
            >
              openrouter.ai
            </a></li>
            <li>Sign up for a free account</li>
            <li>Go to your dashboard → API keys</li>
            <li>Copy your API key (starts with "sk-")</li>
            <li>Paste it below</li>
          </ol>

          {/* API Key Input */}
          <div className="space-y-4">
            <div className="relative">
              <input
                type={showApiKey ? 'text' : 'password'}
                value={apiKey}
                onChange={(e) => {
                  setApiKey(e.target.value)
                  setSaved(false)
                  setError('')
                }}
                placeholder="sk-... (paste your full OpenRouter API key)"
                className="w-full px-4 py-2 border border-gray-300 dark:border-gray-700 rounded-lg bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                type="button"
                onClick={() => setShowApiKey(!showApiKey)}
                className="absolute right-3 top-2.5 text-gray-600 dark:text-gray-400 hover:text-gray-900 dark:hover:text-white"
              >
                {showApiKey ? '🙈 Hide' : '👁️ Show'}
              </button>
            </div>

            {/* Error Message */}
            {error && (
              <div className="p-3 bg-red-100 dark:bg-red-900 text-red-800 dark:text-red-200 rounded-lg">
                ❌ {error}
              </div>
            )}

            {/* Success Message */}
            {saved && (
              <div className="p-3 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 rounded-lg">
                ✅ API key saved successfully!
              </div>
            )}

            {/* Buttons */}
            <div className="flex gap-2">
              <button
                onClick={handleSaveApiKey}
                disabled={loading}
                className="flex-1 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed transition"
              >
                {loading ? '⏳ Saving...' : '💾 Save API Key'}
              </button>
              {apiKey && (
                <button
                  onClick={handleDeleteApiKey}
                  className="px-4 py-2 bg-red-600 hover:bg-red-700 text-white rounded-lg font-medium transition"
                >
                  🗑️ Delete
                </button>
              )}
            </div>
          </div>
        </div>

        {/* Available Models */}
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-6 border border-gray-200 dark:border-gray-800">
          <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-4">
            🤖 Available AI Models
          </h2>
          <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
            Once you add your API key, these models will be available in the chat:
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            {[
              '🤖 OpenRouter Auto',
              '🦙 Meta Llama 3 70B',
              '🌀 Mistral Large',
              '✨ Google Gemini 2.0',
              '🔗 OpenAI GPT-4o',
              '🧠 Claude 3 Opus',
              '⚡ DeepSeek Chat',
              '🎯 Cohere Command',
            ].map((model) => (
              <div
                key={model}
                className="p-3 bg-white dark:bg-gray-800 rounded border border-gray-200 dark:border-gray-700 text-sm text-gray-700 dark:text-gray-300"
              >
                {model}
              </div>
            ))}
          </div>
        </div>

        {/* Information Box */}
        <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-lg">
          <p className="text-sm text-blue-800 dark:text-blue-300">
            <strong>💡 About This Setup:</strong> Your API key is stored locally in your browser. 
            It's <strong>never</strong> sent to our servers - all AI requests go directly from your browser to OpenRouter.
            This means your data and API key stay completely private!
          </p>
        </div>
      </div>
    </div>
  )
}
