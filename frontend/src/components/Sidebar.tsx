import React, { useState } from 'react'
import { Plus, Trash2, Search, Image, MessageSquare, Settings } from 'lucide-react'
import { NavLink } from 'react-router-dom'
import { useChatStore } from '../stores/chat'

export default function Sidebar() {
  const { chats, currentChatId, createChat, deleteChat, selectChat } = useChatStore()
  const [searchQuery, setSearchQuery] = useState('')

  const filteredChats = chats.filter((chat) =>
    chat.title.toLowerCase().includes(searchQuery.toLowerCase())
  )

  return (
    <div className="w-64 bg-white dark:bg-dark-bg border-r border-gray-200 dark:border-gray-700 flex flex-col">
      <div className="p-4 border-b border-gray-200 dark:border-gray-700 space-y-3">
        <button
          onClick={() => createChat()}
          className="w-full flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 transition-colors font-medium"
        >
          <Plus size={18} />
          New Chat
        </button>

        <nav className="grid gap-2">
          <NavLink
            to="/app/chat"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`
            }
          >
            <MessageSquare size={16} />
            Chat
          </NavLink>
          <NavLink
            to="/app/images"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`
            }
          >
            <Image size={16} />
            Image Studio
          </NavLink>
          <NavLink
            to="/app/settings"
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-primary text-white'
                  : 'text-gray-600 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-800'
              }`
            }
          >
            <Settings size={16} />
            Settings
          </NavLink>
        </nav>
      </div>

      <div className="p-3 border-b border-gray-200 dark:border-gray-700">
        <div className="relative">
          <Search size={16} className="absolute left-3 top-3 text-gray-400" />
          <input
            type="text"
            placeholder="Search chats..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-2 bg-gray-100 dark:bg-gray-700 rounded-lg focus:outline-none text-sm"
          />
        </div>
      </div>

      <div className="flex-1 overflow-y-auto">
        {filteredChats.length === 0 ? (
          <div className="p-4 text-center text-gray-500 text-sm">
            No chats yet. Start a new conversation!
          </div>
        ) : (
          <div className="p-2">
            {filteredChats.map((chat) => (
              <div
                key={chat.id}
                className={`group p-3 mb-2 rounded-lg cursor-pointer transition-colors ${
                  currentChatId === chat.id
                    ? 'bg-primary/10 dark:bg-primary/20'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-700'
                }`}
              >
                <div
                  onClick={() => selectChat(chat.id)}
                  className="flex items-start justify-between gap-2"
                >
                  <div className="flex-1 min-w-0">
                    <p className="text-sm font-medium truncate">{chat.title}</p>
                    <p className="text-xs text-gray-500 mt-1">
                      {chat.messages.length} messages
                    </p>
                  </div>
                  <button
                    onClick={(e) => {
                      e.stopPropagation()
                      deleteChat(chat.id)
                    }}
                    className="opacity-0 group-hover:opacity-100 p-1 hover:bg-red-100 dark:hover:bg-red-900/20 rounded transition-all"
                  >
                    <Trash2 size={14} className="text-red-500" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>

      <div className="p-4 border-t border-gray-200 dark:border-gray-700 text-center text-xs text-gray-500">
        <p>SAKHA AI v1.0</p>
      </div>
    </div>
  )
}
