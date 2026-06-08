import React from 'react'
import { NavLink, Outlet } from 'react-router-dom'
import { Menu, X, LogOut } from 'lucide-react'
import { useAppStore } from '../stores/app'
import { supabase, hasSupabase } from '../lib/supabase'
import { Session } from '@supabase/supabase-js'
import Sidebar from './Sidebar'
import ThemeToggle from './ThemeToggle'
import toast from 'react-hot-toast'

interface LayoutProps {
  session?: Session | null
  onLogout?: () => void
}

const navItems = [
  { label: 'Chat', to: '/app/chat' },
  { label: 'Image Studio', to: '/app/images' },
]

export default function Layout({ session, onLogout }: LayoutProps) {
  const { sidebarOpen, toggleSidebar } = useAppStore()

  const handleLogout = async () => {
    if (hasSupabase && supabase?.auth) {
      await supabase.auth.signOut()
    } else {
      // Demo mode logout
      localStorage.removeItem('demo_user')
      onLogout?.()
    }
    toast.success('Logged out successfully')
  }

  return (
    <div className="flex h-screen bg-white dark:bg-darker-bg">
      {sidebarOpen && <Sidebar />}

      <div className="flex-1 flex flex-col overflow-hidden">
        <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center justify-between px-4 bg-white dark:bg-dark-bg gap-4">
          <div className="flex items-center gap-2">
            <button
              onClick={toggleSidebar}
              className="p-2 hover:bg-gray-100 dark:hover:bg-gray-700 rounded-lg transition-colors"
            >
              {sidebarOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
            <div className="flex items-center gap-3">
              <h1 className="gradient-text text-xl font-bold">SAKHA AI</h1>
              <nav className="hidden sm:flex gap-2">
                {navItems.map((item) => (
                  <NavLink
                    key={item.to}
                    to={item.to}
                    className={({ isActive }) =>
                      `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                        isActive
                          ? 'bg-primary text-white'
                          : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
                      }`
                    }
                  >
                    {item.label}
                  </NavLink>
                ))}
              </nav>
            </div>
          </div>

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

        <div className="flex-1 overflow-hidden">
          <Outlet />
        </div>
      </div>
    </div>
  )
}
