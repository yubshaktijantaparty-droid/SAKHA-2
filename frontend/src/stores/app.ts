import { create } from 'zustand'

interface AppStore {
  theme: 'light' | 'dark' | 'system'
  sidebarOpen: boolean
  selectedModel: string
  
  // Actions
  setTheme: (theme: 'light' | 'dark' | 'system') => void
  toggleSidebar: () => void
  setSelectedModel: (model: string) => void
}

export const useAppStore = create<AppStore>((set) => ({
  theme: 'dark',
  sidebarOpen: true,
  selectedModel: 'gpt-4o',

  setTheme: (theme) => set({ theme }),
  toggleSidebar: () => set((state) => ({ sidebarOpen: !state.sidebarOpen })),
  setSelectedModel: (model) => set({ selectedModel: model }),
}))
