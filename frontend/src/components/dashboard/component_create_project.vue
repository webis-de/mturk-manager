<template>
  <form v-on:submit.prevent="save">
    <v-row no-gutters>
      <v-col>
        <v-row no-gutters>
          <v-col>
            <span class="headline">Create New Project</span>
          </v-col>
        </v-row>
        <v-row
          dense
          align="center"
        >
          <v-col>
            <v-text-field
              v-bind:value="name"
              label="Name"
              v-bind:error-messages="errors"
              v-bind:loading="$v.$pending"
              v-on:input="
                update_name($event);
                name_instant = $event;
              "
            />
          </v-col>
          <v-col
            class="shrink"
          >
            <v-btn
              type="submit"
              v-bind:loading="is_creating"
              color="primary"
              v-bind:disabled="
                $v.pending || $v.$invalid || name_instant.trim() === '' || disabled
              "
            >
              Create
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </form>
</template>

<script>
import { mapActions } from 'vuex';
import _ from 'lodash';

import { required } from 'vuelidate/lib/validators';
import { Service_Projects } from '../../services/service_projects';

export default {
  name: 'ComponentCreateProject',
  data() {
    return {
      snackbar_created: false,
      name: '',
      // name: undefined,
      is_creating: false,
      name_instant: '',
      disabled: true,
    };
  },
  computed: {
    errors() {
      const errors = [];
      if (!this.$v.name.$dirty || this.$v.$pending) {
        return errors;
      }

      if (this.$v.name.required === false) {
        errors.push('Required!');
      }
      if (this.$v.name.is_unique === false) {
        errors.push('Name has to be unique!');
      }

      return errors;
    },
  },
  watch: {
    name_instant() {
      this.disabled = true;
      this.is_creating = true;
    },
  },
  methods: {
    save() {
      this.is_creating = true;
      Service_Projects.create_project(this.name).then((project) => {
        this.name = '';
        this.$v.$reset();
        this.is_creating = false;
        this.$router.push({
          name: 'project',
          params: { slug_project: project.slug },
        });
      });
    },
    update_name: _.debounce(function (value) {
      this.name = value.trim();
      this.$v.name.$touch();
    }, 500),
    ...mapActions('moduleProjects', {
      validate_name: 'validate_name',
      create_project: 'create_project',
    }),
  },
  validations: {
    name: {
      required,
      async is_unique(name) {
        this.is_creating = false;
        if (name === '' || name === undefined) {
          this.disabled = false;
          return true;
        }

        const response = await Service_Projects.validate_name(name);
        if (response.data === true) {
          this.disabled = false;
        }
        return response.data;
      },
    },
  },
};
</script>
