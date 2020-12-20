module.exports = {
  root: true,

  env: {
    node: true,
    browser: true,
  },

  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // import fix
    'import/extensions': ['error', 'always', {
      js: 'never',
      ts: 'never',
    }],
    // vuex fix
    'no-param-reassign': [
      'error',
      {
        props: true,
        ignorePropertyModificationsFor: [
          'acc', // for reduce accumulators
          'accumulator', // for reduce accumulators
          'e', // for e.returnvalue
          'ctx', // for Koa routing
          'req', // for Express requests
          'request', // for Express requests
          'res', // for Express responses
          'response', // for Express responses
          '$scope', // for Angular 1 scopes
          'staticContext', // for ReactRouter context
          'state',
        ],
      },
    ],
    'linebreak-style': 0,
    'max-len': [
      'error', {
        code: 120,
        comments: 150,
        ignoreStrings: true,
      },
    ],
    'import/prefer-default-export': 'off',
    'class-methods-use-this': 'off',
    // 'graphql/template-strings': [
    //   'error',
    //   {
    //     env: 'literal',
    //     projectName: 'app',
    //     schemaJsonFilepath: 'node_modules/.temp/graphql/schema.json',
    //   },
    // ],
    'no-shadow': 'off', // replaced by ts-eslint rule below
    '@typescript-eslint/no-shadow': 'error',
    /**
     * Vue-specific styles
     */
    'vue/v-bind-style': ['error', 'longform'],
    'vue/v-on-style': ['error', 'longform'],
    'vue/v-slot-style': ['error', 'longform'],
    'vue/html-self-closing': [
      'error', {
        html: {
          normal: 'never',
        },
      },
    ],
  },

  parserOptions: {
    parser: '@typescript-eslint/parser',
  },

  extends: [
    'plugin:vue/recommended',
    '@vue/airbnb',
    '@vue/typescript/recommended',
  ],

  plugins: [
    'graphql',
  ],
};
