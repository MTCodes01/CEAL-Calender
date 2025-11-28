/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f5f7ff',
          100: '#ebf0fe',
          200: '#d6e1fd',
          300: '#b3c9fb',
          400: '#8aa7f7',
          500: '#667eea',
          600: '#5568d3',
          700: '#4553b8',
          800: '#3a4595',
          900: '#333b78',
        },
      },
    },
  },
  plugins: [],
}
