import React from 'react'
import { BookOpen, Briefcase, Code, Sparkles } from 'lucide-react'

const tools = [
  {
    id: 'study',
    title: 'Study Assistant',
    description: 'NEET prep, Biology, Physics, Chemistry, MCQs',
    icon: BookOpen,
    color: 'bg-blue-500',
  },
  {
    id: 'writing',
    title: 'Writing Assistant',
    description: 'Essays, Blogs, Emails, Scripts',
    icon: Sparkles,
    color: 'bg-purple-500',
  },
  {
    id: 'business',
    title: 'Business Assistant',
    description: 'Startup ideas, Marketing, Sales, Strategy',
    icon: Briefcase,
    color: 'bg-green-500',
  },
  {
    id: 'coding',
    title: 'Coding Assistant',
    description: 'HTML, CSS, JS, Python, Java, C++, Kotlin',
    icon: Code,
    color: 'bg-orange-500',
  },
]

export default function ToolsHub() {
  return (
    <div className="h-full flex flex-col bg-white dark:bg-darker-bg overflow-y-auto">
      {/* Header */}
      <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center px-6 bg-white dark:bg-dark-bg sticky top-0">
        <h1 className="text-xl font-bold">Tools Hub</h1>
      </div>

      <div className="flex-1 p-8">
        <div className="max-w-6xl mx-auto">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {tools.map((tool) => {
              const Icon = tool.icon
              return (
                <div
                  key={tool.id}
                  className="p-6 rounded-lg border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all cursor-pointer hover:-translate-y-1"
                >
                  <div className="flex items-start gap-4">
                    <div className={`${tool.color} p-3 rounded-lg text-white`}>
                      <Icon size={24} />
                    </div>
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold mb-2">{tool.title}</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {tool.description}
                      </p>
                      <button className="mt-4 px-4 py-2 bg-primary text-white rounded text-sm hover:bg-primary/90">
                        Open Tool
                      </button>
                    </div>
                  </div>
                </div>
              )
            })}
          </div>
        </div>
      </div>
    </div>
  )
}
