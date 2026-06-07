import { create } from 'zustand'

export interface Chat {
  id: string
  title: string
  messages: Message[]
  createdAt: Date
  updatedAt: Date
}

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

interface ChatStore {
  chats: Chat[]
  currentChatId: string | null
  currentChat: Chat | null
  
  // Actions
  createChat: (title?: string) => void
  deleteChat: (id: string) => void
  selectChat: (id: string) => void
  addMessage: (chatId: string, message: Message) => void
  renameChat: (id: string, title: string) => void
}

export const useChatStore = create<ChatStore>((set, get) => ({
  chats: [],
  currentChatId: null,
  currentChat: null,

  createChat: (title = 'New Chat') => {
    const newChat: Chat = {
      id: Date.now().toString(),
      title,
      messages: [],
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    set((state) => ({
      chats: [newChat, ...state.chats],
      currentChatId: newChat.id,
      currentChat: newChat,
    }))
  },

  deleteChat: (id) => {
    set((state) => ({
      chats: state.chats.filter((chat) => chat.id !== id),
      currentChatId: state.currentChatId === id ? null : state.currentChatId,
      currentChat: state.currentChat?.id === id ? null : state.currentChat,
    }))
  },

  selectChat: (id) => {
    set((state) => ({
      currentChatId: id,
      currentChat: state.chats.find((chat) => chat.id === id) || null,
    }))
  },

  addMessage: (chatId, message) => {
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === chatId
          ? {
              ...chat,
              messages: [...chat.messages, message],
              updatedAt: new Date(),
            }
          : chat
      ),
      currentChat:
        state.currentChat?.id === chatId
          ? {
              ...state.currentChat,
              messages: [...state.currentChat.messages, message],
              updatedAt: new Date(),
            }
          : state.currentChat,
    }))
  },

  renameChat: (id, title) => {
    set((state) => ({
      chats: state.chats.map((chat) =>
        chat.id === id ? { ...chat, title } : chat
      ),
      currentChat:
        state.currentChat?.id === id
          ? { ...state.currentChat, title }
          : state.currentChat,
    }))
  },
}))
