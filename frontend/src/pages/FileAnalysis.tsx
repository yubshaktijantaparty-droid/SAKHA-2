import React, { useState } from 'react'
import { Upload, Trash2, MoreVertical } from 'lucide-react'
import { fileAPI } from '../services/api'

export default function FileAnalysis() {
  const [uploadedFiles, setUploadedFiles] = useState<any[]>([])
  const [isLoading, setIsLoading] = useState(false)
  const [selectedFile, setSelectedFile] = useState<any>(null)
  const [analysisType, setAnalysisType] = useState('summarize')
  const [analysis, setAnalysis] = useState<any>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files
    if (!files) return

    setIsLoading(true)
    try {
      for (let file of files) {
        const response = await fileAPI.uploadFile(file)
        setUploadedFiles([response, ...uploadedFiles])
      }
    } catch (error) {
      console.error('Failed to upload file:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleAnalyzeFile = async (fileId: string) => {
    setIsLoading(true)
    try {
      const response = await fileAPI.analyzeFile(fileId, analysisType)
      setAnalysis(response.analysis)
    } catch (error) {
      console.error('Failed to analyze file:', error)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="h-full flex flex-col bg-white dark:bg-darker-bg overflow-y-auto">
      {/* Header */}
      <div className="h-14 border-b border-gray-200 dark:border-gray-700 flex items-center px-6 bg-white dark:bg-dark-bg sticky top-0">
        <h1 className="text-xl font-bold">File Analysis</h1>
      </div>

      <div className="flex-1 p-6 overflow-hidden flex gap-6">
        {/* Upload Area */}
        <div className="w-80 space-y-4">
          <div className="border-2 border-dashed border-gray-300 dark:border-gray-600 rounded-lg p-8 text-center hover:border-primary transition-colors">
            <Upload size={32} className="mx-auto mb-3 text-gray-400" />
            <input
              type="file"
              multiple
              onChange={handleFileUpload}
              className="hidden"
              id="file-upload"
              accept=".pdf,.docx,.txt,.jpg,.png,.csv"
            />
            <label htmlFor="file-upload" className="block cursor-pointer">
              <p className="text-sm font-medium">Upload files</p>
              <p className="text-xs text-gray-500 mt-1">PDF, DOCX, TXT, Images, CSV</p>
            </label>
          </div>

          {/* File List */}
          <div className="space-y-2">
            <h3 className="text-sm font-medium">Uploaded Files</h3>
            {uploadedFiles.map((file) => (
              <div
                key={file.file_id}
                className="p-3 bg-gray-100 dark:bg-gray-700 rounded-lg flex items-center justify-between cursor-pointer hover:bg-gray-200 dark:hover:bg-gray-600"
                onClick={() => setSelectedFile(file)}
              >
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium truncate">{file.file_id}</p>
                </div>
                <button className="p-1 hover:text-red-500">
                  <Trash2 size={16} />
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Analysis Area */}
        <div className="flex-1 flex flex-col">
          {selectedFile ? (
            <>
              <div className="mb-4">
                <h3 className="text-lg font-semibold mb-3">{selectedFile.file_id}</h3>
                <div className="flex gap-2 mb-4">
                  {['summarize', 'analyze', 'extract', 'answer'].map((type) => (
                    <button
                      key={type}
                      onClick={() => setAnalysisType(type)}
                      className={`px-4 py-2 rounded text-sm transition-colors ${
                        analysisType === type
                          ? 'bg-primary text-white'
                          : 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300'
                      }`}
                    >
                      {type.charAt(0).toUpperCase() + type.slice(1)}
                    </button>
                  ))}
                </div>
                <button
                  onClick={() => handleAnalyzeFile(selectedFile.file_id)}
                  disabled={isLoading}
                  className="px-4 py-2 bg-primary text-white rounded hover:bg-primary/90 disabled:opacity-50"
                >
                  {isLoading ? 'Analyzing...' : 'Analyze'}
                </button>
              </div>

              {analysis && (
                <div className="flex-1 bg-gray-50 dark:bg-dark-bg p-4 rounded-lg overflow-y-auto">
                  <p className="text-sm">{analysis}</p>
                </div>
              )}
            </>
          ) : (
            <div className="h-full flex items-center justify-center text-gray-500">
              <p>Upload and select a file to analyze</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
