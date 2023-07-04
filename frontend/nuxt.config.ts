export default {
  postcss: {
    plugins: {
      tailwindcss: {},
      autoprefixer: {},
    },
  },
  vue: {
    compilerOptions: {
      directiveTransforms: {
        clickaway: () => ({
          props: [],
          needRuntime: true,
        }),
      },
    },
  },
  css: ["@/assets/css/main.css"],
  runtimeConfig: {
    public: {
      backend: "http://127.0.0.1:5000",
    },
  },
};
