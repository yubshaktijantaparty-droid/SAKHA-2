import React, { useState, useEffect, useRef } from 'react'
import MessageComponent from './Message'
import ChatInput from './ChatInput'
import { useChatStore, Message } from '../stores/chat'
import { chatAPI } from '../services/api'

export default function ChatView() {
  const { currentChat, createChat, addMessage, deleteMessage } = useChatStore()
  const [isLoading, setIsLoading] = useState(false)
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [currentChat?.messages])

  useEffect(() => {
    if (!currentChat) {
      createChat()
    }
  }, [currentChat, createChat])

  const handleSendMessage = async (messageText: string, model: string, deepThinking?: boolean) => {
    if (!currentChat || !messageText.trim()) return

    setIsLoading(true)

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: messageText,
      timestamp: new Date(),
    }
    addMessage(currentChat.id, userMessage)

    try {
      // Convert chat history to conversation format for API
      const conversationHistory = currentChat.messages
        .slice(-10) // Limit to last 10 messages for context
        .map(msg => ({
          role: msg.role,
          content: msg.content,
        }))

      const response = await chatAPI.sendMessage(
        messageText,
        model,
        deepThinking,
        conversationHistory
      )

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: response.message,
        timestamp: new Date(),
      }
      addMessage(currentChat.id, assistantMessage)
    } catch (error) {
      console.error('Failed to get response:', error)
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

  const handleRegenerate = async (messageId: string) => {
    if (!currentChat) return
    const lastUserMessage = [...currentChat.messages]
      .reverse()
      .find((message) => message.role === 'user')

    if (!lastUserMessage) return
    await handleSendMessage(lastUserMessage.content, currentChat.model)
  }

  const handleDeleteMessage = (messageId: string) => {
    if (!currentChat) return
    deleteMessage(currentChat.id, messageId)
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
      <div className="border-b border-gray-200 dark:border-gray-700 px-6 py-4 bg-gray-50 dark:bg-gray-900">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <h2 className="text-xl font-semibold">{currentChat.title}</h2>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              {currentChat.messages.length} messages • Model: {currentChat.model}
            </p>
          </div>
          <div className="text-sm text-gray-600 dark:text-gray-400">
            Powered by SAKHA AI premium assistant
          </div>
        </div>
      </div>

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
                onRegenerate={() => handleRegenerate(message.id)}
                onDelete={() => handleDeleteMessage(message.id)}
              />
            ))}
            {isLoading && (
              <div className="flex gap-4 p-4 bg-gray-50 dark:bg-dark-bg">
                <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center flex-shrink-0">
                  A
                </div>
                <div className="flex items-center gap-2">
                  <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0.2s' }}
                  />
                  <div
                    className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"
                    style={{ animationDelay: '0.4s' }}
                  />
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>
        )}
      </div>

      <ChatInput onSendMessage={handleSendMessage} isLoading={isLoading} />
    </div>
  )
}
