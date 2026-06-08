/**
 * OpenRouter Service - Direct API calls to OpenRouter
 * No backend required - completely client-side
 * 
 * ✅ API keys are loaded from environment variables (.env file)
 * ✅ NO user configuration needed!
 * ✅ NO Settings page required!
 * ✅ Automatic key rotation for load balancing
 */

import axios from 'axios'

const OPENROUTER_BASE_URL = import.meta.env.VITE_OPENROUTER_BASE_URL || 'https://openrouter.ai/api/v1'

// Get all available API keys from environment variables ONLY
const getAvailableApiKeys = (): string[] => {
  const keys: string[] = []
  
  // Primary API key from environment
  const envKey = import.meta.env.VITE_OPENROUTER_API_KEY
  if (envKey && envKey.includes('sk-or-v1')) {
    keys.push(envKey)
  }
  
  // Additional API keys from environment (comma-separated)
  const envKeys = import.meta.env.VITE_OPENROUTER_API_KEYS
  if (envKeys && typeof envKeys === 'string' && envKeys.length > 0) {
    const additionalKeys = envKeys.split(',').map((k: string) => k.trim()).filter((k: string) => k.includes('sk-or-v1'))
    keys.push(...additionalKeys)
  }
  
  return [...new Set(keys)] // Remove duplicates
}

// Get next API key with automatic rotation for load balancing
let currentKeyIndex = 0
const getApiKey = (): string | null => {
  const keys = getAvailableApiKeys()
  if (keys.length === 0) {
    return null
  }
  
  // Rotate through keys automatically
  const key = keys[currentKeyIndex % keys.length]
  currentKeyIndex = (currentKeyIndex + 1) % keys.length
  return key
}

// Check if API keys are configured
export const hasApiKey = (): boolean => {
  return getAvailableApiKeys().length > 0
}

// OpenRouter models with nice names
const OPENROUTER_MODELS = [
  { id: 'openrouter/auto', name: '🤖 OpenRouter Auto (Best for each task)' },
  { id: 'meta-llama/llama-3-70b-instruct', name: 'Meta Llama 3 70B' },
  { id: 'meta-llama/llama-3-8b-instruct', name: 'Meta Llama 3 8B' },
  { id: 'mistralai/mistral-large', name: 'Mistral Large' },
  { id: 'mistralai/mistral-medium', name: 'Mistral Medium' },
  { id: 'mistralai/mistral-small', name: 'Mistral Small' },
  { id: 'google/gemini-2.0-flash-exp', name: 'Google Gemini 2.0 Flash' },
  { id: 'google/gemini-pro', name: 'Google Gemini Pro' },
  { id: 'openai/gpt-4o', name: 'OpenAI GPT-4o' },
  { id: 'openai/gpt-4-turbo', name: 'OpenAI GPT-4 Turbo' },
  { id: 'openai/gpt-3.5-turbo', name: 'OpenAI GPT-3.5 Turbo' },
  { id: 'anthropic/claude-3-opus', name: 'Anthropic Claude 3 Opus' },
  { id: 'anthropic/claude-3-sonnet', name: 'Anthropic Claude 3 Sonnet' },
  { id: 'anthropic/claude-3-haiku', name: 'Anthropic Claude 3 Haiku' },
  { id: 'deepseek/deepseek-chat', name: 'DeepSeek Chat' },
  { id: 'cohere/command', name: 'Cohere Command' },
  { id: 'aleph-alpha/luminous-supreme', name: 'Aleph Alpha Luminous' },
]

export const openRouterService = {
  /**
   * Send message to OpenRouter API
   */
  sendMessage: async (
    message: string,
    model: string = 'openrouter/auto',
    conversationHistory: Array<{ role: string; content: string }> = []
  ): Promise<string> => {
    const apiKey = getApiKey()
    
    if (!apiKey) {
      throw new Error('API key not set. Please configure your OpenRouter API key.')
    }

    try {
      const messages = [
        ...conversationHistory,
        { role: 'user', content: message }
      ]

      const response = await axios.post(
        `${OPENROUTER_BASE_URL}/chat/completions`,
        {
          model,
          messages,
          temperature: 0.7,
          top_p: 0.9,
          max_tokens: 2000,
        },
        {
          headers: {
            'Authorization': `Bearer ${apiKey}`,
            'HTTP-Referer': window.location.origin,
            'X-Title': 'SAKHA AI',
            'Content-Type': 'application/json',
          },
          timeout: 60000,
        }
      )

      return response.data.choices[0].message.content
    } catch (error: any) {
      // Handle specific OpenRouter errors
      if (error.response?.status === 401) {
        throw new Error('Invalid API key. Please check your OpenRouter API key.')
      }
      if (error.response?.status === 429) {
        throw new Error('Rate limit exceeded. Please wait a moment and try again.')
      }
      if (error.response?.status === 400) {
        throw new Error('Invalid request. Please check your input.')
      }
      throw new Error(`API Error: ${error.message}`)
    }
  },

  /**
   * Get available models
   */
  getAvailableModels: async () => {
    return {
      models: OPENROUTER_MODELS
    }
  },

  /**
   * List all available model IDs
   */
  getModelIds: () => {
    return OPENROUTER_MODELS.map(m => m.id)
  },

  /**
   * Get model by ID
   */
  getModel: (modelId: string) => {
    return OPENROUTER_MODELS.find(m => m.id === modelId)
  },
}

export default openRouterService
