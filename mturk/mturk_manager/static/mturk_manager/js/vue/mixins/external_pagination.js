export const external_pagination = {
    data() {
        return {
            items_total: undefined,
        }
    },
    methods: {
        pagination_updated() {},
    },
    watch: {
        pagination: {
            handler(pagination) {
                this.pagination_updated(pagination);
            },
            deep: true
        }
    },
}