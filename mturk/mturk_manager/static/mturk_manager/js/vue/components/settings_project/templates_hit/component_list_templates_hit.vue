<template>
<div>
    <v-data-table
        v-bind:headers="list_headers"
        v-bind:items="list_templates_hit"
    >
        <template
            slot="items"
            slot-scope="props"
        >
            <tr>
                <td>
                    {{ props.item.name }}
                </td>
                <td>
                    <component-edit-template-hit
                        v-bind:key="`component-edit-template-hit-${props.item.id}`"
                        v-bind:template_hit_current="props.item"
                        v-on:edited="snackbar_edited = true"
                    ></component-edit-template-hit>
                    <component-delete-template-hit
                        v-bind:key="`component-delete-template-hit-${props.item.id}`"
                        v-bind:template_hit="props.item"
                        v-on:deleted="snackbar_deleted = true"
                    ></component-delete-template-hit>
                </td>
            </tr>
        </template>
        <template slot="no-data">
            <div class="text-xs-center">
                There exist no templates!
            </div>
        </template>
        <template slot="footer">
        <td colspan="100%">
        	<component-add-template-hit
                v-on:created="snackbar_created = true"
            ></component-add-template-hit>
        </td>
    </template>
    </v-data-table>

    <v-snackbar
        v-model="snackbar_deleted"
        v-bind:timeout="1500"
        bottom
    >
        <v-spacer></v-spacer>
        Deleted!
        <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
        v-model="snackbar_created"
        v-bind:timeout="1500"
        bottom
        color="success"
    >
        <v-spacer></v-spacer>
        Saved!
        <v-spacer></v-spacer>
    </v-snackbar>

    <v-snackbar
        v-model="snackbar_edited"
        v-bind:timeout="1500"
        bottom
        color="success"
    >
        <v-spacer></v-spacer>
        Updated!
        <v-spacer></v-spacer>
    </v-snackbar>
</div>
</template>

<script>
    import ComponentAddTemplateHit from './component_add_template_hit.vue';
    import ComponentDeleteTemplateHit from './component_delete_template_hit.vue';
    import ComponentEditTemplateHit from './component_edit_template_hit.vue';
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
    import {table} from '../../../mixins/table';
export default {
    mixins: [
        table,
    ],
    name: 'component-list-templates-hit',
    data () {
        return {
            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                },
                {
                    text: 'Actions',
                    value: '',
                    sortable: false,
                },
            ],

            snackbar_deleted: false,
            snackbar_edited: false,
            snackbar_created: false,
        }
    },
    computed: {
        list_templates_hit() {
        	// return [{name:"dawd"}]
            if(this.project_current.templates_hit == null) return [];

            return _.orderBy(this.project_current.templates_hit, (template) => template.name);
        },
        ...mapGetters('moduleProjects', {
            'project_current': 'get_project_current',
        }),
    },
    methods: {
    },
    created: function() {
    },
    components: {
        ComponentAddTemplateHit,
        ComponentDeleteTemplateHit,
    	ComponentEditTemplateHit,
    },
}
</script>