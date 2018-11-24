import {store} from "../store/vuex";
import {Service_Workers} from "./service_worker";

class Class_Service_Assignments {
    async set_assignments({object_hits, data_batches, use_sandbox})
    {
        store.commit('moduleAssignments/set_assignments', {
            data_batches,
            object_hits,
            use_sandbox,
        });

        await Service_Workers.load_workers({
            list_ids: store.getters['moduleAssignments/set_ids_worker'],
            use_sandbox,
        });
    }

    async append_assignments({data_batches, object_hits, use_sandbox})
    {
        store.commit('moduleAssignments/set_assignments', {
            data_batches,
            object_hits,
            use_sandbox,
        });

        await Service_Workers.load_workers({
            list_ids: store.getters['moduleAssignments/set_ids_worker'],
            use_sandbox,
            append: true,
        });
    }
}

export const Service_Assignments = new Class_Service_Assignments();