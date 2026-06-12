import type { Config } from 'tailwindcss'

export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        core: {
          navy: '#111827',
          blue: '#2563EB',
          blueHover: '#1D4ED8',
          blueSoft: '#EFF6FF',
          teal: '#0F766E',
          tealSoft: '#F0FDFA',
        },
        app: {
          background: '#F9FAFB',
          surface: '#FFFFFF',
          muted: '#F3F4F6',
          border: '#E5E7EB',
          borderStrong: '#D1D5DB',
        },
        status: {
          success: '#15803D',
          successSoft: '#F0FDF4',
          warning: '#B45309',
          warningSoft: '#FFFBEB',
          danger: '#B91C1C',
          dangerSoft: '#FEF2F2',
          info: '#1D4ED8',
          infoSoft: '#EFF6FF',
          neutral: '#4B5563',
          neutralSoft: '#F3F4F6',
        },
      },
      borderRadius: {
        card: '0.75rem',
      },
      boxShadow: {
        card: '0 1px 2px 0 rgb(17 24 39 / 0.04)',
      },
      width: {
        sidebar: '260px',
      },
      height: {
        topbar: '64px',
      },
    },
  },
  plugins: [],
} satisfies Config
