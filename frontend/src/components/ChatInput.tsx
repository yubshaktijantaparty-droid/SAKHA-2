import React, { useState, useEffect } from 'react'
import { Send, Loader, Brain } from 'lucide-react'
import { chatAPI } from '../services/api'
import { useAppStore } from '../stores/app'

interface ChatInputProps {
  onSendMessage: (message: string, model: string, deepThinking?: boolean) => Promise<void>
  isLoading?: boolean
}

export default function ChatInput({ onSendMessage, isLoading }: ChatInputProps) {
  const [message, setMessage] = useState('')
  const [deepThinking, setDeepThinking] = useState(false)
  const { selectedModel, setSelectedModel } = useAppStore()

  const defaultModels = [
    { id: 'sakha-5.0', name: 'SAKHA-5.0 Unified AI' }
  ]

  const [models, setModels] = useState<any[]>(defaultModels)

  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await chatAPI.getAvailableModels()
        if (data.models && data.models.length > 0) {
          setModels(data.models)
          setSelectedModel('sakha-5.0')
        }
      } catch (error) {
        console.error('Failed to load models:', error)
        // Keep default Sakha-5.0 model
        setSelectedModel('sakha-5.0')
      }
    }

    fetchModels()
  }, [setSelectedModel])

  const handleSend = async () => {
    if (!message.trim() || isLoading) return

    await onSendMessage(message, selectedModel, deepThinking)
    setMessage('')
    setDeepThinking(false)  // Reset deep thinking after sending
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey && !isLoading) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-darker-bg p-4">
      {/* Model Selector & Deep Thinking */}
      <div className="mb-3 flex items-center gap-2">
        <label className="text-sm text-gray-600 dark:text-gray-400">Model:</label>
        <select
          value={selectedModel}
          onChange={(e) => setSelectedModel(e.target.value)}
          className="px-3 py-1 text-sm bg-gray-100 dark:bg-gray-700 rounded border border-gray-300 dark:border-gray-600 focus:outline-none"
        >
          {models.map((model) => (
            <option key={model.id} value={model.id}>
              {model.name}
            </option>
          ))}
        </select>
        
        {/* Deep Thinking Toggle */}
        <button
          onClick={() => setDeepThinking(!deepThinking)}
          disabled={isLoading}
          className={`px-3 py-1 text-sm rounded border transition-colors flex items-center gap-1 ${
            deepThinking
              ? 'bg-purple-600 text-white border-purple-600'
              : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border-gray-300 dark:border-gray-600 hover:bg-gray-200 dark:hover:bg-gray-600'
          } disabled:opacity-50`}
          title="Enable deep thinking for more thorough analysis"
        >
          <Brain size={16} />
          <span>Deep Thinking</span>
        </button>
      </div>

      {/* Input Area */}
      <div className="flex gap-3">
        <textarea
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Type your message... (Shift+Enter for new line)"
          disabled={isLoading}
          rows={3}
          maxLength={4000}
          className="flex-1 px-4 py-3 rounded-lg bg-gray-100 dark:bg-gray-700 border border-gray-300 dark:border-gray-600 focus:outline-none focus:border-primary disabled:opacity-50 resize-none"
        />

        <button
          onClick={handleSend}
          disabled={isLoading || !message.trim()}
          className="px-4 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors flex items-center gap-2"
        >
          {isLoading ? (
            <>
              <Loader size={18} className="animate-spin" />
              <span className="text-sm">Sending...</span>
            </>
          ) : (
            <Send size={18} />
          )}
        </button>
      </div>

      {/* Character Count */}
      <p className="text-xs text-gray-500 mt-2 text-right">
        {message.length} / 4000
      </p>
    </div>
  )
}
