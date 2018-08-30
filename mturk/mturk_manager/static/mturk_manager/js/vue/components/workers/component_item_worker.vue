<template>
    <!-- <div>wda</div> -->
    <v-card class="ma-1">
        <v-card-title
            class="py-0"
        >
            <h4>{{ worker.name }}</h4>
            <v-spacer></v-spacer>
            <v-menu 
                bottom 
                left
                v-bind:close-on-content-click="false"

            >
                <v-btn
                    slot="activator"
                    dark
                    icon
                     class="ma-0"
                >
                    <v-icon>more_vert</v-icon>
                </v-btn>

                <v-list>
                    <v-list-tile
                    >
                        <component-block-worker
                            v-bind:key="`component_block_worker_${worker.name}`"
                            v-bind:worker="worker"
                        ></component-block-worker>
                    </v-list-tile>

                </v-list>
            </v-menu>
        </v-card-title>
        <v-divider></v-divider>
        <v-list dense>
            <v-list-tile>
                <v-list-tile-content>Block Status:</v-list-tile-content>
                <v-list-tile-content class="align-end">

                    <v-tooltip left>
                        <v-btn icon v-bind:loading="status_block.icon == ''" slot="activator" class="ma-0">
                            <v-icon v-bind:color="status_block.color">{{ status_block.icon }}</v-icon>
                        </v-btn>
                        <span>{{ status_block.description }}</span>
                    </v-tooltip>
                </v-list-tile-content>
            </v-list-tile>
            <v-list-tile>
                <v-list-tile-content>#Assignments:</v-list-tile-content>
                <v-list-tile-content class="align-end">
                    <v-text-field
                        type="number"
                        single-line
                        reverse
                        v-bind:value="worker.counter_assignments"
                        v-on:change="changed_counter_assignments($event)"
                    ></v-text-field>
                </v-list-tile-content>
            </v-list-tile>
        </v-list>

        <v-snackbar
            v-model="show_snackbar"
            v-bind:timeout="1500"
            bottom
        >
            <!-- color="success" -->
            Saved!
            <v-btn
                flat
                v-on:click="show_snackbar = false"
            >
                Close
            </v-btn>
        </v-snackbar>
    </v-card>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import { STATUS_BLOCK } from '../../classes/enums.js';

    import ComponentBlockWorker from './component_block_worker.vue';
export default {
    name: 'component-item-worker',
    props: {
        worker: {
            type: Object,
            required: true,
        }
    },
    data () {
        return {
            show_snackbar: false,
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        status_block() {
            if(this.worker.is_blocked == undefined)
            {
                return {
                    description: 'Loading',
                    color: 'success',
                    icon: '',
                };
            }

            switch(this.worker.is_blocked)
            {
                case STATUS_BLOCK.NONE:
                    return {
                        description: 'Not Blocked',
                        color: 'success',
                        icon: 'check',
                    };
                case STATUS_BLOCK.SOFT:
                    return {
                        description: 'Soft Blocked',
                        color: 'warning',
                        icon: 'block',
                    };
                case STATUS_BLOCK.HARD:
                    return {
                        description: 'Hard Blocked',
                        color: 'error',
                        icon: 'block',
                    };
            }
        },
    },
    methods: {
        changed_counter_assignments(value) {
            this.set_show_progress_indicator(true);
            this.update_counter_assignments({
                worker: this.worker, 
                value
            }).then(() => {
                this.show_snackbar = true;
                this.set_show_progress_indicator(false);
            });
        },
        ...mapActions('moduleWorkers', {
            'update_counter_assignments': 'update_counter_assignments',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
    },
    components: {
        ComponentBlockWorker,
    },
}
</script>