import { createClient } from '@supabase/supabase-js'

// For development/demo mode, we're disabling Supabase temporarily
// Uncomment and configure the environment variables below when ready to enable authentication:
// const supabaseUrl = import.meta.env.VITE_SUPABASE_URL
// const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY

const supabaseUrl = import.meta.env.VITE_SUPABASE_URL || ''
const supabaseAnonKey = import.meta.env.VITE_SUPABASE_ANON_KEY || ''

// Force demo mode - only create client if both URL and key are provided AND not empty
let supabaseClient = null
let isSupabaseAvailable = false

try {
  // For demo mode, always set to null
  if (false) { // Temporarily force demo mode
    supabaseClient = createClient(supabaseUrl, supabaseAnonKey)
    isSupabaseAvailable = true
    console.log('✓ Supabase initialized')
  } else {
    console.log('ℹ️ DEMO MODE: Running with local authentication')
  }
} catch (error) {
  console.log('ℹ️ Supabase initialization failed - running in demo mode', error)
}

export const supabase = supabaseClient
export const hasSupabase = isSupabaseAvailable
