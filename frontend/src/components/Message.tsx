import React, { useEffect, useRef } from 'react'
import { Copy, RefreshCw, Trash2, Share2 } from 'lucide-react'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { atomDark } from 'react-syntax-highlighter/dist/esm/styles/prism'
import { Message } from '../stores/chat'

interface MessageComponentProps {
  message: Message
  onCopy?: () => void
  onRegenerate?: () => void
  onDelete?: () => void
}

export default function MessageComponent({
  message,
  onCopy,
  onRegenerate,
  onDelete,
}: MessageComponentProps) {
  const messageRef = useRef<HTMLDivElement>(null)

  const isUser = message.role === 'user'

  return (
    <div
      ref={messageRef}
      className={`flex gap-4 p-4 ${
        isUser
          ? 'bg-white dark:bg-darker-bg'
          : 'bg-gray-50 dark:bg-dark-bg'
      }`}
    >
      {/* Avatar */}
      <div
        className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 text-white text-sm font-bold ${
          isUser ? 'bg-blue-500' : 'bg-primary'
        }`}
      >
        {isUser ? 'U' : 'A'}
      </div>

      {/* Content */}
      <div className="flex-1 min-w-0">
        <p className="text-sm font-semibold mb-2">
          {isUser ? 'You' : 'SAKHA AI'}
        </p>

        <div className="prose dark:prose-invert max-w-none text-sm">
          <ReactMarkdown
            components={{
              code({ className, children, ...props }) {
                const match = /language-(\w+)/.exec(className || '')
                const language = match ? match[1] : 'javascript'

                return (
                  <SyntaxHighlighter
                    style={atomDark}
                    language={language}
                    PreTag="div"
                    {...props}
                  >
                    {String(children).replace(/\n$/, '')}
                  </SyntaxHighlighter>
                )
              },
              p({ children }) {
                return <p className="mb-2">{children}</p>
              },
              ul({ children }) {
                return <ul className="list-disc list-inside mb-2">{children}</ul>
              },
              ol({ children }) {
                return <ol className="list-decimal list-inside mb-2">{children}</ol>
              },
            }}
          >
            {message.content}
          </ReactMarkdown>
        </div>

        {/* Actions */}
        {!isUser && (
          <div className="flex gap-2 mt-3">
            <button
              onClick={onCopy}
              className="flex items-center gap-1 px-3 py-1 text-xs rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              title="Copy response"
            >
              <Copy size={14} />
              Copy
            </button>
            <button
              onClick={onRegenerate}
              className="flex items-center gap-1 px-3 py-1 text-xs rounded hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
              title="Regenerate response"
            >
              <RefreshCw size={14} />
              Regenerate
            </button>
            <button
              onClick={onDelete}
              className="flex items-center gap-1 px-3 py-1 text-xs rounded hover:bg-red-100 dark:hover:bg-red-900/20 text-red-500 transition-colors"
              title="Delete message"
            >
              <Trash2 size={14} />
              Delete
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
