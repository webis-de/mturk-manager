<template>
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
</template>

<script>
import required from 'vuelidate/src/validators/required';
import validations from '../mixins/validations.mixin';
import { AppService } from '../services/app.service';

export default {
  name: 'TheUpdateCredentials',
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

      await AppService.updateCredentials({
        url: this.url,
        token: this.token,
        router: this.$router,
      });

      this.loading = false;
      this.$emit('updated-credentials');
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

<style scoped>

</style>
