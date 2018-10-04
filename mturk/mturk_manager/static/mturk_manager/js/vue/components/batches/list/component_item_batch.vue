<template>
    <!-- <div>wda</div> -->
    <tr>
        <td>
            <v-checkbox
                v-model="props.selected"
                primary
                hide-details
            ></v-checkbox>
        </td>
        <td 
            v-on:click="props.expanded = !props.expanded"
            class="text-xs-center"
        >
            {{ props.item.name }}
        </td>
        <td 
            v-on:click="props.expanded = !props.expanded"
            class="text-xs-center"
        >
            {{ props.item.hits.length }}
        </td>
        <td 
            v-on:click="props.expanded = !props.expanded"
            class="text-xs-center"
        >
            {{ props.item.count_assignments }}
        </td>
    </tr>
</template>
<script>
    import { mapState, mapActions, mapGetters } from 'vuex';

export default {
    name: 'component-item-batch',
    props: {
        props: {
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

        // status_block() {
        //     if(this.worker.is_blocked == undefined)
        //     {
        //         return {
        //             description: 'Loading',
        //             color: 'success',
        //             icon: '',
        //         };
        //     }

        //     switch(this.worker.is_blocked)
        //     {
        //         case STATUS_BLOCK.NONE:
        //             return {
        //                 description: 'Not Blocked',
        //                 color: 'success',
        //                 icon: 'check',
        //             };
        //         case STATUS_BLOCK.SOFT:
        //             return {
        //                 description: 'Soft Blocked',
        //                 color: 'warning',
        //                 icon: 'block',
        //             };
        //         case STATUS_BLOCK.HARD:
        //             return {
        //                 description: 'Hard Blocked',
        //                 color: 'error',
        //                 icon: 'block',
        //             };
        //     }
        // },
        ...mapGetters(['get_show_progress_indicator']),
    },
    methods: {
    },
    components: {
    },
}
</script>

<style lang="scss" scoped>
    td {
        height: unset !important;
    }
    td .v-input--selection-controls {
        padding: unset;
    }
</style>