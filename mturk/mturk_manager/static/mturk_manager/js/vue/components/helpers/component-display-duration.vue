<template>
<v-tooltip top>
    <span slot="activator">{{ duration_formatted }}</span>
    {{ duration.toISOString() }}
</v-tooltip>
</template>

<script>
    // import helpers from '../mixins/helpers';
export default {
    // mixins: [
    //     // helpers,
    // ],
    name: 'component-display-duration',
    props: {
    	duration: {
    		required: true,
    		type: Date|undefined,
    	}
    },
    computed: {
    	duration_formatted: function() {
    		if(this.duration === undefined)
    		{
    			return undefined;
    		} else{
    			// return this.datetime;
    			// console.log(typeof this.datetime)
    			// console.log(this.datetime)
    			return this.duration.humanize();
    			// return this.datetime.toLocaleString();
    		}
      //       return this.amount_formatted(this.amount);
    		// return this.amount.toFixed(2) + ' $';
    	},
    },
}
</script>