# SAKHA AI PREMIUM - FRONTEND COMPONENTS GUIDE

Complete guide for building ChatGPT-like frontend components.

## 1. ChatView Component (Enhanced)

Location: `frontend/src/components/ChatView.tsx`

```typescript
import React, { useState, useEffect, useRef } from 'react'
import { Send, Square, RotateCcw } from 'lucide-react'
import { useChatStore } from '../stores/chat'
import Message from './Message'
import ChatInput from './ChatInput'

export default function ChatView() {
  const { currentChat, currentChatId, addMessage, isLoading } = useChatStore()
  const [isStreaming, setIsStreaming] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [currentChat?.messages])

  const handleSendMessage = async (message: string) => {
    if (!currentChatId || !message.trim()) return

    // Add user message
    addMessage(currentChatId, {
      id: Date.now().toString(),
      role: 'user',
      content: message,
      timestamp: new Date(),
    })

    setIsStreaming(true)

    try {
      const response = await fetch('/api/chat/stream', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message,
          chat_id: currentChatId,
          model: currentChat?.model || 'gpt-4o',
          temperature: currentChat?.temperature || 0.7,
          max_tokens: currentChat?.max_tokens || 2048,
        }),
      })

      const reader = response.body?.getReader()
      const decoder = new TextDecoder()
      let assistantMessage = ''
      const messageId = Date.now().toString()

      addMessage(currentChatId, {
        id: messageId,
        role: 'assistant',
        content: '',
        timestamp: new Date(),
      })

      while (reader) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            try {
              const data = JSON.parse(line.slice(6))
              if (data.chunk) {
                assistantMessage += data.chunk
                // Update message in store
              }
            } catch (e) {
              // Ignore parse errors
            }
          }
        }
      }
    } catch (error) {
      console.error('Error sending message:', error)
    } finally {
      setIsStreaming(false)
    }
  }

  if (!currentChat) {
    return (
      <div className="flex-1 flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <h1 className="text-5xl font-bold mb-4 text-gold-500">SAKHA AI Premium</h1>
          <p className="text-slate-400 text-lg mb-8">Start a new conversation</p>
          <button
            onClick={() => useChatStore.getState().createChat()}
            className="px-6 py-3 bg-gold-500 text-slate-900 rounded-lg hover:bg-gold-600 transition-colors font-semibold"
          >
            New Chat
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto px-4 py-6 space-y-4">
        {currentChat.messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-slate-500">
            <p>No messages yet. Start the conversation!</p>
          </div>
        ) : (
          <>
            {currentChat.messages.map((message) => (
              <Message key={message.id} message={message} />
            ))}
            <div ref={messagesEndRef} />
          </>
        )}
      </div>

      {/* Input Area */}
      <div className="border-t border-slate-700 px-4 py-4 bg-slate-800/50 backdrop-blur">
        <ChatInput onSend={handleSendMessage} isLoading={isStreaming} />
      </div>
    </div>
  )
}
```

## 2. Message Component (Enhanced)

Location: `frontend/src/components/Message.tsx`

