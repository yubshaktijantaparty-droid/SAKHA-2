import { create } from 'zustand'
import { persist } from 'zustand/middleware'

export interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  model?: string
  tokens_used?: number
  timestamp: Date
  edited_content?: string
  edited_at?: Date
}

export interface Chat {
  id: string
  title: string
  messages: Message[]
  model: string
  temperature: number
  max_tokens: number
  createdAt: Date
  updatedAt: Date
  is_archived?: boolean
  is_pinned?: boolean
  tags?: string[]
  folder?: string
}

interface ChatStore {
  chats: Chat[]
  currentChatId: string | null
  currentChat: Chat | null
  isLoading: boolean
  error: string | null
  
  // Actions
  createChat: (title?: string) => string
  deleteChat: (id: string) => void
  selectChat: (id: string) => void
  addMessage: (chatId: string, message: Message) => void
  renameChat: (id: string, title: string) => void
  updateChatModel: (chatId: string, model: string) => void
  updateChatTemperature: (chatId: string, temperature: number) => void
  updateChatMaxTokens: (chatId: string, maxTokens: number) => void
  editMessage: (chatId: string, messageId: string, newContent: string) => void
  deleteMessage: (chatId: string, messageId: string) => void
  archiveChat: (id: string) => void
  pinChat: (id: string) => void
  addTagToChat: (chatId: string, tag: string) => void
  clearCurrentChat: () => void
  setLoading: (loading: boolean) => void
  setError: (error: string | null) => void
}

export const useChatStore = create<ChatStore>()(
  persist(
    (set, get) => ({
      chats: [],
      currentChatId: null,
      currentChat: null,
      isLoading: false,
      error: null,

      createChat: (title = 'New Chat') => {
        const newChat: Chat = {
          id: Date.now().toString(),
          title,
          messages: [],
          model: 'gpt-4o',
          temperature: 0.7,
          max_tokens: 2048,
          createdAt: new Date(),
          updatedAt: new Date(),
          is_archived: false,
          is_pinned: false,
          tags: [],
          folder: undefined,
        }
        set((state) => ({
          chats: [newChat, ...state.chats],
          currentChatId: newChat.id,
          currentChat: newChat,
        }))
        return newChat.id
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
            chat.id === id ? { ...chat, title, updatedAt: new Date() } : chat
          ),
          currentChat:
            state.currentChat?.id === id
              ? { ...state.currentChat, title, updatedAt: new Date() }
              : state.currentChat,
        }))
      },

      updateChatModel: (chatId, model) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId ? { ...chat, model } : chat
          ),
          currentChat:
            state.currentChat?.id === chatId
              ? { ...state.currentChat, model }
              : state.currentChat,
        }))
      },

      updateChatTemperature: (chatId, temperature) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId ? { ...chat, temperature } : chat
          ),
          currentChat:
            state.currentChat?.id === chatId
              ? { ...state.currentChat, temperature }
              : state.currentChat,
        }))
      },

      updateChatMaxTokens: (chatId, maxTokens) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId ? { ...chat, max_tokens: maxTokens } : chat
          ),
          currentChat:
            state.currentChat?.id === chatId
              ? { ...state.currentChat, max_tokens: maxTokens }
              : state.currentChat,
        }))
      },

      editMessage: (chatId, messageId, newContent) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId
              ? {
                  ...chat,
                  messages: chat.messages.map((msg) =>
                    msg.id === messageId
                      ? {
                          ...msg,
                          edited_content: newContent,
                          edited_at: new Date(),
                        }
                      : msg
                  ),
                }
              : chat
          ),
          currentChat:
            state.currentChat?.id === chatId
              ? {
                  ...state.currentChat,
                  messages: state.currentChat.messages.map((msg) =>
                    msg.id === messageId
                      ? {
                          ...msg,
                          edited_content: newContent,
                          edited_at: new Date(),
                        }
                      : msg
                  ),
                }
              : state.currentChat,
        }))
      },

      deleteMessage: (chatId, messageId) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId
              ? {
                  ...chat,
                  messages: chat.messages.filter((msg) => msg.id !== messageId),
                }
              : chat
          ),
          currentChat:
            state.currentChat?.id === chatId
              ? {
                  ...state.currentChat,
                  messages: state.currentChat.messages.filter(
                    (msg) => msg.id !== messageId
                  ),
                }
              : state.currentChat,
        }))
      },

      archiveChat: (id) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === id ? { ...chat, is_archived: true } : chat
          ),
        }))
      },

      pinChat: (id) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === id ? { ...chat, is_pinned: !chat.is_pinned } : chat
          ),
        }))
      },

      addTagToChat: (chatId, tag) => {
        set((state) => ({
          chats: state.chats.map((chat) =>
            chat.id === chatId
              ? {
                  ...chat,
                  tags: chat.tags?.includes(tag) ? chat.tags : [...(chat.tags || []), tag],
                }
              : chat
          ),
        }))
      },

      clearCurrentChat: () => {
        set({ currentChatId: null, currentChat: null })
      },

      setLoading: (loading) => {
        set({ isLoading: loading })
      },

      setError: (error) => {
        set({ error })
      },
    }),
    {
      name: 'chat-store',
    }
  )
)
