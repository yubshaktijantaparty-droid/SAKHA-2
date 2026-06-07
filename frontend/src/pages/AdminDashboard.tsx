import React, { useState, useEffect } from 'react'
import { BarChart, Users, MessageSquare, Zap, TrendingUp, AlertCircle } from 'lucide-react'
import axios from 'axios'

export default function AdminDashboard() {
  const [stats, setStats] = useState<any>(null)
  const [logs, setLogs] = useState<any[]>([])
  const [performance, setPerformance] = useState<any>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    fetchAdminData()
  }, [])

  const fetchAdminData = async () => {
    try {
      const adminKey = 'your-admin-key'
      const headers = { 'X-Admin-Key': adminKey }

      const [statsRes, logsRes, perfRes] = await Promise.all([
        axios.get('/api/admin/stats', { headers }),
        axios.get('/api/admin/logs?limit=10', { headers }),
        axios.get('/api/admin/performance', { headers }),
      ])

      setStats(statsRes.data)
      setLogs(logsRes.data.logs || [])
      setPerformance(perfRes.data)
    } catch (error) {
      console.error('Failed to fetch admin data:', error)
    } finally {
      setIsLoading(false)
    }
  }

  if (isLoading) {
    return <div className="p-8">Loading admin dashboard...</div>
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-darker-bg overflow-y-auto">
      {/* Header */}
      <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center px-6 bg-white dark:bg-dark-bg sticky top-0">
        <h1 className="text-xl font-bold">Admin Dashboard</h1>
      </div>

      <div className="flex-1 p-6">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-blue-100">Total Users</p>
                <p className="text-3xl font-bold">{stats?.total_users || 0}</p>
              </div>
              <Users size={32} className="opacity-20" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-green-100">Total Chats</p>
                <p className="text-3xl font-bold">{stats?.total_chats || 0}</p>
              </div>
              <MessageSquare size={32} className="opacity-20" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100">Images Generated</p>
                <p className="text-3xl font-bold">{stats?.total_images_generated || 0}</p>
              </div>
              <TrendingUp size={32} className="opacity-20" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-6 rounded-lg">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100">Uptime</p>
                <p className="text-3xl font-bold">{stats?.uptime || '0%'}</p>
              </div>
              <Zap size={32} className="opacity-20" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Performance Metrics */}
          <div className="lg:col-span-1 bg-gray-50 dark:bg-dark-bg p-6 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold mb-4">Performance</h3>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Avg Response Time</p>
                <p className="text-2xl font-bold">{performance?.response_time_avg || 0}ms</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Requests/Second</p>
                <p className="text-2xl font-bold">{performance?.requests_per_second || 0}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 dark:text-gray-400">Cache Hit Rate</p>
                <p className="text-2xl font-bold">{performance?.cache_hit_rate || 0}%</p>
              </div>
            </div>
          </div>

          {/* Recent Logs */}
          <div className="lg:col-span-2 bg-gray-50 dark:bg-dark-bg p-6 rounded-lg border border-gray-200 dark:border-gray-700">
            <h3 className="text-lg font-semibold mb-4">Recent Logs</h3>
            <div className="space-y-2 max-h-96 overflow-y-auto">
              {logs.length === 0 ? (
                <p className="text-sm text-gray-500">No logs available</p>
              ) : (
                logs.map((log, idx) => (
                  <div key={idx} className="flex gap-3 text-sm">
                    <AlertCircle size={16} className="text-red-500 flex-shrink-0 mt-0.5" />
                    <p className="text-gray-600 dark:text-gray-400">{log}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
