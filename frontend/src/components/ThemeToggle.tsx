import React from 'react'
import { Moon, Sun, Monitor } from 'lucide-react'
import { useAppStore } from '../stores/app'

export default function ThemeToggle() {
  const { theme, setTheme } = useAppStore()

  return (
    <div className="flex gap-1 bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
      <button
        onClick={() => setTheme('light')}
        className={`p-2 rounded transition-colors ${
          theme === 'light'
            ? 'bg-white dark:bg-gray-600 shadow'
            : 'hover:bg-gray-200 dark:hover:bg-gray-600'
        }`}
        title="Light mode"
      >
        <Sun size={16} />
      </button>
      <button
        onClick={() => setTheme('dark')}
        className={`p-2 rounded transition-colors ${
          theme === 'dark'
            ? 'bg-white dark:bg-gray-600 shadow'
            : 'hover:bg-gray-200 dark:hover:bg-gray-600'
        }`}
        title="Dark mode"
      >
        <Moon size={16} />
      </button>
      <button
        onClick={() => setTheme('system')}
        className={`p-2 rounded transition-colors ${
          theme === 'system'
            ? 'bg-white dark:bg-gray-600 shadow'
            : 'hover:bg-gray-200 dark:hover:bg-gray-600'
        }`}
        title="System theme"
      >
        <Monitor size={16} />
      </button>
    </div>
  )
}
