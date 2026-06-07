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

export const chatAPI = {
  sendMessage: async (message: string, model?: string) => {
    const response = await api.post('/chat', {
      message,
      model: model || 'openai',
    })
    return response.data
  },

  streamMessage: async (message: string, model?: string) => {
    const response = await api.post('/chat/stream', {
      message,
      model: model || 'openai',
    }, {
      responseType: 'stream',
    })
    return response.data
  },

  getAvailableModels: async () => {
    const response = await api.get('/chat/models')
    return response.data
  },

  getChatHistory: async (chatId: string) => {
    const response = await api.get(`/chat/history/${chatId}`)
    return response.data
  },

  deleteChat: async (chatId: string) => {
    const response = await api.post(`/chat/${chatId}/delete`)
    return response.data
  },
}

export const imageAPI = {
  generateImage: async (prompt: string, style?: string) => {
    const response = await api.post('/images/generate', {
      prompt,
      style: style || 'realistic',
    })
    return response.data
  },

  getStyles: async () => {
    const response = await api.get('/images/styles')
    return response.data
  },

  getHistory: async (userId: string) => {
    const response = await api.get(`/images/history/${userId}`)
    return response.data
  },
}

export const fileAPI = {
  uploadFile: async (file: File) => {
    const formData = new FormData()
    formData.append('file', file)

    const response = await api.post('/files/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    })
    return response.data
  },

  analyzeFile: async (fileId: string, action: string, question?: string) => {
    const response = await api.post(`/files/${fileId}/analyze`, {
      action,
      question,
    })
    return response.data
  },

  getSupportedTypes: async () => {
    const response = await api.get('/files/supported')
    return response.data
  },
}

export default api
