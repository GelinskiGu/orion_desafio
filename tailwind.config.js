/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme');


module.exports = {
  content: ["./templates/**/*.html", "./app.py", "./assets/css/style.css"],
  theme: {
    colors: {
      sky: colors.sky,
      indigo: colors.indigo,
      red: colors.red,
      white: colors.white,
      black: colors.black,
      gray: colors.gray,
    },
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

