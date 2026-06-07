import React, { useState, useEffect, useRef } from 'react'
import { Loader } from 'lucide-react'
import MessageComponent from './Message'
import ChatInput from './ChatInput'
import { useChatStore, Message } from '../stores/chat'
import { chatAPI } from '../services/api'

export default function ChatView() {
  const { currentChat, createChat, addMessage } = useChatStore()
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [currentChat?.messages])

  useEffect(() => {
    if (!currentChat) {
      createChat()
    }
  }, [])

  const handleSendMessage = async (messageText: string, model: string) => {
    if (!currentChat) return

    setIsLoading(true)

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
      timestamp: new Date(),
    }
    addMessage(currentChat.id, userMessage)

    try {
      // Get AI response
      const response = await chatAPI.sendMessage(messageText, model)

      // Add assistant message
      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      }
      addMessage(currentChat.id, assistantMessage)
    } catch (error) {
      console.error('Failed to get response:', error)

      // Add error message
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content:
          'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date(),
      }
      addMessage(currentChat.id, errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  if (!currentChat) {
    return (
      <div className="flex-1 flex items-center justify-center">
        <div className="text-center">
          <h2 className="text-2xl font-bold mb-4">Welcome to SAKHA AI</h2>
          <p className="text-gray-600 dark:text-gray-400 mb-6">
            Start a new conversation to begin
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="flex-1 flex flex-col overflow-hidden">
      {/* Messages */}
      <div className="flex-1 overflow-y-auto">
        {currentChat.messages.length === 0 ? (
          <div className="h-full flex items-center justify-center text-gray-500">
            <div className="text-center">
              <h3 className="text-lg font-semibold mb-2">Start a conversation</h3>
              <p className="text-sm">Send your first message to get started!</p>
            </div>
          </div>
        ) : (
          <div>
            {currentChat.messages.map((message) => (
              <MessageComponent
                key={message.id}
                message={message}
                onCopy={() => {
                  navigator.clipboard.writeText(message.content)
                }}
                onRegenerate={() => {
                  console.log('Regenerate:', message.id)
                }}
                onDelete={() => {
                  console.log('Delete:', message.id)
                }}
              />
            ))}
            {isLoading && (
              <div className="flex gap-4 p-4 bg-gray-50 dark:bg-dark-bg">
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                  A
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.4s' }} />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      {/* Input */}
      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  )
}
