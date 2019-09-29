<template>
  <v-container class="fill-height">
    <v-row
      class="fill-height"
      justify="center"
    >
      <v-col cols="4">
        <v-row
          class="fill-height"
          align="center"
        >
          <v-col
            class="text-center"
          >
            <v-form
              v-on:submit.prevent="save"
            >
              <v-text-field
                v-model="url"
                label="URL"
                autofocus
              />

              <v-text-field
                v-model="token"
                label="Token"
              />

              <v-btn
                type="submit"
                v-bind:disabled="$v.pending || $v.$invalid"
                color="primary"
                v-bind:loading="loading"
              >
                Save
              </v-btn>
            </v-form>
          </v-col>
        </v-row>
      </v-col>
    </v-row>

    <v-snackbar
      v-bind:value="false"
      v-bind:timeout="0"
      color="error"
      top
    >
      Cannot connect to the database! Please check the credentials
    </v-snackbar>
  </v-container>
</template>

<script>
import required from 'vuelidate/src/validators/required';
import validations from '../../mixins/validations.mixin';
import { Service_App } from '../../services/service.app';

export default {
  name: 'AddCredentials',
  mixins: [validations],
  data() {
    return {
      url: this.$store.state.module_app.url_api,
      token: this.$store.state.module_app.token_instance,

      loading: false,
    };
  },
  methods: {
    async save() {
      this.loading = true;

      await Service_App.updateCredentials({
        url: this.url,
        token: this.token,
        router: this.$router,
      });
    },
  },
  validations: {
    url: {
      required,
    },
    token: {
      required,
    },
  },
};
</script>

<style scoped></style>
