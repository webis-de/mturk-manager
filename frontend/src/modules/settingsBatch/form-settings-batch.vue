<template>
  <div>
    <base-text-input
      v-bind:value="title"
      v-bind:validation="validation.title"
      v-bind:options="{
        label: 'Title',
      }"
      v-on:input="$emit('update:title', $event)"
    />

    <base-text-input
      v-bind:value="description"
      v-bind:validation="validation.description"
      v-bind:options="{
        label: 'Description',
      }"
      v-on:input="$emit('update:description', $event)"
    />

    <base-amount-input
      v-bind:value="reward"
      v-bind:validation="validation.reward"
      v-bind:options="{
        label: `Reward`,
      }"
      v-on:input="$emit('update:reward', $event)"
    />

    <base-number-input
      v-bind:value="countAssignments"
      v-bind:validation="validation.countAssignments"
      v-bind:options="{
        label: 'Number of assignments per HIT',
      }"
      v-on:input="$emit('update:countAssignments', $event)"
    />

    <base-duration-input
      v-bind:value="lifetime"
      v-bind:validation="validation.lifetime"
      v-bind:options="{
        label: 'Lifetime',
      }"
      v-on:input="$emit('update:lifetime', $event)"
    />

    <base-duration-input
      v-bind:value="duration"
      v-bind:validation="validation.duration"
      v-bind:options="{
        label: 'Duration',
      }"
      v-on:input="$emit('update:duration', $event)"
    />

    <base-input-select
      v-bind:value="templateWorker"
      v-bind:validation="validation.templateWorker"
      v-bind:options="{
        label: 'Worker template',
        items: templatesWorker,
        'item-key': 'id',
        'item-text': 'name',
        clearable: true,
      }"
      v-on:input="$emit('update:templateWorker', $event)"
    />

    <base-input-boolean
      v-bind:value="blockWorkers"
      v-bind:validation="validation.blockWorkers"
      v-bind:options="{
        label: 'Block workers',
      }"
      v-on:input="$emit('update:blockWorkers', $event)"
    />

    <base-input-combobox
      v-bind:value="keywords"
      v-bind:validation="validation.keywords"
      v-bind:options="{
        label: 'Keywords (Separated with TAB)',
        items: suggestionsKeywords,
        multiple: true,
      }"
      v-on:input="$emit('update:keywords', $event)"
    />

    <base-input-boolean
      v-bind:value="hasContentAdult"
      v-bind:validation="validation.hasContentAdult"
      v-bind:options="{
        label: 'Contains adult content',
      }"
      v-on:input="$emit('update:hasContentAdult', $event)"
    />

    <base-number-input
      v-bind:value="qualificationAssignmentsApproved"
      v-bind:validation="validation.qualificationAssignmentsApproved"
      v-bind:options="{
        label: 'Approved assignments',
        min: 0,
        max: 100,
      }"
      v-on:input="$emit('update:qualificationAssignmentsApproved', $event)"
    />

    <base-number-input
      v-bind:value="qualificationHitsApproved"
      v-bind:validation="validation.qualificationHitsApproved"
      v-bind:options="{
        label: 'Approved assignments',
        min: 0,
        max: 100,
      }"
      v-on:input="$emit('update:qualificationHitsApproved', $event)"
    />

    <base-input-combobox
      v-bind:value="qualificationLocale"
      v-bind:validation="validation.qualificationLocale"
      v-bind:options="{
        label: 'Locale (Separated with TAB)',
        items: suggestionsKeywords,
        multiple: true,
      }"
      v-on:input="$emit('update:qualificationLocale', $event)"
    />
  </div>
</template>

<script>
import { computed, defineComponent } from '@vue/composition-api';
import BaseTextInput from '@/modules/app/base/inputs/base-text-input.vue';
import { getValidator } from '@/modules/app/helpers';
import BaseNumberInput from '@/modules/app/base/inputs/base-number-input.vue';
import BaseAmountInput from '@/modules/app/base/inputs/base-amount-input.vue';
import BaseDurationInput from '@/modules/app/base/inputs/base-duration-input.vue';
import BaseInputSelect from '@/modules/app/base/inputs/base-input-select.vue';
import { store } from '@/store/vuex';
import BaseInputBoolean from '@/modules/app/base/inputs/base-input-boolean.vue';
import BaseInputCombobox from '@/modules/app/base/inputs/base-input-combobox.vue';

export default defineComponent({
  name: 'FormSettingsBatch',
  components: {
    BaseInputCombobox,
    BaseInputBoolean,
    BaseInputSelect,
    BaseDurationInput,
    BaseAmountInput,
    BaseNumberInput,
    BaseTextInput,
  },
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
      validator: getValidator({ number: true, null: true }),
    },
    countAssignments: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    lifetime: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    duration: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    templateWorker: {
      required: true,
      validator: getValidator({ object: true, null: true }),
    },
    blockWorkers: {
      required: true,
      validator: getValidator({ boolean: true }),
    },
    keywords: {
      required: true,
      validator: getValidator({
        object: true, array: true, null: true, undefined: true,
      }),
    },
    hasContentAdult: {
      required: true,
      validator: getValidator({ boolean: true }),
    },
    qualificationAssignmentsApproved: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    qualificationHitsApproved: {
      required: true,
      validator: getValidator({ number: true, null: true }),
    },
    qualificationLocale: {
      required: true,
      validator: getValidator({
        object: true, array: true, null: true, undefined: true,
      }),
    },
    validation: {
      required: false,
      type: Object,
      default: () => ({}),
    },
  },
  setup() {
    return {
      templatesWorker: computed(() => {
        const templatesWorker = store.getters['moduleTemplates/templatesWorkerSortedByName'];

        return templatesWorker === null ? [] : templatesWorker;
      }),
      suggestionsKeywords: computed(() => {
        const keywords = store.getters['moduleKeywords/get_object_keywords'];

        return keywords === null ? [] : Object.values(keywords);
      }),
    };
  },
});
</script>

<style scoped>

</style>
