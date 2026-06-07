import axios from 'axios'

// Support both relative and absolute API URLs
const getAPIBaseURL = () => {
  const apiUrl = import.meta.env.VITE_API_URL
  if (apiUrl && apiUrl.startsWith('http')) {
    return `${apiUrl}/api`
  }
  return '/api'
}

const API_BASE_URL = getAPIBaseURL()

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
})

// Demo mode responses for when backend is unavailable
const demoResponses: { [key: string]: string } = {
  'what is biochemistry': 'Biochemistry is the study of chemical processes occurring within living organisms. It focuses on the structure and function of biological molecules like proteins, nucleic acids, carbohydrates, and lipids. Key areas include metabolism, enzyme kinetics, and cellular signaling.',
  'hi': 'Hello! I\'m SAKHA AI, your premium AI assistant. How can I help you today? Feel free to ask me questions, brainstorm ideas, or discuss any topic.',
  'hello': 'Hi there! Welcome to SAKHA AI. I\'m here to help with any questions or tasks you have. What would you like to know?',
  'how are you': 'I\'m doing great, thanks for asking! I\'m ready to help you with any questions or tasks. What can I assist you with?',
  'help': 'I\'m SAKHA AI, your personal AI assistant! I can help you with: answering questions, writing content, coding, analysis, brainstorming, and much more. Just ask me anything!',
  'default': 'That\'s an interesting question! Based on my knowledge, I can provide insights on this topic. Could you provide more context or ask a more specific question so I can give you a better answer?',
}

const getDemoResponse = (message: string): string => {
  const lowerMessage = message.toLowerCase().trim()
  
  // Check for exact or partial matches
  for (const [key, value] of Object.entries(demoResponses)) {
    if (lowerMessage.includes(key) || key.includes(lowerMessage)) {
      return value
    }
  }
  
  return demoResponses['default']
}

const isInDemoMode = (): boolean => {
  return localStorage.getItem('demo_user') !== null
}

export const chatAPI = {
  sendMessage: async (message: string, model?: string, deepThinking?: boolean) => {
    try {
      const response = await api.post('/chat', {
        message,
        model: model || 'sakha-5.0',
        deep_thinking: deepThinking || false,
      })
      return response.data
    } catch (error) {
      // If backend fails and we're in demo mode, return mock response
      if (isInDemoMode()) {
        return {
          message: getDemoResponse(message),
          model: 'sakha-5.0',
          demo: true,
        }
      }
      throw error
    }
  },

  streamMessage: async (message: string, model?: string) => {
    try {
      const response = await api.post('/chat/stream', {
        message,
        model: model || 'sakha-5.0',
      }, {
        responseType: 'stream',
      })
      return response.data
    } catch (error) {
      // If backend fails and we're in demo mode, return mock response
      if (isInDemoMode()) {
        return {
          message: getDemoResponse(message),
          model: 'sakha-5.0',
          demo: true,
        }
      }
      throw error
    }
  },

  getAvailableModels: async () => {
    try {
      const response = await api.get('/chat/models')
      return response.data
    } catch (error) {
      // Return Sakha-5.0 as default if backend fails
      return {
        models: [
          { id: 'sakha-5.0', name: 'SAKHA-5.0 Unified AI' },
        ]
      }
    }
  },

  getChatHistory: async (chatId: string) => {
    try {
      const response = await api.get(`/chat/history/${chatId}`)
      return response.data
    } catch (error) {
      return { messages: [] }
    }
  },

  deleteChat: async (chatId: string) => {
    try {
      const response = await api.post(`/chat/${chatId}/delete`)
      return response.data
    } catch (error) {
      return { success: true }
    }
  },
}

export const imageAPI = {
  generateImage: async (prompt: string, style?: string) => {
    try {
      const response = await api.post('/images/generate', {
        prompt,
        style: style || 'realistic',
      })
      return response.data
    } catch (error) {
      // Return demo image if backend fails
      return {
        images: [
          {
            url: `https://picsum.photos/512/512?random=${Date.now()}`,
            prompt,
            style: style || 'realistic'
          }
        ],
        demo: true,
      }
    }
  },

  getStyles: async () => {
    try {
      const response = await api.get('/images/styles')
      return response.data
    } catch (error) {
      // Return default styles if backend fails
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
    }
  },

  getHistory: async (userId: string) => {
    try {
      const response = await api.get(`/images/history/${userId}`)
      return response.data
    } catch (error) {
      return { images: [] }
    }
  },
}

export const fileAPI = {
  uploadFile: async (file: File) => {
    try {
      const formData = new FormData()
      formData.append('file', file)

      const response = await api.post('/files/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      return response.data
    } catch (error) {
      return { file_id: 'demo_' + Date.now(), name: file.name, demo: true }
    }
  },

  analyzeFile: async (fileId: string, action: string, question?: string) => {
    try {
      const response = await api.post(`/files/${fileId}/analyze`, {
        action,
        question,
      })
      return response.data
    } catch (error) {
      return { result: 'File analysis feature is in demo mode. Real analysis requires backend access.', demo: true }
    }
  },

  getSupportedTypes: async () => {
    try {
      const response = await api.get('/files/supported')
      return response.data
    } catch (error) {
      return { types: ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'csv'] }
    }
  },
}

export default api
