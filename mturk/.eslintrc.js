module.exports = {
  root: true,

  env: {
    node: true,
    browser: true,
  },

  rules: {
    'no-console': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    'no-debugger': process.env.NODE_ENV === 'production' ? 'error' : 'off',
    // own vue style fix
    'vue/v-bind-style': ['error', 'longform'],
    'vue/v-on-style': ['error', 'longform'],
    // import fix
    'import/extensions': ['error', 'always', {
      'js': 'never',
      'vue': 'never'
    }],
    // vuex fix
    'no-param-reassign': [
      'error',
      {
        'props': true,
        'ignorePropertyModificationsFor': [
          'state',
        ]
      }
    ],
    'linebreak-style': 0
  },

  parserOptions: {
    parser: 'babel-eslint',
  },

  extends: [
    'plugin:vue/recommended',
    '@vue/airbnb',
  ],
};
