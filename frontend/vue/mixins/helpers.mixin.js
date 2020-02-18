import Dinero from 'dinero.js';

export default {
  methods: {
    amount_formatted(value, messageInvalid = 'invalid', currency = '$') {
      if (Number.isInteger(value) === false) {
        return messageInvalid;
      }
      return Dinero({ amount: value }).toFormat('0,0.00');
      // return Dinero({ amount: value }).toFormat(`${currency}0,0.00`);
    },
    try_money(value) {
      const number = this.try_number(value);
      if (isNaN(number)) {
        return number;
      }
      return number * 100;
    },
    try_number(number) {
      const number_parsed = parseFloat(number);
      if (isNaN(number_parsed)) {
        console.log('######');
        return number;
      }
      return number_parsed;
    },
    tryInteger(value) {
      const valueParsed = parseInt(value, 10);
      if (isNaN(valueParsed)) {
        return value;
      }
      return valueParsed;
    },
  },
};
