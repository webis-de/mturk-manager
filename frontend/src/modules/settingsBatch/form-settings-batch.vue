<template>
  <div>
    <!--    {{ validation }}-->
    <base-text-field
      v-bind:value="title"
      v-bind:validation="validation.title"
      v-bind:options="{
        label: 'Title',
      }"
      v-on:input="$emit('update:title', $event)"
    />

    <base-text-field
      v-bind:value="description"
      v-bind:validation="validation.description"
      v-bind:options="{
        label: 'Description',
      }"
      v-on:input="$emit('update:description', $event)"
    />

    <base-text-field
      v-bind:value="reward"
      v-bind:validation="validation.reward"
      v-bind:options="{
        label: 'Reward',
        type: 'number'
      }"
      v-on:input="$emit('update:reward', $event)"
    />
  </div>
</template>

<script>
import { defineComponent } from '@vue/composition-api';
import BaseTextField from '@/modules/app/base/inputs/base-text-field.vue';
import { getValidator } from '@/modules/app/helpers';

export default defineComponent({
  name: 'FormSettingsBatch',
  components: { BaseTextField },
  props: {
    title: {
      required: true,
      validator: getValidator({ string: true, null: true }),
    },
    description: {
      required: true,
      validator: getValidator({ string: true, null: true }),
    },
    reward: {
      required: true,
      validator: getValidator({ number: true, undefined: true }),
    },
    validation: {
      required: false,
      type: Object,
      default: () => ({}),
    },
  },
});
</script>

<style scoped>

</style>
