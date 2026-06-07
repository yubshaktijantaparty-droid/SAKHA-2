import React from 'react'
import { Link } from 'react-router-dom'
import { ArrowRight, Zap, Sparkles, Shield, Rocket } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 dark:from-darker-bg dark:to-dark-bg">
      {/* Navigation */}
      <nav className="border-b border-gray-200 dark:border-gray-700 bg-white dark:bg-dark-bg sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <h1 className="gradient-text text-2xl font-bold">SAKHA AI</h1>
          <div className="flex gap-6">
            <a href="#features" className="text-gray-600 dark:text-gray-400 hover:text-gray-900">
              Features
            </a>
            <a href="#models" className="text-gray-600 dark:text-gray-400 hover:text-gray-900">
              Models
            </a>
            <a href="#tools" className="text-gray-600 dark:text-gray-400 hover:text-gray-900">
              Tools
            </a>
            <button className="px-6 py-2 bg-primary text-white rounded-lg hover:bg-primary/90">
              Get Started
            </button>
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="max-w-7xl mx-auto px-6 py-20 text-center">
        <h2 className="text-5xl font-bold mb-6 dark:text-white">
          Your Personal AI Assistant
        </h2>
        <p className="text-xl text-gray-600 dark:text-gray-400 mb-8 max-w-2xl mx-auto">
          Chat with advanced AI models, generate images, analyze files, and boost your productivity.
          All in one premium application.
        </p>
        <div className="flex gap-4 justify-center">
          <Link
            to="/login"
            className="px-8 py-3 bg-primary text-white rounded-lg hover:bg-primary/90 flex items-center gap-2"
          >
            Start Chatting
            <ArrowRight size={20} />
          </Link>
          <a
            href="#features"
            className="px-8 py-3 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700"
          >
            Learn More
          </a>
        </div>
      </section>

      {/* Features */}
      <section id="features" className="max-w-7xl mx-auto px-6 py-20">
        <h3 className="text-3xl font-bold text-center mb-12">Core Features</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {[
            { icon: Sparkles, title: 'AI Chat', desc: 'Chat with multiple AI models' },
            { icon: Zap, title: 'Fast', desc: 'Lightning-fast responses' },
            { icon: Rocket, title: 'Advanced', desc: 'State-of-the-art technology' },
            { icon: Shield, title: 'Secure', desc: 'Your data is safe' },
          ].map((feature, idx) => {
            const Icon = feature.icon
            return (
              <div
                key={idx}
                className="p-6 bg-white dark:bg-dark-bg rounded-lg border border-gray-200 dark:border-gray-700 text-center"
              >
                <Icon size={32} className="mx-auto text-primary mb-3" />
                <h4 className="font-semibold mb-2">{feature.title}</h4>
                <p className="text-sm text-gray-600 dark:text-gray-400">{feature.desc}</p>
              </div>
            )
          })}
        </div>
      </section>

      {/* Models */}
      <section id="models" className="bg-white dark:bg-dark-bg py-20">
        <div className="max-w-7xl mx-auto px-6">
          <h3 className="text-3xl font-bold text-center mb-12">Supported AI Models</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {['OpenAI GPT-4', 'DeepSeek', 'Google Gemini', 'OpenRouter'].map((model, idx) => (
              <div
                key={idx}
                className="p-6 bg-gray-50 dark:bg-darker-bg rounded-lg border border-gray-200 dark:border-gray-700 text-center hover:shadow-lg transition-shadow"
              >
                <div className="w-12 h-12 bg-primary/10 rounded-lg mx-auto mb-3 flex items-center justify-center">
                  <span className="text-lg font-bold text-primary">{model.charAt(0)}</span>
                </div>
                <h4 className="font-semibold">{model}</h4>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="bg-gradient-to-r from-primary to-blue-600 text-white py-16">
        <div className="max-w-4xl mx-auto px-6 text-center">
          <h3 className="text-3xl font-bold mb-4">Ready to get started?</h3>
          <p className="text-lg mb-8 opacity-90">
            Join thousands of users already using SAKHA AI for learning, productivity, and creativity.
          </p>
          <button className="px-8 py-3 bg-white text-primary rounded-lg hover:bg-gray-100 font-semibold">
            Start Free Trial
          </button>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-dark-bg text-gray-400 py-8 border-t border-gray-700">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p>&copy; 2024 SAKHA AI. All rights reserved.</p>
        </div>
      </footer>
    </div>
  )
}
