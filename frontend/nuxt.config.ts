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
      backend: "https://ai-backend.bank.green",
    },
  },
};
