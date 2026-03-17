/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#fcfaf8", // Soft beige/white
        foreground: "#2d2d2d",
        brand: {
          sage: "#8da399",
          "sage-light": "#b8c5bf",
          "sage-dark": "#6a7f76",
          beige: "#f5f0e1",
          purple: "#9b8da3",
          "purple-light": "#c0b8c5",
        },
        neutral: {
          50: "#f9f9f9",
          100: "#f3f3f3",
          200: "#e5e5e5",
          300: "#d4d4d4",
          400: "#a3a3a3",
          500: "#737373",
        }
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        xl: "1rem",
        "2xl": "1.5rem",
      },
    },
  },
  plugins: [],
}
