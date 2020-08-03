import Vuetify from 'vuetify/lib';
import localforage from 'localforage';
import colors from 'vuetify/lib/util/colors';

export const vuetify = new Vuetify({
  theme: {
    themes: {
      light: {
        // primary: colors.deepPurple.darken2,
        // secondary: colors.grey,
        // accent: colors.grey,
      },
      dark: {
        // primary: colors.blue.darken1,
      //   secondary: colors.grey.darken4,
      //   // accent: colors.grey.darken4,
      },
    },
    dark: true,
  },
  // lang: {
  //   locales: { de },
  //   current: 'de',
  // },
  // theme: {
  //   themes: {
  //     light: {
  //       primary: '#011e40',
  //       secondary: '#009fe3',
  //     },
  //   },
  // },
});

localforage.getItem('isActiveModeLight').then((isActiveModeLight) => {
  vuetify.framework.theme.dark = !isActiveModeLight;
});
