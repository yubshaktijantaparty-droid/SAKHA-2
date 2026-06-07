/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Premium Gold Palette
        'gold': {
          50: '#fffbf0',
          100: '#fef5e7',
          200: '#fde9cf',
          300: '#fcdab8',
          400: '#ffc966',
          500: '#FFD700',
          600: '#FFB800',
          700: '#f4a600',
          800: '#cc8800',
          900: '#aa6d00',
        },
        // Slate/Navy Palette
        'slate': {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
        },
        // Legacy colors for compatibility
        'primary': '#FFD700',
        'accent': '#FFB800',
        'bg-dark': '#0F172A',
        'bg-secondary': '#1E293B',
        'text-primary': '#F8FAFC',
        'dark-bg': '#0F172A',
        'darker-bg': '#0A0F1F',
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'glass': 'linear-gradient(135deg, rgba(255, 215, 0, 0.1), rgba(255, 184, 0, 0.05))',
      },
      backdropBlur: {
        'xs': '2px',
        'sm': '4px',
        'md': '12px',
        'lg': '16px',
        'xl': '24px',
      },
      animation: {
        'pulse-slow': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'fade-in': 'fadeIn 0.3s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
      },
    },
  },
  darkMode: 'class',
  plugins: [
    // Glassmorphism plugin
    function({ addUtilities }) {
      const glassUtilities = {
        '.glass': {
          background: 'rgba(255, 215, 0, 0.1)',
          backdropFilter: 'blur(10px)',
          webkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 215, 0, 0.2)',
        },
        '.glass-dark': {
          background: 'rgba(15, 23, 42, 0.8)',
          backdropFilter: 'blur(10px)',
          webkitBackdropFilter: 'blur(10px)',
          border: '1px solid rgba(255, 215, 0, 0.1)',
        },
      }
      addUtilities(glassUtilities)
    },
  ],
}
