import React, { useState, useEffect } from 'react'
import { Download, Trash2, Copy } from 'lucide-react'
import { imageAPI } from '../services/api'

export default function ImageGenerator() {
  const [prompt, setPrompt] = useState('')
  const [negativePrompt, setNegativePrompt] = useState('')
  const [style, setStyle] = useState('realistic')
  const [aspectRatio, setAspectRatio] = useState('1:1')
  const [images, setImages] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [styles, setStyles] = useState<any[]>([])
  const [history, setHistory] = useState<any[]>([])

  useEffect(() => {
    fetchStyles()
  }, [])

  const fetchStyles = async () => {
    try {
      const data = await imageAPI.getStyles()
      setStyles(data.styles || [])
    } catch (error) {
      console.error('Failed to load styles:', error)
    }
  }

  const handleGenerateImage = async () => {
    if (!prompt.trim()) return

    setIsLoading(true)
    try {
      const response = await imageAPI.generateImage(prompt, style)
      setImages(response.images || [])
      setHistory([
        {
          id: Date.now().toString(),
          prompt,
          timestamp: new Date(),
          images: response.images,
        },
        ...history,
      ])
    } catch (error) {
      console.error('Failed to generate image:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-darker-bg overflow-y-auto">
      {/* Header */}
      <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center px-6 bg-white dark:bg-dark-bg sticky top-0">
        <h1 className="text-xl font-bold">Image Generator</h1>
      </div>

      <div className="flex-1 flex gap-6 p-6 overflow-hidden">
        {/* Controls */}
        <div className="w-80 space-y-4 overflow-y-auto">
          <div>
            <label className="block text-sm font-medium mb-2">Prompt</label>
            <textarea
              value={prompt}
              onChange={(e) => setPrompt(e.target.value)}
              placeholder="Describe the image you want to generate..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none resize-none"
              rows={3}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Negative Prompt</label>
            <input
              type="text"
              value={negativePrompt}
              onChange={(e) => setNegativePrompt(e.target.value)}
              placeholder="What to avoid..."
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Style</label>
            <select
              value={style}
              onChange={(e) => setStyle(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none"
            >
              {styles.map((s) => (
                <option key={s.id} value={s.id}>
                  {s.name}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Aspect Ratio</label>
            <select
              value={aspectRatio}
              onChange={(e) => setAspectRatio(e.target.value)}
              className="w-full px-3 py-2 border border-gray-300 dark:border-gray-600 rounded-lg bg-white dark:bg-gray-700 focus:outline-none"
            >
              <option value="1:1">Square (1:1)</option>
              <option value="16:9">Landscape (16:9)</option>
              <option value="9:16">Portrait (9:16)</option>
              <option value="4:3">Standard (4:3)</option>
            </select>
          </div>

          <button
            onClick={handleGenerateImage}
            disabled={isLoading || !prompt.trim()}
            className="w-full px-4 py-2 bg-primary text-white rounded-lg hover:bg-primary/90 disabled:opacity-50 transition-colors"
          >
            {isLoading ? 'Generating...' : 'Generate Image'}
          </button>
        </div>

        {/* Gallery */}
        <div className="flex-1">
          {images.length === 0 ? (
            <div className="h-full flex items-center justify-center text-gray-500">
              <div className="text-center">
                <p>Enter a prompt and generate an image</p>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-1 gap-4">
              {images.map((img, idx) => (
                <div
                  key={idx}
                  className="rounded-lg overflow-hidden shadow-lg bg-gray-200 dark:bg-gray-700"
                >
                  <img
                    src={img.url}
                    alt={img.prompt}
                    className="w-full h-96 object-cover"
                  />
                  <div className="p-4 space-y-2">
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      {img.prompt}
                    </p>
                    <div className="flex gap-2">
                      <button className="flex-1 flex items-center justify-center gap-2 px-3 py-2 bg-gray-100 dark:bg-gray-700 rounded hover:bg-gray-200 dark:hover:bg-gray-600">
                        <Download size={16} />
                        Download
                      </button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
