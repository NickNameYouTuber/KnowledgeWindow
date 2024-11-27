module.exports = {
  darkMode: 'class', // или 'media'
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Добавьте свои цвета для темной темы
        dark: {
          bg: '#1a202c',
          text: '#ffffff',
          input: '#000000', // Цвет текста в полях ввода в темной теме
        },
      },
    },
  },
  plugins: [],
}