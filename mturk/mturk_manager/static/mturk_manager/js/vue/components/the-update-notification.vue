<template>
    <v-snackbar
        top
        v-bind:value="version_api > version_app"
        v-bind:timeout="0"
        color="info"
        >
        <v-spacer></v-spacer>Update Available!<v-spacer></v-spacer>
    </v-snackbar>
</template>

<script>
    import {mapState} from "vuex";

    export default {
        name: "the-update-notification",
        data() {
            return {}
        },
        computed: {
            ...mapState('module_app', [
                'version_api',
                'version_app',
            ]),
        }
    }
</script>

<style scoped>

</style>