import axios from 'axios'
import { openRouterService, hasApiKey } from './openrouter-service'

/**
 * SAKHA AI API Service - Completely GitHub Dependent
 * 
 * This service:
 * 1. Uses OpenRouter API directly (no backend server needed)
 * 2. Stores chat history in localStorage
 * 3. Runs completely on GitHub Pages
 * 4. No dependencies on Railway or any external servers
 * 5. API Keys loaded from environment variables (NO USER CONFIG NEEDED)
 */

// Chat API - Uses OpenRouter directly
export const chatAPI = {
  /**
   * Send a message and get AI response
   * Calls OpenRouter API directly from the browser
   * No configuration needed - uses API keys from .env
   */
  sendMessage: async (
    message: string,
    model: string = 'openrouter/auto',
    deepThinking?: boolean,
    conversationHistory: Array<{ role: string; content: string }> = []
  ) => {
    try {
      // Check if API keys are configured from environment variables
      if (!hasApiKey()) {
        return {
          message: '❌ No OpenRouter API key found. Add VITE_OPENROUTER_API_KEY to frontend/.env file and rebuild.',
          model,
          error: true,
          isConfigurationError: true,
        }
      }

      // Get response directly from OpenRouter
      const aiResponse = await openRouterService.sendMessage(
        message,
        model,
        conversationHistory
      )

      return {
        message: aiResponse,
        model,
        timestamp: new Date().toISOString(),
      }
    } catch (error: any) {
      console.error('Chat error:', error)
      return {
        message: error.message || 'Failed to get AI response. Please try again.',
        model,
        error: true,
        isConfigurationError: error.message?.includes('API key'),
      }
    }
  },

  /**
   * Get available AI models from OpenRouter
   */
  getAvailableModels: async () => {
    try {
      const models = await openRouterService.getAvailableModels()
      return models
    } catch (error) {
      console.error('Failed to fetch models:', error)
      // Return a default model list
      return {
        models: [
          { id: 'openrouter/auto', name: '🤖 OpenRouter Auto (Best for each task)' },
          { id: 'meta-llama/llama-3-70b-instruct', name: 'Meta Llama 3 70B' },
          { id: 'mistralai/mistral-large', name: 'Mistral Large' },
          { id: 'google/gemini-pro', name: 'Google Gemini Pro' },
          { id: 'openai/gpt-4o', name: 'OpenAI GPT-4o' },
        ]
      }
    }
  },

  /**
   * Get chat history from localStorage
   */
  getChatHistory: async (chatId: string) => {
    try {
      const history = localStorage.getItem(`chat_${chatId}`)
      if (history) {
        return JSON.parse(history)
      }
      return { messages: [] }
    } catch (error) {
      return { messages: [] }
    }
  },

  /**
   * Save chat history to localStorage
   */
  saveChatHistory: async (chatId: string, messages: any[]) => {
    try {
      localStorage.setItem(`chat_${chatId}`, JSON.stringify({ messages }))
      return { success: true }
    } catch (error) {
      console.error('Failed to save chat:', error)
      return { success: false }
    }
  },

  /**
   * Delete chat from localStorage
   */
  deleteChat: async (chatId: string) => {
    try {
      localStorage.removeItem(`chat_${chatId}`)
      return { success: true }
    } catch (error) {
      console.error('Failed to delete chat:', error)
      return { success: false }
    }
  },
}

export const imageAPI = {
  generateImage: async (prompt: string, style?: string) => {
    try {
      return {
        images: [
          {
            url: `https://picsum.photos/512/512?random=${Date.now()}&t=${encodeURIComponent(prompt)}`,
            prompt,
            style: style || 'realistic',
            timestamp: new Date().toISOString(),
          }
        ]
      }
    } catch (error) {
      return {
        images: [
          {
            url: `https://picsum.photos/512/512?random=${Date.now()}`,
            prompt,
            style: style || 'realistic',
          }
        ],
        demo: true,
      }
    }
  },

  getStyles: async () => {
    return {
      styles: [
        { id: 'realistic', name: 'Realistic' },
        { id: 'anime', name: 'Anime' },
        { id: 'oil-painting', name: 'Oil Painting' },
        { id: 'watercolor', name: 'Watercolor' },
        { id: 'digital-art', name: 'Digital Art' },
        { id: 'cyberpunk', name: 'Cyberpunk' },
        { id: 'steampunk', name: 'Steampunk' },
        { id: 'abstract', name: 'Abstract' },
      ]
    }
  },

  getHistory: async (userId: string) => {
    try {
      const history = localStorage.getItem(`images_${userId}`)
      if (history) {
        return JSON.parse(history)
      }
      return { images: [] }
    } catch (error) {
      return { images: [] }
    }
  },
}

export const fileAPI = {
  uploadFile: async (file: File) => {
    try {
      const reader = new FileReader()
      return new Promise((resolve) => {
        reader.onload = (e) => {
          const fileData = {
            file_id: 'file_' + Date.now(),
            name: file.name,
            size: file.size,
            type: file.type,
          }
          try {
            localStorage.setItem(`file_${fileData.file_id}`, JSON.stringify(fileData))
          } catch (error) {
            console.warn('File too large for localStorage')
          }
          resolve(fileData)
        }
        reader.readAsDataURL(file)
      })
    } catch (error) {
      return { file_id: 'file_' + Date.now(), name: file.name, demo: true }
    }
  },

  analyzeFile: async (fileId: string, action: string, question?: string) => {
    try {
      return { result: 'File analysis is available through AI chat. Ask the AI assistant about your file contents.', demo: true }
    } catch (error) {
      return { result: 'Please use the AI chat to analyze file contents.', demo: true }
    }
  },

  getSupportedTypes: async () => {
    return { types: ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'csv', 'jpg', 'png'] }
  },
}

// Settings API - localStorage based
export const settingsAPI = {
  setApiKey: (key: string) => {
    localStorage.setItem('openrouter_api_key', key)
    return { success: true }
  },

  getApiKey: () => {
    return {
      apiKey: localStorage.getItem('openrouter_api_key') || '',
    }
  },

  deleteApiKey: () => {
    localStorage.removeItem('openrouter_api_key')
    return { success: true }
  },

  getSettings: () => {
    const settings = localStorage.getItem('sakha_settings')
    if (settings) {
      return JSON.parse(settings)
    }
    return {
      theme: 'dark',
      language: 'en',
      autoSave: true,
    }
  },

  updateSettings: (settings: any) => {
    localStorage.setItem('sakha_settings', JSON.stringify(settings))
    return { success: true }
  },
}

export default {
  chatAPI,
  imageAPI,
  fileAPI,
  settingsAPI,
}
