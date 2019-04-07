const MESSAGES_DEFAULT = {
  required: 'Required!',
  minValue: 'Too low!',
  maxValue: 'Too high!',
  contains_form_injection: "'data-inject_input_forms' is missing!",
  contains_injection_assignments: "'data-inject_assignments' is missing!",
  is_unique: 'Has to be unique!',
  validBudget: 'Invalid Budget',
};

export default {
  data() {
    return {
      validation_errors: {},
    };
  },
  watch: {},
  methods: {
    validate(name_field, messages = {}) {
      const foo = name_field.split('.');
      const errors = [];

      let bar;
      if (foo.length == 1) {
        bar = this.$v[foo[0]];
      } else {
        bar = this.$v[foo[0]][foo[1]];
      }

      if (!bar.$dirty || this.$v.$pending) {
        return errors;
      }

      for (const name_requirement in bar.$params) {
        if (bar[name_requirement] == false) {
          if (messages.hasOwnProperty(name_requirement)) {
            errors.push(messages[name_requirement]);
          } else if (MESSAGES_DEFAULT.hasOwnProperty(name_requirement)) {
            errors.push(MESSAGES_DEFAULT[name_requirement]);
          } else {
            errors.push('Error!');
          }
        }
      }
      if (foo.length == 1) {
        this.validation_errors[foo[0]] = errors;
      } else {
        this.validation_errors[foo[0]][foo[1]] = errors;
        // bar = this.$v[foo[0]][foo[1]];
      }
    },
    v_has_children(foo) {
      // console.log(foo[Object.keys(foo)[0]])
      return foo[Object.keys(foo)[0]] === null;
    },
  },
  created() {
    for (const name_field in this.$v.$params) {
      // console.log(name_field)
      // console.log(this.$v[name_field])
      // console.log(this.$v[name_field].$params)
      if (this.v_has_children(this.$v[name_field].$params)) {
        // console.log('has_children')
        for (const foo in this.$v[name_field].$params) {
          this.$set(this.validation_errors, name_field, {});
          this.$set(this.validation_errors[name_field], foo, []);
          // console.log(this.validation_errors)
          // this.$set(this.validation_errors, `${name_field}.${foo}`, []);
          this.$watch(`${name_field}.${foo}`, () => this.validate(`${name_field}.${foo}`));
          // console.log(foo)
        }
      } else {
        this.$set(this.validation_errors, name_field, []);
        this.$watch(name_field, () => this.validate(name_field));
      }

      // for(let foo in this.$v[name_field].$params)
      // {
      // 	console.log(foo)
      // }
      // let bar = this.foo != undefined ? this.foo+'.' : '';
      // bar += name_field
      // console.log(this.foo)
      // console.log(bar)
    }
    // console.log(this.validation_errors)
    // console.log('äääääääääääääääääääääääääääääääääääääääääääää')
  },
  validations: {},
};
