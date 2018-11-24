<template>
<span>{{ datetime_formatted }}</span>
</template>

<script>
    // import helpers from '../mixins/helpers';
export default {
    // mixins: [
    //     // helpers,
    // ],
    name: 'component-display-datetime',
    props: {
    	datetime: {
    		required: true,
    		type: Date|undefined,
    	}
    },
    computed: {
    	datetime_formatted: function() {
    		if(this.datetime == undefined)
    		{
    			return undefined;
    		} else{
    			// return this.datetime;
    			// console.log(typeof this.datetime)
    			// console.log(this.datetime)
    			return this.datetime.toLocaleString();
    		}
      //       return this.amount_formatted(this.amount);
    		// return this.amount.toFixed(2) + ' $';
    	},
    },
}
</script>