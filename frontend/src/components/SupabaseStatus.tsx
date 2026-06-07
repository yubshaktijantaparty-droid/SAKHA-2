import { useState } from 'react'
import { supabaseHealthCheck } from '../lib/supabaseService'
import { CheckCircle, AlertCircle, Loader } from 'lucide-react'
import toast from 'react-hot-toast'

export function SupabaseStatus() {
  const [status, setStatus] = useState<any>(null)
  const [loading, setLoading] = useState(false)
  const [showDetails, setShowDetails] = useState(false)

  const handleCheck = async () => {
    setLoading(true)
    try {
      const result = await supabaseHealthCheck()
      setStatus(result)
      
      if (result.connection.connected) {
        toast.success('Supabase connection verified!')
      } else {
        toast.error('Supabase connection failed')
      }
    } catch (error) {
      toast.error('Health check failed')
      console.error(error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-white font-semibold">Supabase Status</h3>
        <button
          onClick={handleCheck}
          disabled={loading}
          className="px-4 py-2 bg-emerald-600 hover:bg-emerald-700 disabled:opacity-50 text-white rounded-lg text-sm"
        >
          {loading ? (
            <>
              <Loader className="w-4 h-4 animate-spin inline mr-2" />
              Checking...
            </>
          ) : (
            'Check Status'
          )}
        </button>
      </div>

      {status && (
        <div className="space-y-3">
          {/* Connection Status */}
          <div className="flex items-center gap-2 p-3 bg-slate-700 rounded">
            {status.connection.connected ? (
              <CheckCircle className="w-5 h-5 text-emerald-500" />
            ) : (
              <AlertCircle className="w-5 h-5 text-red-500" />
            )}
            <div>
              <p className="text-white text-sm font-medium">Connection</p>
              <p className="text-slate-400 text-xs">
                {status.connection.connected ? 'Connected ✓' : 'Disconnected ✗'}
              </p>
            </div>
          </div>

          {/* User Status */}
          <div className="flex items-center gap-2 p-3 bg-slate-700 rounded">
            {status.currentUser ? (
              <CheckCircle className="w-5 h-5 text-emerald-500" />
            ) : (
              <AlertCircle className="w-5 h-5 text-slate-500" />
            )}
            <div>
              <p className="text-white text-sm font-medium">User Session</p>
              <p className="text-slate-400 text-xs">
                {status.currentUser ? `Logged in: ${status.currentUser.email}` : 'No active session'}
              </p>
            </div>
          </div>

          {/* Database Tables */}
          <div className="space-y-2">
            <p className="text-white text-sm font-medium">Database Tables</p>
            {Object.entries(status.tables).map(([table, info]: [string, any]) => (
              <div key={table} className="flex items-center gap-2 p-2 bg-slate-700 rounded text-xs">
                {info.exists ? (
                  <CheckCircle className="w-4 h-4 text-emerald-500 flex-shrink-0" />
                ) : (
                  <AlertCircle className="w-4 h-4 text-red-500 flex-shrink-0" />
                )}
                <span className="text-slate-300">{table}</span>
                <span className="text-slate-500 ml-auto">
                  {info.exists ? 'Ready' : 'Not found'}
                </span>
              </div>
            ))}
          </div>

          {/* Details Toggle */}
          <button
            onClick={() => setShowDetails(!showDetails)}
            className="w-full text-xs text-emerald-400 hover:text-emerald-300 py-2"
          >
            {showDetails ? 'Hide Details' : 'Show Details'}
          </button>

          {showDetails && (
            <pre className="bg-slate-900 p-3 rounded text-slate-300 text-xs overflow-auto max-h-40">
              {JSON.stringify(status, null, 2)}
            </pre>
          )}
        </div>
      )}
    </div>
  )
}
