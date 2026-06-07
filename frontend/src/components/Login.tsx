import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { supabase, hasSupabase } from '../lib/supabase'
import { Mail, Lock, Loader, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'

interface LoginProps {
  onLoginSuccess?: () => void
}

export function Login({ onLoginSuccess }: LoginProps) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [isSignUp, setIsSignUp] = useState(false)

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault()
    setIsLoading(true)

    try {
      if (!email || !password) {
        throw new Error('Please enter email and password')
      }
      
      if (password.length < 6) {
        throw new Error('Password must be at least 6 characters')
      }

      // Use demo authentication if Supabase is not available
      if (!hasSupabase) {
        // Demo mode - accept any valid credentials
        if (isSignUp) {
          localStorage.setItem('demo_user', JSON.stringify({ email, type: 'signup' }))
          toast.success('Account created successfully!')
        } else {
          localStorage.setItem('demo_user', JSON.stringify({ email, type: 'signin' }))
          toast.success('Logged in successfully!')
        }
        
        // Navigate after showing toast
        setTimeout(() => {
          onLoginSuccess?.()
          navigate('/app/chat', { replace: true })
        }, 300)
        return
      }

      // Real Supabase authentication
      if (!supabase) {
        throw new Error('Authentication service not available')
      }

      if (isSignUp) {
        const { error } = await supabase.auth.signUp({
          email,
          password,
        })
        if (error) throw error
        toast.success('Account created! Check your email to verify.')
      } else {
        const { error } = await supabase.auth.signInWithPassword({
          email,
          password,
        })
        if (error) throw error
        toast.success('Logged in successfully!')
      }
      
      // Navigate after showing toast
      setTimeout(() => {
        onLoginSuccess?.()
        navigate('/app/chat', { replace: true })
      }, 300)
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Authentication failed'
      toast.error(message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 flex items-center justify-center p-4">
      <div className="w-full max-w-md">
        <div className="bg-slate-800 rounded-lg shadow-2xl p-8 border border-slate-700">
          <div className="text-center mb-8">
            <h1 className="text-3xl font-bold text-white mb-2">SAKHA AI</h1>
            <p className="text-slate-400">{isSignUp ? 'Create Account' : 'Welcome Back'}</p>
          </div>

          {!hasSupabase && (
            <div className="mb-6 bg-blue-900/30 border border-blue-700 rounded-lg p-4 flex gap-3">
              <AlertCircle className="w-5 h-5 text-blue-400 flex-shrink-0 mt-0.5" />
              <div className="text-sm text-blue-200">
                <p className="font-semibold mb-1">Demo Mode</p>
                <p>Enter any email and password (6+ chars) to test the application.</p>
              </div>
            </div>
          )}

          <form onSubmit={handleAuth} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Email Address
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@example.com"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg py-2 pl-10 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                  required
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-300 mb-2">
                Password
              </label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 w-5 h-5 text-slate-500" />
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="••••••••"
                  className="w-full bg-slate-700 border border-slate-600 rounded-lg py-2 pl-10 pr-4 text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500 focus:ring-1 focus:ring-emerald-500"
                  required
                  minLength={6}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white font-semibold py-2 rounded-lg transition flex items-center justify-center gap-2"
            >
              {isLoading && <Loader className="w-4 h-4 animate-spin" />}
              {isSignUp ? 'Create Account' : 'Sign In'}
            </button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-slate-400">
              {isSignUp ? 'Already have an account?' : "Don't have an account?"}
              <button
                type="button"
                onClick={() => setIsSignUp(!isSignUp)}
                className="text-emerald-500 hover:text-emerald-400 font-medium ml-2"
              >
                {isSignUp ? 'Sign In' : 'Sign Up'}
              </button>
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
