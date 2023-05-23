/** @type {import('tailwindcss').Config} */
const colors = require('tailwindcss/colors')
const defaultTheme = require('tailwindcss/defaultTheme');


module.exports = {
  content: ["./templates/**/*.html", "./app.py", "./assets/css/style.css", "./static/src/**/*.js", "./node_modules/flowbite/**/*.js"],
  theme: {
    colors: {
      sky: colors.sky,
      indigo: colors.indigo,
      red: colors.red,
      white: colors.white,
      black: colors.black,
      gray: colors.gray,
      background_primary: '#001B48',
      background_secondary: '#02457A',
      middle_color: '#018ABE',
      text_primary: '#D6EBEE',
      text_secondary: '#97CADB',
    },
    extend: {
      fontFamily: {
        sans: ['Inter var', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('flowbite/plugin'),
  ],
}

