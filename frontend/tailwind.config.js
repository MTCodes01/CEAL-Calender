/** @type {import('tailwindcss').Config} */
export default {
  darkMode: 'class',
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#f0f5ff',
          100: '#e0ebff',
          200: '#c2d6ff',
          300: '#94b8ff',
          400: '#5c91ff',
          500: '#3779e6', /* Requested rgb(55 121 230) is close to this, using as base */
          600: 'rgb(55 121 230)', /* Exact requested color */
          700: '#2b5ec2',
          800: '#264c9e',
          900: '#24417d',
          950: '#17284f',
        },
      },
    },
  },
  plugins: [],
}
