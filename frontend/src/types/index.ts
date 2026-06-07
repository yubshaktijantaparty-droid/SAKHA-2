"""TypeScript types for SAKHA AI Premium frontend"""

// Message type
export interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  model?: string;
  tokens_used?: number;
  created_at: Date;
  edited_content?: string;
  edited_at?: Date;
}

// Chat type
export interface Chat {
  id: string;
  user_id: string;
  title: string;
  description?: string;
  model: string;
  messages: Message[];
  temperature: number;
  max_tokens: number;
  created_at: Date;
  updated_at: Date;
  is_archived?: boolean;
  is_pinned?: boolean;
  tags?: string[];
  folder?: string;
}

// AI Model type
export interface AIModel {
  id: string;
  name: string;
  provider: 'openai' | 'anthropic' | 'google' | 'deepseek';
  speed: number; // 1-5
  cost: number; // 1-5
  intelligence: number; // 1-5
  context_window: number;
  description: string;
  available: boolean;
}

// Memory type
export interface Memory {
  id: string;
  user_id: string;
  name: string;
  content: string;
  memory_type: 'personal' | 'work' | 'preferences' | 'custom';
  is_active: boolean;
  importance: number;
  created_at: Date;
  updated_at: Date;
}

// File type
export interface UploadedFile {
  id: string;
  user_id: string;
  filename: string;
  file_type: string;
  file_size: number;
  is_analyzed: boolean;
  analysis_summary?: string;
  created_at: Date;
}

// User type
export interface User {
  id: string;
  email: string;
  username: string;
  full_name: string;
  avatar_url?: string;
  preferences: UserPreferences;
  created_at: Date;
}

// User preferences type
export interface UserPreferences {
  theme: 'dark' | 'light' | 'auto';
  language: string;
  default_model: string;
  temperature: number;
  max_tokens: number;
  enable_memory: boolean;
  enable_voice: boolean;
  enable_notifications: boolean;
  auto_save_chats: boolean;
}

// API Response type
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  error?: string;
  message?: string;
}

// Streaming chunk type
export interface StreamingChunk {
  type: 'chunk' | 'complete' | 'error';
  content: string;
  tokens_used?: number;
}

// Export type
export interface ExportOptions {
  format: 'pdf' | 'markdown' | 'txt' | 'json';
  include_metadata: boolean;
  date_range?: {
    start: Date;
    end: Date;
  };
}
