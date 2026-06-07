import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { supabase, hasSupabase } from './lib/supabase'
import { Session } from '@supabase/supabase-js'
import Layout from './components/Layout'
import { Login } from './components/Login'
import LandingPage from './pages/LandingPage'
import ChatView from './components/ChatView'
import ImageGenerator from './pages/ImageGenerator'
import { useAppStore } from './stores/app'

export default function App() {
  const [session, setSession] = useState<Session | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const theme = useAppStore((state) => state.theme)

  useEffect(() => {
    const root = document.documentElement
    const updateTheme = () => {
      if (theme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        root.classList.toggle('dark', prefersDark)
      } else {
        root.classList.toggle('dark', theme === 'dark')
      }
    }

    updateTheme()
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    mediaQuery.addEventListener?.('change', updateTheme)

    return () => mediaQuery.removeEventListener?.('change', updateTheme)
  }, [theme])

  useEffect(() => {
    // Only check auth if Supabase is available
    if (!hasSupabase || !supabase?.auth) {
      // In demo mode, load demo user from localStorage
      const demoUser = localStorage.getItem('demo_user')
      if (demoUser) {
        // Create a mock session for demo mode
        setSession(JSON.parse(demoUser) as any)
      }
      setIsLoading(false)
      return
    }

    // Real Supabase auth check
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session)
      setIsLoading(false)
    })

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session)
    })

    return () => subscription?.unsubscribe()
  }, [])

  if (isLoading) {
    return (
      <div className="w-full min-h-screen flex items-center justify-center bg-slate-950 text-white">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-emerald-500 mx-auto mb-4"></div>
          <p className="text-slate-300">Loading SAKHA AI...</p>
        </div>
      </div>
    )
  }

  return (
    <BrowserRouter>
      <div className="min-h-screen bg-white dark:bg-darker-bg text-slate-900 dark:text-slate-100">
        <Toaster position="bottom-right" />
        <Routes>
          <Route path="/" element={session ? <Navigate to="/app/chat" replace /> : <LandingPage />} />
          <Route path="/login" element={session ? <Navigate to="/app/chat" replace /> : <Login onLoginSuccess={() => {}} />} />
          <Route
            path="/app"
            element={session ? <Layout session={session} /> : <Navigate to="/login" replace />}
          >
            <Route index element={<Navigate to="chat" replace />} />
            <Route path="chat" element={<ChatView />} />
            <Route path="images" element={<ImageGenerator />} />
          </Route>
          <Route path="*" element={<Navigate to={session ? '/app/chat' : '/login'} replace />} />
        </Routes>
      </div>
    </BrowserRouter>
  )
}
