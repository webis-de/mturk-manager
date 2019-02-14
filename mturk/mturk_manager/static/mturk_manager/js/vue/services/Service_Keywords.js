import { Service_Endpoint } from "./service_endpoint";
import { store } from "../store/vuex";

class Class_Service_Keywords {
  async load() {
    if (store.getters["moduleKeywords/get_object_keywords"] == null) {
      const response = await Service_Endpoint.make_request({
        method: "get",
        url: {
          path: store.getters["get_url"]("url_api_keywords", "moduleKeywords")
        }
      });

      store.commit("moduleKeywords/set_keywords", response.data);
    }
  }
}

export const Service_Keywords = new Class_Service_Keywords();
