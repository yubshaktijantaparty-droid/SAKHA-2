import React from 'react'
import { Menu, X, LogOut } from 'lucide-react'
import { useAppStore } from '../stores/app'
import { supabase } from '../lib/supabase'
import { Session } from '@supabase/supabase-js'
import Sidebar from './Sidebar'
import ChatView from './ChatView'
import ThemeToggle from './ThemeToggle'
import toast from 'react-hot-toast'

interface LayoutProps {
  session?: Session | null
}

export default function Layout({ session }: LayoutProps) {
  const { sidebarOpen, toggleSidebar } = useAppStore()

  const handleLogout = async () => {
    await supabase.auth.signOut()
    toast.success('Logged out successfully')
  }

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
          <div className="flex items-center gap-3">
            <ThemeToggle />
            {session && (
              <div className="flex items-center gap-2">
                <span className="text-sm text-gray-600 dark:text-gray-400 truncate max-w-[150px]">
                  {session.user?.email}
                </span>
                <button
                  onClick={handleLogout}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors text-red-500 hover:text-red-600"
                  title="Logout"
                >
                  <LogOut size={20} />
                </button>
              </div>
            )}
          </div>
        </div>

        {/* Chat Area */}
        <ChatView />
      </div>
    </div>
  )
}
