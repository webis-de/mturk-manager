<template>
<span>{{ amount_formatted }}</span>
</template>

<script>
export default {
    name: 'component-display-money',
    props: {
    	amount: {
    		required: true,
    		type: Number,
    	}
    },
    computed: {
    	amount_formatted: function() {
    		return this.amount.toFixed(2) + ' $';
    	},
    },
}
</script>