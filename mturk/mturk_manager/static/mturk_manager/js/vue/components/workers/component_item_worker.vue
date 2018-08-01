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
                        <v-btn icon slot="activator">
                            <v-icon v-bind:color="status_block.color">{{ status_block.icon }}</v-icon>
                        </v-btn>
                        <span>{{ status_block.description }}</span>
                    </v-tooltip>
                </v-list-tile-content>
            </v-list-tile>
        </v-list>
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
        }
    },
    // watch: {
    //     'worker.is_blocked': function() {
    //         console.log(this.worker.is_blocked)
    //     },
    // },
    computed: {
        status_block() {
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
    },
    created: function() {
    },
    components: {
        ComponentBlockWorker,
    },
}
</script>