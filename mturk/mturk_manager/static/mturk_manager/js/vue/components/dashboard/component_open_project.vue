<template>
<v-layout wrap>
    <v-flex>
        <v-layout wrap>
            <v-flex class="text-xs-center">
                <div class="headline">Open Existing Project</div>
            </v-flex>
        </v-layout>
        <v-layout wrap>
            <v-flex>
                <v-text-field
                    v-model="search"
                    append-icon="search"
                    label="Search for Project"
                    hide-details
                    class="mb-2"
                ></v-text-field>
            </v-flex>
        </v-layout>
        <v-layout wrap>
            <v-flex>

                <!-- select-all -->
                <!-- v-bind:rows-per-page-items="items_per_page" -->
                    <!-- select-all -->
                <v-data-table
                    v-bind:pagination.sync="pagination"
                    v-bind:headers="list_headers"
                    v-bind:items="list_projects"
                    v-bind:search="search"
                >
                    <template
                        slot="items"
                        slot-scope="props"
                    >
                        <tr>
                            <td>
                                {{ props.item.name }}
                            </td>
                            <td class="text-xs-right">
                                <v-btn
                                    small
                                    color="primary"
                                    v-bind:to="{ name: 'settings_project', params: { slug_project: props.item.slug } }"
                                >Open</v-btn>
                                    <!-- v-bind:to="{ name: 'batches', params: { slug_project: props.item.slug } }" -->
                            </td>
                        </tr>
                    </template>
                </v-data-table>
            </v-flex>
        </v-layout>
    </v-flex>
</v-layout>
</template>

<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import _ from 'lodash';
    import table from '../../mixins/table';
export default {
    mixins: [
        table,
    ],
    name: 'component-open-project',
    data () {
        return {
            search: '',
            list_headers: [
                {
                    text: 'Name',
                    value: 'name',
                    align: 'left'
                },
                {
                    text: '',
                    value: '',
                    align: ''
                },
            ],
        }
    },
    computed: {
        list_projects() {
            return _.orderBy(this.object_projects, (project) => project.name);
        },
        ...mapGetters('moduleProjects', {
            'object_projects': 'get_object_projects',
        }),
    },
    methods: {
    },
    created: function() {
    },
    components: {
    },
}
</script>