export default {
  methods: {
    amount_formatted(value) {
      if (isNaN(value)) {
        return "invalid";
      } else {
        return (value / 100.0).toFixed(2) + " $";
      }
    },
    try_money(value) {
      const number = this.try_number(value);
      if (isNaN(number)) {
        return number;
      } else {
        return number * 100;
      }
    },
    try_number(number) {
      const number_parsed = parseFloat(number);
      if (isNaN(number_parsed)) {
        console.log("######");
        return number;
      } else {
        return number_parsed;
      }
    }
  }
};
