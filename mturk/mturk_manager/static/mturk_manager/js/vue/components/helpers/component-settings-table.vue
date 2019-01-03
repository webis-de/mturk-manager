<template>
<td>
    <v-btn
        color="primary"
        v-on:click="dialog = true"
    >
        Toggle Columns
    </v-btn>

	<v-dialog
		v-model="dialog"
        max-width="80%"
	>
        <v-card>
          	<v-card-title>
          		Download Batch(es)
          	</v-card-title>
          	<v-card-text>
				<v-layout>
					<v-flex>
						<v-checkbox
							v-for="column in array_columns"
							v-bind:label="column.text"
							v-bind:value="column.value"
							v-model="intern_array_columns_selected"
							hide-details
						></v-checkbox>
					</v-flex>
				</v-layout>
			    <v-layout row>
			        <v-flex>
					</v-flex>
				</v-layout>
	            <!-- append-icon="clear"
	            v-on:click:append="limit = 0" -->
          	</v-card-text>
        </v-card>
    </v-dialog>
</td>
</template>

<script>
    import { mapState, mapMutations, mapActions, mapGetters } from 'vuex';
    export default {
        name: "component-settings-table",
		props: {
	  		array_columns: {
	  		    type: Array,
				required: true,
			},
	  		array_columns_selected: {
	  		    type: Array,
				required: true,
			},
	  		array_columns_selected_initial: {
	  		    type: Array,
				required: true,
			}
		},
        data() {
            return {
                dialog: false,
				intern_array_columns_selected: this.array_columns_selected,
            }
        },
		// computed: {
        //     intern_array_columns_selected: {
        //         get() {
        //             return
		// 		},
		// 	}
		// },
		watch: {
	  		intern_array_columns_selected() {
	  		    this.$emit('change', this.intern_array_columns_selected);
			}
		},
    }
</script>

<style scoped>

</style>