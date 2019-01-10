<template>
<td>
    <v-btn
        color="primary"
        v-on:click="dialog = true"
		small
    >
        Toggle Columns
    </v-btn>

	<v-dialog
		v-model="dialog"
        max-width="80%"
	>
        <v-card>
          	<v-card-text>
				<v-layout>
					<v-flex>
						<v-checkbox
							class="ma-0"
							label="Toggle all"
							v-model="is_toggled_all"
							v-bind:indeterminate="is_indeterminate"
							hide-details
						></v-checkbox>
					</v-flex>
				</v-layout>
				<v-layout>
					<v-flex>
						<v-checkbox
							class="ma-0"
							v-for="column in array_columns"
							v-bind:key="column.value"
							v-bind:label="column.label || column.text"
							v-bind:value="column.value"
							v-model="intern_array_columns_selected"
							hide-details
						></v-checkbox>
					</v-flex>
				</v-layout>
			    <v-layout row class="mt-3">
			        <v-flex>
						<v-btn
							color="primary"
							v-on:click="function_reset(); dialog = false;"
						>Reset to default</v-btn>
						<v-btn
							flat
							v-on:click="dialog = false"
						>Cancel</v-btn>
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
    import _ from 'lodash';
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
			},
	  		function_reset: {
	  		    type: Function,
				required: true,
			},
		},
        data() {
            return {
                dialog: false,
				intern_array_columns_selected: this.array_columns_selected,
            }
        },
		computed: {
            is_toggled_all: {
                get() {
                    return _.size(this.array_columns) === _.size(this.intern_array_columns_selected)
                },
				set(is_checked) {
                    if(is_checked === true)
					{
						this.intern_array_columns_selected = _.map(this.array_columns, column => column.value);
					} else {
						this.intern_array_columns_selected = [];
					}
				}
			},
			is_indeterminate() {
                return !this.is_toggled_all && _.size(this.intern_array_columns_selected) !== 0;
			}
        //     intern_array_columns_selected: {
        //         get() {
        //             return
		// 		},
		// 	}
		},
		watch: {
            array_columns_selected() {
				this.intern_array_columns_selected = this.array_columns_selected;
			},
	  		intern_array_columns_selected() {
                // console.log('_.size(this.array_columns_selected)', _.size(this.array_columns_selected));
                // console.log('_.size(this.intern_array_columns_selected)', _.size(this.intern_array_columns_selected));
                // if(_.size(this.array_columns) === _.size(this.intern_array_columns_selected)) {
                //     this.is_toggled_all = true;
				// } else if(_.size(this.intern_array_columns_selected) === 0) {
                //     this.is_toggled_all = false;
				// }
	  		    this.$emit('change', this.intern_array_columns_selected);
			}
		},
    }
</script>

<style scoped>

</style>