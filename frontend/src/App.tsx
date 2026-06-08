import React, { useEffect, useState } from 'react'
import { HashRouter, Routes, Route, Navigate, useLocation, useNavigate } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { supabase, hasSupabase } from './lib/supabase'
import { Session } from '@supabase/supabase-js'
import Layout from './components/Layout'
import { Login } from './components/Login'
import LandingPage from './pages/LandingPage'
import ChatView from './components/ChatView'
import ImageGenerator from './pages/ImageGenerator'
import { useAppStore } from './stores/app'

function AppRoutes({ session, onLoginSuccess, onLogout }: {
  session: Session | any
  onLoginSuccess: () => void
  onLogout: () => void
}) {
  const location = useLocation()
  const navigate = useNavigate()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const redirect = params.get('redirect')

    if (redirect && location.pathname === '/') {
      navigate(redirect, { replace: true })
    }
  }, [location, navigate])

  return (
    <Routes>
      <Route path="/" element={session ? <Navigate to="/app/chat" replace /> : <LandingPage />} />
      <Route path="/login" element={session ? <Navigate to="/app/chat" replace /> : <Login onLoginSuccess={onLoginSuccess} />} />
      <Route
        path="/app"
        element={session ? <Layout session={session} onLogout={onLogout} /> : <Navigate to="/login" replace />}
      >
        <Route index element={<Navigate to="chat" replace />} />
        <Route path="chat" element={<ChatView />} />
        <Route path="images" element={<ImageGenerator />} />
      </Route>
      <Route path="*" element={<Navigate to={session ? '/app/chat' : '/login'} replace />} />
    </Routes>
  )
}

export default function App() {
  const [session, setSession] = useState<Session | any>(null)
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
    // Check for demo user in localStorage
    const checkDemoUser = () => {
      const demoUser = localStorage.getItem('demo_user')
      if (demoUser) {
        setSession(JSON.parse(demoUser) as any)
      } else {
        setSession(null)
      }
    }

    // Only check auth if Supabase is available
    if (!hasSupabase || !supabase?.auth) {
      // In demo mode, load demo user from localStorage
      checkDemoUser()
      setIsLoading(false)
      
      // Monitor localStorage changes for demo mode
      const handleStorageChange = (e: StorageEvent) => {
        if (e.key === 'demo_user') {
          checkDemoUser()
        }
      }
      window.addEventListener('storage', handleStorageChange)
      return () => window.removeEventListener('storage', handleStorageChange)
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

  const handleDemoLoginSuccess = () => {
    const demoUser = localStorage.getItem('demo_user')
    if (demoUser) {
      setSession(JSON.parse(demoUser) as Session)
    } else {
      setSession(null)
    }
  }

  const handleDemoLogout = () => {
    setSession(null)
  }

  return (
    <HashRouter>
      <div className="min-h-screen bg-white dark:bg-darker-bg text-slate-900 dark:text-slate-100">
        <Toaster position="bottom-right" />
        <AppRoutes session={session} onLoginSuccess={handleDemoLoginSuccess} onLogout={handleDemoLogout} />
      </div>
    </HashRouter>
  )
}
