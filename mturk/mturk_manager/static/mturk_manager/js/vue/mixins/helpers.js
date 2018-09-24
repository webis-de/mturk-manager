export default {
 	methods: {
 		try_number(number) {
			const number_parsed = parseFloat(number);
			if(isNaN(number_parsed))
			{
				return number;
			} else {
				return number_parsed;
			}
		},
	}
}