{% raw %}
```typescript
import React, { useState } from 'react'
import { Copy, Edit, Trash2, ThumbsUp, ThumbsDown } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

interface MessageProps {
  message: {
    id: string
    role: 'user' | 'assistant'
    content: string
    timestamp: Date
  }
}

export default function Message({ message }: MessageProps) {
  const [copied, setCopied] = useState(false)
  const [isEditing, setIsEditing] = useState(false)
  const [editContent, setEditContent] = useState(message.content)

  const copyToClipboard = () => {
    navigator.clipboard.writeText(message.content)
    setCopied(true)
    setTimeout(() => setCopied(false), 2000)
  }

  const isAssistant = message.role === 'assistant'

  return (
    <div className={`flex gap-4 animate-fade-in ${isAssistant ? 'bg-slate-800/50' : ''} rounded-lg p-4`}>
      {/* Avatar */}
      <div className={`w-8 h-8 rounded-full flex items-center justify-center font-semibold text-sm flex-shrink-0 ${
        isAssistant
          ? 'bg-gold-500/20 text-gold-500'
          : 'bg-slate-600 text-slate-100'
      }`}>
        {isAssistant ? '🤖' : '👤'}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        {isEditing ? (
          <textarea
            value={editContent}
            onChange={(e) => setEditContent(e.target.value)}
            className="w-full p-2 bg-slate-700 text-slate-100 rounded border border-slate-600"
          />
        ) : (
          <div className="prose prose-invert max-w-none">
            <ReactMarkdown
              components={{
                code: ({ inline, className, children }: any) => {
                  const match = /language-(\w+)/.exec(className || '')
                  return !inline && match ? (
                    <SyntaxHighlighter
                      style={atomDark}
                      language={match[1]}
                      PreTag="div"
                    >
                      {String(children).replace(/\n$/, '')}
                    </SyntaxHighlighter>
                  ) : (
                    <code className="bg-slate-700 px-2 py-1 rounded text-gold-500">
                      {children}
                    </code>
                  )
                },
              }}
            >
              {message.content}
            </ReactMarkdown>
          </div>
        )}
```
{% endraw %}

        {/* Actions */}
        {isAssistant && (
          <div className="flex gap-2 mt-3 text-slate-400">
            <button
              onClick={copyToClipboard}
              className="hover:text-gold-500 transition-colors"
              title="Copy"
            >
              <Copy size={18} />
            </button>
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="hover:text-gold-500 transition-colors"
              title="Edit"
            >
              <Edit size={18} />
            </button>
            <button
              className="hover:text-gold-500 transition-colors"
              title="Regenerate"
            >
              <RotateCcw size={18} />
            </button>
            <button
              className="hover:text-gold-500 transition-colors"
              title="Like"
            >
              <ThumbsUp size={18} />
            </button>
            <button
              className="hover:text-gold-500 transition-colors"
              title="Dislike"
            >
              <ThumbsDown size={18} />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
```

## 3. ChatInput Component (Enhanced)

Location: `frontend/src/components/ChatInput.tsx`

```typescript
import React, { useState, useRef } from 'react'
import { Send, Mic, Paperclip } from 'lucide-react'

interface ChatInputProps {
  onSend: (message: string) => void
  isLoading: boolean
}

export default function ChatInput({ onSend, isLoading }: ChatInputProps) {
  const [input, setInput] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSend = () => {
    if (input.trim() && !isLoading) {
      onSend(input)
      setInput('')
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="flex gap-3 items-end">
      {/* File Upload */}
      <button
        className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-400 hover:text-gold-500"
        title="Attach file"
      >
        <Paperclip size={20} />
      </button>

      {/* Textarea */}
      <textarea
        ref={textareaRef}
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Ask anything... (Shift+Enter for new line)"
        className="flex-1 p-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-500 resize-none focus:outline-none focus:border-gold-500 transition-colors max-h-32"
        rows={1}
        disabled={isLoading}
      />

      {/* Voice Input */}
      <button
        className="p-2 hover:bg-slate-700 rounded-lg transition-colors text-slate-400 hover:text-gold-500"
        title="Voice input"
      >
        <Mic size={20} />
      </button>

      {/* Send Button */}
      <button
        onClick={handleSend}
        disabled={!input.trim() || isLoading}
        className="p-2 bg-gold-500 hover:bg-gold-600 disabled:bg-slate-600 rounded-lg transition-colors text-slate-900 font-semibold disabled:cursor-not-allowed"
      >
        <Send size={20} />
      </button>
    </div>
  )
}
```

## 4. Model Selector Component

Location: `frontend/src/components/ModelSelector.tsx`

```typescript
import React, { useState } from 'react'
import { ChevronDown } from 'lucide-react'

const MODELS = [
  {
    id: 'gpt-5',
    name: 'GPT-5',
    speed: 3,
    cost: 5,
    intelligence: 5,
  },
  {
    id: 'gpt-4o',
    name: 'GPT-4o',
    speed: 4,
    cost: 3,
    intelligence: 5,
  },
  {
    id: 'claude-opus',
    name: 'Claude Opus',
    speed: 2,
    cost: 5,
    intelligence: 5,
  },
  {
    id: 'claude-sonnet',
    name: 'Claude Sonnet',
    speed: 4,
    cost: 3,
    intelligence: 5,
  },
  {
    id: 'gemini-pro',
    name: 'Gemini 2.5 Pro',
    speed: 3,
    cost: 2,
    intelligence: 5,
  },
  {
    id: 'gemini-flash',
    name: 'Gemini 2.5 Flash',
    speed: 5,
    cost: 1,
    intelligence: 3,
  },
  {
    id: 'deepseek-chat',
    name: 'DeepSeek Chat',
    speed: 5,
    cost: 1,
    intelligence: 3,
  },
  {
    id: 'deepseek-reasoner',
    name: 'DeepSeek Reasoner',
    speed: 2,
    cost: 2,
    intelligence: 4,
  },
]

interface ModelSelectorProps {
  selectedModel: string
  onModelChange: (model: string) => void
}

export default function ModelSelector({
  selectedModel,
  onModelChange,
}: ModelSelectorProps) {
  const [isOpen, setIsOpen] = useState(false)
  const currentModel = MODELS.find((m) => m.id === selectedModel)

  const renderBadges = (model: any) => (
    <div className="flex gap-1 ml-2">
      <span title="Speed" className="text-xs">
        {'⚡'.repeat(model.speed)}
      </span>
      <span title="Cost" className="text-xs">
        {'💰'.repeat(model.cost)}
      </span>
      <span title="Intelligence" className="text-xs">
        {'🧠'.repeat(model.intelligence)}
      </span>
    </div>
  )

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="flex items-center gap-2 px-3 py-2 bg-slate-700 hover:bg-slate-600 rounded-lg transition-colors text-slate-100"
      >
        {currentModel?.name}
        {renderBadges(currentModel)}
        <ChevronDown size={16} />
      </button>

      {isOpen && (
        <div className="absolute top-full mt-2 w-64 bg-slate-700 rounded-lg shadow-lg border border-slate-600 z-50">
          {MODELS.map((model) => (
            <button
              key={model.id}
              onClick={() => {
                onModelChange(model.id)
                setIsOpen(false)
              }}
              className={`w-full text-left px-4 py-3 hover:bg-slate-600 transition-colors first:rounded-t-lg last:rounded-b-lg border-b border-slate-600 last:border-b-0 ${
                selectedModel === model.id ? 'bg-gold-500/20 text-gold-500' : 'text-slate-100'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold">{model.name}</span>
                {renderBadges(model)}
              </div>
            </button>
          ))}
        </div>
      )}
    </div>
  )
}
```

## 5. Sidebar Component (Enhanced)

Location: `frontend/src/components/Sidebar.tsx`

See the existing Sidebar.tsx and enhance it with:
- Chat search functionality
- Folders/organization
- Archive section
- Pinned chats
- Settings access
- Profile section

## 6. MemoryPanel Component

Location: `frontend/src/components/MemoryPanel.tsx`

```typescript
import React, { useState } from 'react'
import { X, Plus, Edit, Trash2 } from 'lucide-react'

interface MemoryPanelProps {
  onClose: () => void
}

export default function MemoryPanel({ onClose }: MemoryPanelProps) {
  const [memories, setMemories] = useState<any[]>([])
  const [newMemory, setNewMemory] = useState('')
  const [selectedMemory, setSelectedMemory] = useState<string | null>(null)

  return (
    <div className="glass-dark border border-slate-600 rounded-lg p-6 max-h-96 overflow-y-auto">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-lg font-semibold text-gold-500">User Memory</h2>
        <button onClick={onClose} className="text-slate-400 hover:text-slate-100">
          <X size={20} />
        </button>
      </div>

      <div className="space-y-3 mb-4">
        {memories.map((memory) => (
          <div
            key={memory.id}
            className="p-3 bg-slate-700/50 rounded border border-slate-600 hover:border-gold-500/50 transition-colors"
          >
            <div className="flex justify-between items-start">
              <p className="text-slate-100 text-sm">{memory.content}</p>
              <div className="flex gap-1">
                <button className="text-slate-400 hover:text-gold-500">
                  <Edit size={16} />
                </button>
                <button className="text-slate-400 hover:text-red-500">
                  <Trash2 size={16} />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          type="text"
          value={newMemory}
          onChange={(e) => setNewMemory(e.target.value)}
          placeholder="Add memory..."
          className="flex-1 p-2 bg-slate-700 border border-slate-600 rounded text-slate-100 placeholder-slate-500 focus:border-gold-500 outline-none"
        />
        <button className="p-2 bg-gold-500 hover:bg-gold-600 rounded text-slate-900">
          <Plus size={20} />
        </button>
      </div>
    </div>
  )
}
```

## Implementation Order

1. **Update Chat Component** - Add streaming support
2. **Update Message Component** - Add markdown, code highlighting, actions
3. **Update ChatInput Component** - Add file/voice buttons
4. **Add ModelSelector** - For model switching
5. **Add MemoryPanel** - For user memory management
6. **Add FileUpload** - For file analysis
7. **Add VoiceInput** - For speech-to-text
8. **Add ImageStudio** - For image generation
9. **Add SettingsPanel** - For user preferences
10. **Add Export** - For chat export

## Styling Notes

- Use the new gold color palette (#FFD700, #FFB800)
- Apply glassmorphism effects with backdrop-blur
- Smooth animations with Framer Motion
- Mobile-first responsive design
- Dark theme by default

All components should follow React best practices and use TypeScript for type safety.
