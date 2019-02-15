<template>
  <v-container>
    <v-layout fill-height column justify-center>
      <v-flex shrink>
        <v-layout justify-center>
          <v-flex shrink class="text-xs-center">
            <v-text-field v-model="url" label="URL" autofocus></v-text-field>
            <v-text-field v-model="token" label="Token"></v-text-field>

            <v-btn
              v-on:click="save"
              v-bind:disabled="$v.pending || $v.$invalid"
              color="primary"
              >Save</v-btn
            >
          </v-flex>
        </v-layout>
      </v-flex>
    </v-layout>
  </v-container>
</template>

<script>
import required from 'vuelidate/src/validators/required';
import { mapActions } from 'vuex';
import validations from '../../mixins/validations';
import { Service_App } from '../../services/service.app';

export default {
  name: 'add-credentials',
  mixins: [validations],
  data() {
    return {
      url: '',
      token: '',
    };
  },
  methods: {
    async save() {
      if (!this.url.startsWith('http')) {
        this.url = `http://${this.url}`;
      }

      await this.set_credentials({
        url: this.url,
        token: this.token,
      });

      await Service_App.init();

      this.$router.push({ name: 'dashboard' });
    },
    ...mapActions('module_app', ['set_credentials']),
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
