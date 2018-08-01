<template>
    <!-- <v-slider
        v-model="status_block_new"
        label="Block status"
        always-dirty
        min="1"
        max="3"
        v-bind:tick-labels="labels_ticks"
        step="1"
        ticks="always"
        tick-size="1"
    ></v-slider> -->
<span>
    <v-radio-group v-model="status_block_new" row>
        <v-radio
            v-for="(n, i) in labels_ticks"
            v-bind:key="`${worker.name}_${n}`"
            v-bind:name="worker.name"
            v-bind:label="n"
            v-bind:value="values[i]"
        ></v-radio>
    </v-radio-group>
</span>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';
    import { STATUS_BLOCK } from '../../classes/enums.js';
export default {
    name: 'component-block-worker',
    props: {
        worker: {
            type: Object,
            required: true,
        }
    },
    data () {
        return {
            status_block_new: this.worker.is_blocked,
            labels_ticks: ['None', 'Soft', 'Hard'],
            values: [STATUS_BLOCK.NONE, STATUS_BLOCK.SOFT, STATUS_BLOCK.HARD]
        }
    },
    watch: {
        status_block_new: function() {
            this.set_show_progress_indicator(true);
            
            this.update_status_block({
                worker: this.worker,
                status_block_new: this.status_block_new,
            }).then(() => {
                this.set_show_progress_indicator(false);
            });
        },
    },
    computed: {
    },
    methods: {
        ...mapActions('moduleWorkers', {
            'update_status_block': 'update_status_block',
        }),
        ...mapActions(['set_show_progress_indicator']),
    },
    created: function() {
    },
    components: {
    },
}
</script>