import React from 'react'
import { Menu, X } from 'lucide-react'
import { useAppStore } from '../stores/app'
import Sidebar from './Sidebar'
import ChatView from './ChatView'
import ThemeToggle from './ThemeToggle'

export default function Layout() {
  const { sidebarOpen, toggleSidebar } = useAppStore()

  return (
    <div className="flex h-screen bg-white dark:bg-darker-bg">
      {/* Sidebar */}
      {sidebarOpen && <Sidebar />}

      {/* Main Content */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-4 bg-white dark:bg-dark-bg">
          <button
            onClick={toggleSidebar}
            className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
          >
            {sidebarOpen ? (
              <X size={20} />
            ) : (
              <Menu size={20} />
            )}
          </button>
          <h1 className="gradient-text text-xl font-bold">SAKHA AI</h1>
          <ThemeToggle />
        </div>

        {/* Chat Area */}
        <ChatView />
      </div>
    </div>
  )
}
