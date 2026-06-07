import { supabase } from './supabase'
import toast from 'react-hot-toast'

// ============================================
// SUPABASE CONNECTION & DATA SERVICE
// ============================================

/**
 * Test Supabase connection
 */
export async function testSupabaseConnection() {
  try {
    const { data, error } = await supabase.auth.getSession()
    if (error) throw error
    return { connected: true, data }
  } catch (error) {
    console.error('Supabase Connection Error:', error)
    return { connected: false, error }
  }
}

/**
 * Get current authenticated user
 */
export async function getCurrentUser() {
  try {
    const { data: { user }, error } = await supabase.auth.getUser()
    if (error) throw error
    return user
  } catch (error) {
    console.error('Get User Error:', error)
    return null
  }
}

/**
 * Save user data to database
 */
export async function saveUserData(userId: string, userData: any) {
  try {
    const { data, error } = await supabase
      .from('user_profiles')
      .upsert({
        id: userId,
        ...userData,
        updated_at: new Date().toISOString(),
      })
      .select()

    if (error) throw error
    toast.success('User data saved successfully')
    return data
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Failed to save data'
    console.error('Save Data Error:', message)
    toast.error(message)
    return null
  }
}

/**
 * Save chat message
 */
export async function saveChatMessage(userId: string, message: string, role: 'user' | 'assistant') {
  try {
    const { data, error } = await supabase
      .from('messages')
      .insert({
        user_id: userId,
        content: message,
        role: role,
        created_at: new Date().toISOString(),
      })
      .select()

    if (error) throw error
    return data
  } catch (error) {
    console.error('Save Message Error:', error)
    return null
  }
}

/**
 * Get user chat history
 */
export async function getUserMessages(userId: string, limit = 50) {
  try {
    const { data, error } = await supabase
      .from('messages')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })
      .limit(limit)

    if (error) throw error
    return data
  } catch (error) {
    console.error('Get Messages Error:', error)
    return []
  }
}

/**
 * Save file metadata
 */
export async function saveFileMetadata(userId: string, fileData: any) {
  try {
    const { data, error } = await supabase
      .from('files')
      .insert({
        user_id: userId,
        ...fileData,
        created_at: new Date().toISOString(),
      })
      .select()

    if (error) throw error
    toast.success('File saved successfully')
    return data
  } catch (error) {
    console.error('Save File Error:', error)
    toast.error('Failed to save file')
    return null
  }
}

/**
 * Get user files
 */
export async function getUserFiles(userId: string) {
  try {
    const { data, error } = await supabase
      .from('files')
      .select('*')
      .eq('user_id', userId)
      .order('created_at', { ascending: false })

    if (error) throw error
    return data
  } catch (error) {
    console.error('Get Files Error:', error)
    return []
  }
}

/**
 * Verify Supabase tables exist
 */
export async function verifySupabaseTables() {
  const tables = ['user_profiles', 'messages', 'files']
  const results = {}

  for (const table of tables) {
    try {
      const { data, error } = await supabase
        .from(table)
        .select('count()')
        .limit(1)

      if (error) {
        results[table] = { exists: false, error: error.message }
      } else {
        results[table] = { exists: true, status: 'ready' }
      }
    } catch (error) {
      results[table] = { exists: false, error: String(error) }
    }
  }

  return results
}

/**
 * Complete Supabase health check
 */
export async function supabaseHealthCheck() {
  const checks = {
    connection: await testSupabaseConnection(),
    currentUser: await getCurrentUser(),
    tables: await verifySupabaseTables(),
    timestamp: new Date().toISOString(),
  }

  return checks
}
