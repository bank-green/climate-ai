export default {
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  css: ["@/assets/css/main.css"],
  runtimeConfig: {
    public: {
      backend: "http://127.0.0.1:5000",
    },
  },
};
