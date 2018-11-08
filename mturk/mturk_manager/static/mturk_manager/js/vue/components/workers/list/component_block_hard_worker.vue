<template>
<span>
    <v-tooltip left>
        <v-btn 
            icon 
            small
            slot="activator" 
            class="ma-0"
            v-on:click="toggle()"
            v-bind:loading="is_updating" 
        >
            <v-icon 
                v-bind:color="color"
            >block</v-icon>
        </v-btn>
        <span>{{ text_tooltip }}</span>
    </v-tooltip>  

    <v-snackbar
        v-model="show_snackbar"
        v-bind:timeout="1000"
        color="info"
        bottom
    >
        Updated
        <v-btn
            flat
            v-on:click="show_snackbar = false"
        >
            Close
        </v-btn>
    </v-snackbar>  
</span>
<!-- <v-layout align-center>
    <v-flex mr-3>
        Block:
    </v-flex>
    <v-flex>
        <v-radio-group 
            v-bind:disabled="!is_enabled" 
            v-bind:value="status_block_current" 
            v-on:input="status_block_new = $event"
            row>
            <v-radio
                v-for="(n, i) in labels_ticks"
                v-bind:key="`${worker.name}_${n}`"
                v-bind:name="worker.name"
                v-bind:label="n"
                v-bind:value="values[i]"
                class="mb-0"
            ></v-radio>
        </v-radio-group>
    </v-flex>
</v-layout> -->
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    // import { STATUS_BLOCK } from '../../classes/enums.js';
export default {
    name: 'component-block-hard-worker',
    props: {
        worker: {
            type: Object,
            required: true,
        }
    },
    data () {
        return {
            // labels_ticks: ['None', 'Soft', 'Hard'],
            // values: [STATUS_BLOCK.NONE, STATUS_BLOCK.SOFT, STATUS_BLOCK.HARD],
            // is_updating: true,
            // status_block_current: undefined,
            // status_block_new: undefined,
            show_snackbar: false,
        }
    },
    watch: {
        // 'worker.is_blocked_hard': function(value) {
        //     if(value != undefined) {
        //         this.is_updating = false;
        //     }
        // }
        // 'worker.is_blocked': function(value) {
        //     this.status_block_current = value;

        // },
        // status_block_new(value_new) {
        //     this.set_show_progress_indicator(true);
        //     this.is_updating = true;

        //     this.status_block_current = value_new;

        //     this.update_status_block({
        //         worker: this.worker,
        //         status_block_new: value_new,
        //         status_block_old: this.worker.is_blocked,
        //     }).then(() => {
        //         this.is_updating = false;
        //         this.set_show_progress_indicator(false);
        //     });
        // },  
    },
    computed: {
        is_updating() {
            return this.worker.is_blocked_hard == undefined;
        },
        text_tooltip() {
            return this.worker.is_blocked_hard ? 'Is blocked globally': 'Is not blocked globally';
        },
        color() {
            return this.worker.is_blocked_hard ? 'error': 'grey';
        },
        // is_enabled() {
        //     return !this.is_updating && this.worker.is_blocked != undefined;
        // },
    },
    methods: {
        toggle() {
            this.set_show_progress_indicator(true);
            // this.is_updating = true;

            this.update_status_block_hard({
                worker: this.worker,
                is_blocked: !this.worker.is_blocked_hard,
                // status_block_new: value_new,
                // status_block_old: this.worker.is_blocked,
            }).then(() => {
                // this.is_updating = false;
                this.show_snackbar = true;
                this.set_show_progress_indicator(false);
            });
            // console.log(this.worker.is_blocked_hard);
        },
        ...mapActions('moduleWorkers', {
            'update_status_block_hard': 'update_status_block_hard',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
    },
    components: {
    },
}
</script>