(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["workers"],{"1c4c":function(e,t,r){"use strict";var a=r("9b43"),n=r("5ca1"),o=r("4bf8"),s=r("1fa8"),i=r("33a4"),c=r("9def"),l=r("f1ae"),u=r("27ee");n(n.S+n.F*!r("5cc5")(function(e){Array.from(e)}),"Array",{from:function(e){var t,r,n,d,_=o(e),p="function"==typeof this?this:Array,m=arguments.length,h=m>1?arguments[1]:void 0,f=void 0!==h,b=0,k=u(_);if(f&&(h=a(h,m>2?arguments[2]:void 0,2)),void 0==k||p==Array&&i(k))for(t=c(_.length),r=new p(t);t>b;b++)l(r,b,f?h(_[b],b):_[b]);else for(d=k.call(_),r=new p;!(n=d.next()).done;b++)l(r,b,f?s(d,h,[n.value,b],!0):n.value);return r.length=b,r}})},2677:function(e,t,r){"use strict";r.d(t,"a",function(){return c});var a=r("8654"),n=r("a844"),o=r("7cf7"),s=r("ab6d"),i=r("d9bd"),c={functional:!0,$_wrapperFor:a["a"],props:{textarea:Boolean,multiLine:Boolean},render:function(e,t){var r=t.props,l=t.data,u=t.slots,d=t.parent;Object(s["a"])(l);var _=Object(o["a"])(u(),e);return r.textarea&&Object(i["d"])("<v-text-field textarea>","<v-textarea outline>",c,d),r.multiLine&&Object(i["d"])("<v-text-field multi-line>","<v-textarea>",c,d),r.textarea||r.multiLine?(l.attrs.outline=r.textarea,e(n["a"],l,_)):e(a["a"],l,_)}}},"2e29":function(e,t,r){},"38b4":function(e,t,r){"use strict";r.d(t,"a",function(){return m});r("96cf");var a=r("3b8d"),n=r("d225"),o=r("b0b4"),s=r("308d"),i=r("6bb5"),c=r("4e2b"),l=r("256d"),u=r("8a26"),d=r("6956"),_=r("d4cc"),p=function(e){function t(){return Object(n["a"])(this,t),Object(s["a"])(this,Object(i["a"])(t).apply(this,arguments))}return Object(c["a"])(t,e),Object(o["a"])(t,[{key:"create",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(t){var r,a;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return r=u["a"].state.module_app.use_sandbox,a=u["a"].getters["moduleProjects/get_project_current"],e.next=4,l["a"].make_request({method:"post",url:{path:u["a"].getters.get_url("url_api_projects_batches","moduleBatches"),use_sandbox:r,project:a},data:t});case 4:e.sent;case 5:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"sync_mturk",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(){var t,r,a;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return t=u["a"].state.module_app.use_sandbox,r=u["a"].getters["moduleProjects/get_project_current"],u["a"].commit("moduleBatches/set_is_syncing_mturk",!0),e.next=5,l["a"].make_request({method:"patch",url:{path:u["a"].getters.get_url("url_api_projects_batches","moduleBatches"),project:r,use_sandbox:t}});case 5:a=e.sent,a.data,u["a"].commit("moduleBatches/set_is_syncing_mturk",!1);case 8:case"end":return e.stop()}},e)}));function t(){return e.apply(this,arguments)}return t}()},{key:"load_page",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(r,a){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return n=u["a"].state.module_app.use_sandbox,e.abrupt("return",t.loadPage({pagination:r,filters:a,url:{path:u["a"].getters.get_url("url_api_projects_batches","moduleBatches"),use_sandbox:n,project:u["a"].getters["moduleProjects/get_project_current"]},callback:function(e){u["a"].commit("moduleBatches/set_batches",{data:e.data.data,use_sandbox:n})}}));case 2:case"end":return e.stop()}},e)}));function r(t,r){return e.apply(this,arguments)}return r}()},{key:"get_batch",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(t){var r;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,l["a"].make_request({method:"get",url:{path:u["a"].getters.get_url("url_api_projects_batches","moduleBatches"),project:u["a"].getters["moduleProjects/get_project_current"],value:t}});case 2:return r=e.sent,e.abrupt("return",new d["a"](r.data));case 4:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"download",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(t){var r,a;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,l["a"].make_request({method:"get",url:{path:u["a"].getters.get_url("url_api_projects_batches_download","moduleBatches"),project:u["a"].getters["moduleProjects/get_project_current"]},params:t,options:{responseType:"blob"}});case 2:r=e.sent,a=window.document.createElement("a"),a.href=window.URL.createObjectURL(r.data,{type:"text/plain"}),a.download="filename.csv",document.body.appendChild(a),a.click(),document.body.removeChild(a);case 9:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"get_download_info",value:function(){var e=Object(a["a"])(regeneratorRuntime.mark(function e(t){var r;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return e.next=2,l["a"].make_request({method:"get",url:{path:u["a"].getters.get_url("url_api_projects_batches_download_info","moduleBatches"),project:u["a"].getters["moduleProjects/get_project_current"]},params:t});case 2:return r=e.sent,console.log("response",r.data),e.abrupt("return",r);case 5:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"isValidCSV",value:function(){return null!==u["a"].state.moduleBatches.objectCSVParsed&&0===u["a"].state.moduleBatches.objectCSVParsed.errors.length}}]),t}(_["a"]),m=new p},"63aa":function(e,t,r){"use strict";var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-flex",e._b({},"v-flex",e.breakpoints,!1),[r("v-card",{attrs:{color:(e.filtersActive.hasOwnProperty(e.nameFilter),"secondary")}},[r("v-card-title",{staticClass:"px-2 py-1"},[r("v-layout",[r("v-flex",{staticClass:"subheading"},[r("span",{class:{"warning--text":e.filtersActive.hasOwnProperty(e.nameFilter)}},[e._v("\n              "+e._s(e.title)+"\n          ")])]),r("v-flex",{attrs:{shrink:""}},[e._t("header"),r("v-switch",{staticClass:"mt-0 pt-0",attrs:{label:"Exclude","hide-details":"","input-value":e.isExcluded},on:{change:function(t){return e.$set(e.filters,e.nameExcluded,t)}}})],2)],1)],1),r("v-card-text",{staticClass:"px-2 pt-0 pb-2"},[e._t("default")],2)],1)],1)},n=[],o={name:"BaseTableFilter",props:{filtersActive:{required:!0,type:Object},filters:{required:!0,type:Object},title:{required:!0,type:String},nameFilter:{required:!0,type:String},breakpoints:{required:!1,type:Object,default:function(){}}},computed:{nameExcluded:function(){return"".concat(this.nameFilter,"Exclude")},isExcluded:function(){return!!this.filters.hasOwnProperty(this.nameExcluded)&&this.filters[this.nameExcluded]}}},s=o,i=r("2877"),c=r("6544"),l=r.n(c),u=r("b0af"),d=r("99d9"),_=r("12b2"),p=r("0e8f"),m=r("a722"),h=r("b73d"),f=Object(i["a"])(s,a,n,!1,null,"15737898",null);t["a"]=f.exports;l()(f,{VCard:u["a"],VCardText:d["b"],VCardTitle:_["a"],VFlex:p["a"],VLayout:m["a"],VSwitch:h["a"]})},7165:function(e,t,r){"use strict";var a=r("7b2a"),n=r.n(a);n.a},"7b2a":function(e,t,r){},"7e63":function(e,t,r){},a581:function(e,t,r){"use strict";r.r(t);var a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",[r("h1",{staticClass:"headline"},[e._v("Workers")]),r("table-workers")],1)},n=[],o=r("2f62"),s=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("base-table",{attrs:{"name-vuex-module":"moduleWorkers","name-state-pagination":e.nameStatePagination,"name-local-storage-pagination":e.nameLocalStoragePagination,"function-load-page":e.loadPage,"array-items":e.array_items,"name-local-storage-columns-selected":e.nameLocalStorageColumnsSelected,"name-state-columns":e.nameStateColumns,"name-state-columns-selected":e.nameStateColumnsSelected,"name-state-columns-selected-initial":e.nameStateColumnsSelectedInitial,"name-state-items-selected":e.nameStateItemsSelected,"function-set-items-selected":e.function_set_items_selected,"function-clear-items-selected":e.function_clear_items_selected,filters:e.filtersComputed,"filters-default":e.filtersDefaultComputed,"set-state":e.setState,"name-state-filters":"objectFiltersGeneral","name-local-storage-filters":"filtersWorkersGeneral"},scopedSlots:e._u([{key:"default",fn:function(t){var a=t.props,n=t.array_columns_selected,o=t.isCondensed;return[r("component-item-worker",{attrs:{props:a,array_columns_selected:n,show_links:e.showLinks,"is-condensed":o}})]}},{key:"filters",fn:function(e){var t=e.filters,a=e.filtersActive;return[r("filters-table-workers",{attrs:{filters:t,"filters-active":a}})]}},{key:"actions",fn:function(){return[e._t("actions")]},proxy:!0}],null,!0)})},i=[],c=r("cebc"),l=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("tr",[r("td",{style:e.stylesCell},[r("v-checkbox",{attrs:{primary:"","hide-details":""},model:{value:e.props.selected,callback:function(t){e.$set(e.props,"selected",t)},expression:"props.selected"}})],1),e.set_columns_selected.has("id_worker")?r("td",{staticClass:"text-xs-left",style:e.stylesCell},[e._v("\n    "+e._s(e.props.item.id_worker)+"\n  ")]):e._e(),e.set_columns_selected.has("counter_assignments")?r("td",{staticClass:"text-xs-center",style:e.stylesCell},[r("component-limit-assignments",{key:"component_limit_assignments_"+e.props.item.id_worker,attrs:{worker:e.worker}})],1):e._e(),e.set_columns_selected.has("block_soft")?r("td",{staticClass:"text-xs-center",style:e.stylesCell},[r("component-block-soft-worker",{key:"component_block_soft_worker_"+e.worker.id_worker,attrs:{worker:e.worker}})],1):e._e(),e.set_columns_selected.has("block_soft_hard")?r("td",{staticClass:"text-xs-center",style:e.stylesCell},[r("component-block-global-worker",{key:"component_block_global_worker_"+e.worker.id_worker,attrs:{worker:e.worker}})],1):e._e(),e.set_columns_selected.has("block_hard")?r("td",{staticClass:"text-xs-center",style:e.stylesCell},[r("component-block-hard-worker",{key:"component_block_hard_worker_"+e.worker.id_worker,attrs:{worker:e.worker}})],1):e._e()])},u=[],d=(r("ac6a"),r("5df3"),r("4f7f"),function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("span",[r("v-tooltip",{attrs:{left:""}},[r("v-btn",{staticClass:"ma-0",attrs:{slot:"activator",icon:"",small:"",loading:e.is_updating},on:{click:function(t){return e.toggle()}},slot:"activator"},[r("v-icon",{attrs:{color:e.color}},[e._v("block")])],1),r("span",[e._v(e._s(e.text_tooltip))])],1),r("v-snackbar",{attrs:{timeout:1e3,color:"info",bottom:""},model:{value:e.show_snackbar,callback:function(t){e.show_snackbar=t},expression:"show_snackbar"}},[e._v("\n      Updated\n      "),r("v-btn",{attrs:{flat:""},on:{click:function(t){e.show_snackbar=!1}}},[e._v("\n        Close\n      ")])],1)],1)}),_=[],p=(r("1c4c"),r("96cf"),r("3b8d")),m=r("d225"),h=r("b0b4"),f=r("308d"),b=r("6bb5"),k=r("4e2b"),g=r("2ef0"),w=r.n(g),v=r("8a26"),x=r("256d"),y=r("38b4"),j=r("d4cc"),O=function(e){function t(){return Object(m["a"])(this,t),Object(f["a"])(this,Object(b["a"])(t).apply(this,arguments))}return Object(k["a"])(t,e),Object(h["a"])(t,[{key:"load_workers",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(t){var r,a,n,o,s,i,c;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:if(r=t.list_ids,a=t.use_sandbox,n=t.append,0!==w.a.size(r)){e.next=3;break}return e.abrupt("return");case 3:return e.next=5,x["a"].make_request({method:"patch",url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),use_sandbox:a,project:v["a"].getters["moduleProjects/get_project_current"]},data:Array.from(r)});case 5:return o=e.sent,s=o.data,!0===n?v["a"].commit("moduleWorkers/append_workers",{data_workers:s,use_sandbox:a}):v["a"].commit("moduleWorkers/set_workers",{data_workers:s,use_sandbox:a}),y["a"].add_workers({object_workers:v["a"].getters["moduleWorkers/get_object_workers"](a),use_sandbox:a}),e.next=11,x["a"].make_request({method:"patch",url:{path:v["a"].getters.get_url("url_api_workers_get_blocks_hard","moduleWorkers"),use_sandbox:a,project:v["a"].getters["moduleProjects/get_project_current"]},data:Array.from(r)});case 11:i=e.sent,c=i.data,v["a"].commit("moduleWorkers/set_blocks_hard",{array_blocks_hard:c,use_sandbox:a});case 14:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"update_status_block_soft",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(t){var r,a,n,o,s;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return r=t.worker,a=t.is_blocked,n=v["a"].state.module_app.use_sandbox,o=v["a"].getters["moduleProjects/get_project_current"],e.next=5,x["a"].make_request({method:"put",url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),value:r.id,use_sandbox:n,project:o},data:{is_blocked_soft:a}});case 5:s=e.sent,v["a"].commit("moduleWorkers/update_status_block_soft",{worker:r,data:s.data,use_sandbox:n});case 7:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"update_status_block_hard",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(t){var r,a,n,o,s;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return r=t.worker,a=t.is_blocked,n=v["a"].state.module_app.use_sandbox,o=v["a"].getters["moduleProjects/get_project_current"],e.next=5,x["a"].make_request({method:"put",url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),value:r.id,use_sandbox:n,project:o},data:{is_blocked_hard:a}});case 5:s=e.sent,v["a"].commit("moduleWorkers/update_status_block_hard",{worker:r,data:s.data,use_sandbox:n});case 7:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"update_status_block_global",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(t){var r,a,n,o,s;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return r=t.worker,a=t.is_blocked,n=v["a"].state.module_app.use_sandbox,o=v["a"].getters["moduleProjects/get_project_current"],e.next=5,x["a"].make_request({method:"put",url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),value:r.id,use_sandbox:n,project:o},data:{is_blocked_global:a}});case 5:s=e.sent,v["a"].commit("moduleWorkers/update_status_block_global",{worker:r,data:s.data,use_sandbox:n});case 7:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"update_count_assignments_limit",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(t){var r,a,n,o,s;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return r=t.worker,a=t.value,n=v["a"].state.module_app.use_sandbox,o=v["a"].getters["moduleProjects/get_project_current"],e.next=5,x["a"].make_request({method:"put",url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),value:r.id,use_sandbox:n,project:o},data:{count_assignments_limit:a}});case 5:s=e.sent,v["a"].commit("moduleWorkers/set_worker",{worker:r,worker_new:s.data,array_fields:["count_assignments_limit"]});case 7:case"end":return e.stop()}},e)}));function t(t){return e.apply(this,arguments)}return t}()},{key:"load_page",value:function(){var e=Object(p["a"])(regeneratorRuntime.mark(function e(r,a){var n;return regeneratorRuntime.wrap(function(e){while(1)switch(e.prev=e.next){case 0:return n=v["a"].state.module_app.use_sandbox,e.abrupt("return",t.loadPage({pagination:r,filters:a,url:{path:v["a"].getters.get_url("url_api_workers","moduleWorkers"),use_sandbox:n,project:v["a"].getters["moduleProjects/get_project_current"]},callback:function(e){v["a"].commit("moduleWorkers/set_workers",{data:e.data.data,use_sandbox:n}),x["a"].make_request({method:"patch",url:{path:v["a"].getters.get_url("url_api_workers_get_blocks_hard","moduleWorkers"),use_sandbox:n,project:v["a"].getters["moduleProjects/get_project_current"]}}).then(function(e){v["a"].commit("moduleWorkers/set_blocks_hard",{data:e.data,use_sandbox:n})})}}));case 2:case"end":return e.stop()}},e)}));function r(t,r){return e.apply(this,arguments)}return r}()}]),t}(j["a"]),C=new O,S={name:"component-block-soft-worker",props:{worker:{type:Object,required:!0}},data:function(){return{is_updating:!1,show_snackbar:!1}},watch:{},computed:{text_tooltip:function(){return this.worker.is_blocked_soft?"Is blocked project-wide":"Is not blocked project-wide"},color:function(){return this.worker.is_blocked_soft?"warning":"grey"}},methods:Object(c["a"])({toggle:function(){var e=this;this.set_show_progress_indicator(!0),this.is_updating=!0,C.update_status_block_soft({worker:this.worker,is_blocked:!this.worker.is_blocked_soft}).then(function(){e.is_updating=!1,e.show_snackbar=!0,e.set_show_progress_indicator(!1)})}},Object(o["b"])(["set_show_progress_indicator"])),created:function(){},components:{}},q=S,P=r("2877"),W=r("6544"),R=r.n(W),V=r("8336"),B=r("132d"),E=r("2db4"),I=r("3a2f"),T=Object(P["a"])(q,d,_,!1,null,null,null),L=T.exports;R()(T,{VBtn:V["a"],VIcon:B["a"],VSnackbar:E["a"],VTooltip:I["a"]});var F=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("span",[r("v-tooltip",{attrs:{left:""}},[r("v-btn",{staticClass:"ma-0",attrs:{slot:"activator",icon:"",small:"",loading:e.is_updating},on:{click:function(t){return e.toggle()}},slot:"activator"},[r("v-icon",{attrs:{color:e.color}},[e._v("block")])],1),r("span",[e._v(e._s(e.text_tooltip))])],1),r("v-snackbar",{attrs:{timeout:1e3,color:"info",bottom:""},model:{value:e.show_snackbar,callback:function(t){e.show_snackbar=t},expression:"show_snackbar"}},[e._v("\n      Updated\n      "),r("v-btn",{attrs:{flat:""},on:{click:function(t){e.show_snackbar=!1}}},[e._v("\n        Close\n      ")])],1)],1)},$=[],A={name:"component-block-soft-hard-worker",props:{worker:{type:Object,required:!0}},data:function(){return{is_updating:!1,show_snackbar:!1}},watch:{},computed:{text_tooltip:function(){return this.worker.is_blocked_global?"Is soft-blocked globally":"Is not soft-blocked globally"},color:function(){return this.worker.is_blocked_global?"warning":"grey"}},methods:Object(c["a"])({toggle:function(){var e=this;this.set_show_progress_indicator(!0),this.is_updating=!0,C.update_status_block_global({worker:this.worker,is_blocked:!this.worker.is_blocked_global}).then(function(){e.is_updating=!1,e.show_snackbar=!0,e.set_show_progress_indicator(!1)})}},Object(o["b"])("moduleWorkers",{update_status_block_global:"update_status_block_global"}),Object(o["b"])(["set_show_progress_indicator"])),created:function(){},components:{}},G=A,H=Object(P["a"])(G,F,$,!1,null,null,null),D=H.exports;R()(H,{VBtn:V["a"],VIcon:B["a"],VSnackbar:E["a"],VTooltip:I["a"]});var X=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("span",[r("v-tooltip",{attrs:{left:""}},[r("v-btn",{staticClass:"ma-0",attrs:{slot:"activator",icon:"",small:"",loading:e.is_updating},on:{click:function(t){return e.toggle()}},slot:"activator"},[r("v-icon",{attrs:{color:e.color}},[e._v("block")])],1),r("span",[e._v(e._s(e.text_tooltip))])],1),r("v-snackbar",{attrs:{timeout:1e3,color:"info",bottom:""},model:{value:e.show_snackbar,callback:function(t){e.show_snackbar=t},expression:"show_snackbar"}},[e._v("\n      Updated\n      "),r("v-btn",{attrs:{flat:""},on:{click:function(t){e.show_snackbar=!1}}},[e._v("\n        Close\n      ")])],1)],1)},Y=[],z={name:"component-block-hard-worker",props:{worker:{type:Object,required:!0}},data:function(){return{show_snackbar:!1}},watch:{},computed:{is_updating:function(){return void 0==this.worker.is_blocked_hard},text_tooltip:function(){return this.worker.is_blocked_hard?"Is blocked globally":"Is not blocked globally"},color:function(){return this.worker.is_blocked_hard?"error":"grey"}},methods:Object(c["a"])({toggle:function(){var e=this;this.set_show_progress_indicator(!0),C.update_status_block_hard({worker:this.worker,is_blocked:!this.worker.is_blocked_hard}).then(function(){e.show_snackbar=!0,e.set_show_progress_indicator(!1)})}},Object(o["b"])(["set_show_progress_indicator"])),created:function(){},components:{}},N=z,U=Object(P["a"])(N,X,Y,!1,null,null,null),M=U.exports;R()(U,{VBtn:V["a"],VIcon:B["a"],VSnackbar:E["a"],VTooltip:I["a"]});var J=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("span",[null!==e.project_current.count_assignments_max_per_worker?r("v-dialog",{attrs:{"max-width":"500px"},model:{value:e.dialog,callback:function(t){e.dialog=t},expression:"dialog"}},[r("span",{class:{"warning--text":e.has_reached_limit_assignments},attrs:{slot:"activator"},slot:"activator"},[e._v("\n        "+e._s(e.content)+"\n      ")]),r("v-card",[r("v-card-title",[e._v("\n          Assignment Limit for Worker "+e._s(e.worker.id_worker)+"\n        ")]),r("v-card-text",[r("v-layout",{attrs:{row:"","align-center":""}},[r("v-flex",[r("v-text-field",{attrs:{type:"number",label:"Assignment Limit",min:"0",autofocus:""},model:{value:e.limit,callback:function(t){e.limit=t},expression:"limit"}})],1),r("v-flex",[r("v-btn",{attrs:{color:"primary",disabled:!e.has_changed},on:{click:function(t){return e.set(e.limit)}}},[e._v("Set to "+e._s(e.limit))])],1),r("v-flex",[r("v-btn",{attrs:{color:"primary"},on:{click:function(t){return e.set(0)}}},[e._v("Reset")])],1),r("v-flex",[r("v-btn",{attrs:{color:"primary"},on:{click:function(t){return e.set(-1)}}},[e._v("Unlock")])],1)],1)],1)],1)],1):[e._v("\n      No limit\n    ")],r("v-snackbar",{attrs:{timeout:1e3,color:"info",bottom:""},model:{value:e.show_snackbar,callback:function(t){e.show_snackbar=t},expression:"show_snackbar"}},[e._v("\n      Updated\n      "),r("v-btn",{attrs:{flat:""},on:{click:function(t){e.show_snackbar=!1}}},[e._v("\n        Close\n      ")])],1)],2)},K=[],Q={name:"component-limit-assignments",props:{worker:{type:Object,required:!0}},data:function(){return{limit:this.worker.count_assignments_limit,show_snackbar:!1,dialog:!1}},watch:{dialog:function(e){e||(this.limit=this.worker.count_assignments_limit)},"worker.count_assignments_limit":function(){console.log("aawd"),this.limit=this.worker.count_assignments_limit}},computed:Object(c["a"])({has_changed:function(){return this.limit!=this.worker.count_assignments_limit},content:function(){return-1==this.worker.count_assignments_limit?"Unlimited":"".concat(this.worker.count_assignments_limit," of ").concat(this.project_current.count_assignments_max_per_worker," ").concat(this.has_reached_limit_assignments?"(blocked)":"")},has_reached_limit_assignments:function(){return this.worker.count_assignments_limit>=this.project_current.count_assignments_max_per_worker}},Object(o["c"])("moduleProjects",{project_current:"get_project_current"})),methods:Object(c["a"])({set:function(e){var t=this;this.set_show_progress_indicator(!0),C.update_count_assignments_limit({worker:this.worker,value:e}).then(function(){t.show_snackbar=!0,t.dialog=!1,t.set_show_progress_indicator(!1)})}},Object(o["b"])(["set_show_progress_indicator"]))},Z=Q,ee=(r("a96e"),r("b0af")),te=r("99d9"),re=r("12b2"),ae=r("169a"),ne=r("0e8f"),oe=r("a722"),se=r("2677"),ie=Object(P["a"])(Z,J,K,!1,null,null,null),ce=ie.exports;R()(ie,{VBtn:V["a"],VCard:ee["a"],VCardText:te["b"],VCardTitle:re["a"],VDialog:ae["a"],VFlex:ne["a"],VLayout:oe["a"],VSnackbar:E["a"],VTextField:se["a"]});var le={name:"component-item-worker",props:{props:{type:Object,required:!0},array_columns_selected:{type:Array,required:!0},isCondensed:{required:!0,type:Boolean}},data:function(){return{show_snackbar:!1,worker:this.props.item}},computed:Object(c["a"])({set_columns_selected:function(){return new Set(this.array_columns_selected)},stylesCell:function(){return this.isCondensed?{height:"unset !important",paddingLeft:"5px !important",paddingRight:"5px !important"}:{}}},Object(o["c"])(["get_show_progress_indicator"])),methods:{},components:{ComponentBlockSoftWorker:L,ComponentBlockGlobalWorker:D,ComponentBlockHardWorker:M,ComponentLimitAssignments:ce}},ue=le,de=r("ac7c"),_e=Object(P["a"])(ue,l,u,!1,null,"0efd579e",null),pe=_e.exports;R()(_e,{VCheckbox:de["a"]});var me=r("ea2c"),he=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-layout",{attrs:{wrap:""}},[r("base-table-filter",{attrs:{title:"Worker ID","filters-active":e.filtersActive,filters:e.filters,breakpoints:{sm12:!0,md6:!0},"name-filter":"workersSelected"}},[r("v-combobox",{attrs:{label:"Filter workers by their ID",multiple:"",chips:"","deletable-chips":"",clearable:"","hide-details":"",dense:""},model:{value:e.filters.workersSelected,callback:function(t){e.$set(e.filters,"workersSelected",t)},expression:"filters.workersSelected"}})],1)],1)},fe=[],be=r("63aa"),ke={name:"FiltersTableWorkers",components:{BaseTableFilter:be["a"]},props:{filters:{required:!0,type:Object},filtersActive:{required:!0,type:Object}}},ge=ke,we=r("2b5d"),ve=Object(P["a"])(ge,he,fe,!1,null,"e82b3432",null),xe=ve.exports;R()(ve,{VCombobox:we["a"],VLayout:oe["a"]});var ye={name:"TableWorkers",components:{FiltersTableWorkers:xe,BaseTable:me["a"],ComponentItemWorker:pe},props:{nameStatePagination:{required:!1,type:String,default:"paginationGeneral"},nameLocalStoragePagination:{required:!1,type:String,default:"pagination_workers_general"},nameStateColumns:{required:!1,type:String,default:"array_columns_general"},nameLocalStorageColumnsSelected:{required:!1,type:String,default:"array_columns_workers_general"},nameStateColumnsSelected:{required:!1,type:String,default:"array_columns_selected_general"},nameStateColumnsSelectedInitial:{required:!1,type:String,default:"array_columns_selected_initial_general"},nameStateItemsSelected:{required:!1,type:String,default:"object_workers_selected"},filters:{required:!1,type:Object,default:void 0},filtersDefault:{required:!1,type:Object,default:void 0},nameStateFilters:{required:!1,type:String,default:"objectFiltersGeneral"},nameLocalStorageFilters:{required:!1,type:String,default:"filtersWorkersGeneral"},showLinks:{required:!1,type:Boolean,default:!0}},data:function(){return{loadPage:C.load_page,workers_selected:[],pagination:{rowsPerPage:5},show_dialog_policy:!1,policy_to_be_edited:null,items_total:void 0,list_headers:[{text:"Name",value:"name"},{text:"Assignment Limit",value:"counter_assignments",align:"center",width:"1px"},{text:"Project Block",value:"block_soft",width:"1px"},{text:"Soft MTurk Block",value:"block_soft_hard",width:"1px"},{text:"Hard MTurk Block",value:"block_hard",width:"1px"}]}},computed:Object(c["a"])({filtersComputed:function(){return void 0!==this.filters?this.filters:this.filtersGeneral},filtersDefaultComputed:function(){return void 0!==this.filtersDefault?this.filtersDefault:this.filtersDefaultGeneral}},Object(o["c"])("moduleWorkers",{array_items:"get_array_workers",object_items_selected:"get_object_workers_selected",array_columns:"get_array_columns_general",array_columns_selected:"get_array_columns_selected_general"}),{list_workers:function(){return this.list_workers_processed.slice(0,5)}},Object(o["c"])("moduleWorkers",{list_workers_processed:"list_workers"}),Object(o["c"])("moduleProjects",{project_current:"get_project_current"}),Object(o["e"])("moduleWorkers",{paginationComputed:"paginationGeneral",filtersGeneral:"objectFiltersGeneral",filtersDefaultGeneral:"objectFiltersDefaultGeneral"})),methods:Object(c["a"])({load_page:function(){var e=this;this.loading=!0,C.load_page(this.pagination,Object(c["a"])({},this.filters)).then(function(t){e.items_total=t,e.loading=!1})}},Object(o["d"])("moduleWorkers",{function_set_items_selected:"set_workers_selected",function_clear_items_selected:"clear_workers_selected",function_set_array_columns:"set_array_columns_general",functionSetPagination:"setPaginationGeneral"}),Object(o["b"])("moduleWorkers",{update_status_block:"update_status_block",function_reset_array_columns:"reset_array_columns_general",setState:"setState"}))},je=ye,Oe=(r("7165"),Object(P["a"])(je,s,i,!1,null,"19014b2c",null)),Ce=Oe.exports,Se={name:"AppWorkers",components:{TableWorkers:Ce},data:function(){return{workers_selected:[]}},computed:{},methods:{}},qe=Se,Pe=Object(P["a"])(qe,a,n,!1,null,null,null);t["default"]=Pe.exports},a844:function(e,t,r){"use strict";r("7e63");var a=r("8654"),n=r("d9bd"),o=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var a in r)Object.prototype.hasOwnProperty.call(r,a)&&(e[a]=r[a])}return e};t["a"]={name:"v-textarea",extends:a["a"],props:{autoGrow:Boolean,noResize:Boolean,outline:Boolean,rowHeight:{type:[Number,String],default:24,validator:function(e){return!isNaN(parseFloat(e))}},rows:{type:[Number,String],default:5,validator:function(e){return!isNaN(parseInt(e,10))}}},computed:{classes:function(){return o({"v-textarea":!0,"v-textarea--auto-grow":this.autoGrow,"v-textarea--no-resize":this.noResizeHandle},a["a"].options.computed.classes.call(this,null))},dynamicHeight:function(){return this.autoGrow?this.inputHeight:"auto"},isEnclosed:function(){return this.textarea||a["a"].options.computed.isEnclosed.call(this)},noResizeHandle:function(){return this.noResize||this.autoGrow}},watch:{lazyValue:function(){!this.internalChange&&this.autoGrow&&this.$nextTick(this.calculateInputHeight)}},mounted:function(){var e=this;setTimeout(function(){e.autoGrow&&e.calculateInputHeight()},0),this.autoGrow&&this.noResize&&Object(n["b"])('"no-resize" is now implied when using "auto-grow", and can be removed',this)},methods:{calculateInputHeight:function(){var e=this.$refs.input;if(e){e.style.height=0;var t=e.scrollHeight,r=parseInt(this.rows,10)*parseFloat(this.rowHeight);e.style.height=Math.max(r,t)+"px"}},genInput:function(){var e=a["a"].options.methods.genInput.call(this);return e.tag="textarea",delete e.data.attrs.type,e.data.attrs.rows=this.rows,e},onInput:function(e){a["a"].options.methods.onInput.call(this,e),this.autoGrow&&this.calculateInputHeight()},onKeyDown:function(e){this.isFocused&&13===e.keyCode&&e.stopPropagation(),this.internalChange=!0,this.$emit("keydown",e)}}}},a96e:function(e,t,r){"use strict";var a=r("d896"),n=r.n(a);n.a},b73d:function(e,t,r){"use strict";r("94a7"),r("2e29");var a=r("5368"),n=r("c341"),o=r("0789"),s=r("490a"),i=r("80d2"),c=Object.assign||function(e){for(var t=1;t<arguments.length;t++){var r=arguments[t];for(var a in r)Object.prototype.hasOwnProperty.call(r,a)&&(e[a]=r[a])}return e};t["a"]={name:"v-switch",directives:{Touch:n["a"]},mixins:[a["a"]],props:{loading:{type:[Boolean,String],default:!1}},computed:{classes:function(){return{"v-input--selection-controls v-input--switch":!0}},switchData:function(){return this.setTextColor(this.loading?void 0:this.computedColor,{class:this.themeClasses})}},methods:{genDefaultSlot:function(){return[this.genSwitch(),this.genLabel()]},genSwitch:function(){return this.$createElement("div",{staticClass:"v-input--selection-controls__input"},[this.genInput("checkbox",this.$attrs),this.genRipple(this.setTextColor(this.computedColor,{directives:[{name:"touch",value:{left:this.onSwipeLeft,right:this.onSwipeRight}}]})),this.$createElement("div",c({staticClass:"v-input--switch__track"},this.switchData)),this.$createElement("div",c({staticClass:"v-input--switch__thumb"},this.switchData),[this.genProgress()])])},genProgress:function(){return this.$createElement(o["b"],{},[!1===this.loading?null:this.$slots.progress||this.$createElement(s["a"],{props:{color:!0===this.loading||""===this.loading?this.color||"primary":this.loading,size:16,width:2,indeterminate:!0}})])},onSwipeLeft:function(){this.isActive&&this.onChange()},onSwipeRight:function(){this.isActive||this.onChange()},onKeydown:function(e){(e.keyCode===i["q"].left&&this.isActive||e.keyCode===i["q"].right&&!this.isActive)&&this.onChange()}}}},c341:function(e,t,r){"use strict";var a=r("80d2"),n=function(e){var t=e.touchstartX,r=e.touchendX,a=e.touchstartY,n=e.touchendY,o=.5,s=16;e.offsetX=r-t,e.offsetY=n-a,Math.abs(e.offsetY)<o*Math.abs(e.offsetX)&&(e.left&&r<t-s&&e.left(e),e.right&&r>t+s&&e.right(e)),Math.abs(e.offsetX)<o*Math.abs(e.offsetY)&&(e.up&&n<a-s&&e.up(e),e.down&&n>a+s&&e.down(e))};function o(e,t){var r=e.changedTouches[0];t.touchstartX=r.clientX,t.touchstartY=r.clientY,t.start&&t.start(Object.assign(e,t))}function s(e,t){var r=e.changedTouches[0];t.touchendX=r.clientX,t.touchendY=r.clientY,t.end&&t.end(Object.assign(e,t)),n(t)}function i(e,t){var r=e.changedTouches[0];t.touchmoveX=r.clientX,t.touchmoveY=r.clientY,t.move&&t.move(Object.assign(e,t))}function c(e){var t={touchstartX:0,touchstartY:0,touchendX:0,touchendY:0,touchmoveX:0,touchmoveY:0,offsetX:0,offsetY:0,left:e.left,right:e.right,up:e.up,down:e.down,start:e.start,move:e.move,end:e.end};return{touchstart:function(e){return o(e,t)},touchend:function(e){return s(e,t)},touchmove:function(e){return i(e,t)}}}function l(e,t,r){var n=t.value,o=n.parent?e.parentElement:e,s=n.options||{passive:!0};if(o){var i=c(t.value);o._touchHandlers=Object(o._touchHandlers),o._touchHandlers[r.context._uid]=i,Object(a["r"])(i).forEach(function(e){o.addEventListener(e,i[e],s)})}}function u(e,t,r){var n=t.value.parent?e.parentElement:e;if(n&&n._touchHandlers){var o=n._touchHandlers[r.context._uid];Object(a["r"])(o).forEach(function(e){n.removeEventListener(e,o[e])}),delete n._touchHandlers[r.context._uid]}}t["a"]={inserted:l,unbind:u}},d896:function(e,t,r){},f1ae:function(e,t,r){"use strict";var a=r("86cc"),n=r("4630");e.exports=function(e,t,r){t in e?a.f(e,t,n(0,r)):e[t]=r}}}]);
//# sourceMappingURL=workers.e6036737.js.map