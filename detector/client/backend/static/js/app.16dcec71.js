(function(e){function t(t){for(var n,a,c=t[0],s=t[1],i=t[2],l=0,d=[];l<c.length;l++)a=c[l],Object.prototype.hasOwnProperty.call(o,a)&&o[a]&&d.push(o[a][0]),o[a]=0;for(n in s)Object.prototype.hasOwnProperty.call(s,n)&&(e[n]=s[n]);p&&p(t);while(d.length)d.shift()();return u.push.apply(u,i||[]),r()}function r(){for(var e,t=0;t<u.length;t++){for(var r=u[t],n=!0,a=1;a<r.length;a++){var c=r[a];0!==o[c]&&(n=!1)}n&&(u.splice(t--,1),e=s(s.s=r[0]))}return e}var n={},a={app:0},o={app:0},u=[];function c(e){return s.p+"js/"+({}[e]||e)+"."+{"chunk-350f4156":"084ad2a5","chunk-0ed90b40":"7657eb50","chunk-64698555":"e8546d3c","chunk-2d0a43e1":"ed90d7fb","chunk-5eea4817":"abb8debc"}[e]+".js"}function s(t){if(n[t])return n[t].exports;var r=n[t]={i:t,l:!1,exports:{}};return e[t].call(r.exports,r,r.exports,s),r.l=!0,r.exports}s.e=function(e){var t=[],r={"chunk-350f4156":1,"chunk-0ed90b40":1,"chunk-64698555":1,"chunk-5eea4817":1};a[e]?t.push(a[e]):0!==a[e]&&r[e]&&t.push(a[e]=new Promise((function(t,r){for(var n="css/"+({}[e]||e)+"."+{"chunk-350f4156":"8d4ebc6d","chunk-0ed90b40":"6bd5bafa","chunk-64698555":"2e67d550","chunk-2d0a43e1":"31d6cfe0","chunk-5eea4817":"4eb0deb2"}[e]+".css",o=s.p+n,u=document.getElementsByTagName("link"),c=0;c<u.length;c++){var i=u[c],l=i.getAttribute("data-href")||i.getAttribute("href");if("stylesheet"===i.rel&&(l===n||l===o))return t()}var d=document.getElementsByTagName("style");for(c=0;c<d.length;c++){i=d[c],l=i.getAttribute("data-href");if(l===n||l===o)return t()}var p=document.createElement("link");p.rel="stylesheet",p.type="text/css",p.onload=t,p.onerror=function(t){var n=t&&t.target&&t.target.src||o,u=new Error("Loading CSS chunk "+e+" failed.\n("+n+")");u.code="CSS_CHUNK_LOAD_FAILED",u.request=n,delete a[e],p.parentNode.removeChild(p),r(u)},p.href=o;var f=document.getElementsByTagName("head")[0];f.appendChild(p)})).then((function(){a[e]=0})));var n=o[e];if(0!==n)if(n)t.push(n[2]);else{var u=new Promise((function(t,r){n=o[e]=[t,r]}));t.push(n[2]=u);var i,l=document.createElement("script");l.charset="utf-8",l.timeout=120,s.nc&&l.setAttribute("nonce",s.nc),l.src=c(e);var d=new Error;i=function(t){l.onerror=l.onload=null,clearTimeout(p);var r=o[e];if(0!==r){if(r){var n=t&&("load"===t.type?"missing":t.type),a=t&&t.target&&t.target.src;d.message="Loading chunk "+e+" failed.\n("+n+": "+a+")",d.name="ChunkLoadError",d.type=n,d.request=a,r[1](d)}o[e]=void 0}};var p=setTimeout((function(){i({type:"timeout",target:l})}),12e4);l.onerror=l.onload=i,document.head.appendChild(l)}return Promise.all(t)},s.m=e,s.c=n,s.d=function(e,t,r){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:r})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var r=Object.create(null);if(s.r(r),Object.defineProperty(r,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)s.d(r,n,function(t){return e[t]}.bind(null,n));return r},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/",s.oe=function(e){throw console.error(e),e};var i=window["webpackJsonp"]=window["webpackJsonp"]||[],l=i.push.bind(i);i.push=t,i=i.slice();for(var d=0;d<i.length;d++)t(i[d]);var p=l;u.push([0,"chunk-vendors"]),r()})({0:function(e,t,r){e.exports=r("56d7")},"034f":function(e,t,r){"use strict";r("85ec")},"56d7":function(e,t,r){"use strict";r.r(t);r("e260"),r("e6cf"),r("cca6"),r("a79d"),r("d3b7");var n=r("2b0e"),a=function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("div",{attrs:{id:"app"}},[r("v-app",[r("nav-bar"),r("v-main",[r("router-view")],1),r("v-dialog",{attrs:{"max-width":"300"},model:{value:e.showErrorModal,callback:function(t){e.showErrorModal=t},expression:"showErrorModal"}},[r("v-card",[r("v-card-title",{staticClass:"text-h5"},[e._v(" Ошибка ")]),r("v-card-text",[e._v(" "+e._s(e.modalContent)+" ")]),r("v-card-actions",[r("v-btn",{attrs:{color:"green darken-1",text:""},on:{click:function(t){e.showErrorModal=!1}}},[e._v(" OK ")])],1)],1)],1)],1)],1)},o=[],u=r("1da1"),c=(r("96cf"),function(){var e=this,t=e.$createElement,r=e._self._c||t;return r("v-app-bar",{attrs:{color:"light-blue",dark:"",app:""}},[r("v-toolbar-title",[r("router-link",{staticClass:"text-white",attrs:{to:"/"}},[e._v("Детектор аномалий")])],1),r("v-spacer"),e.$store.state.isAuthenticated?r("v-btn",{attrs:{plain:""},on:{click:e.logout}},[e._v(" Выйти ")]):e._e()],1)}),s=[],i=(r("ac1f"),r("5319"),{methods:{logout:function(){var e=this;return Object(u["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,e.$store.dispatch("logout");case 2:e.$router.replace({name:"Login"});case 3:case"end":return t.stop()}}),t)})))()}}}),l=i,d=r("2877"),p=r("6544"),f=r.n(p),h=r("40dc"),m=r("8336"),v=r("2fa4"),b=r("2a7f"),g=Object(d["a"])(l,c,s,!1,null,null,null),w=g.exports;f()(g,{VAppBar:h["a"],VBtn:m["a"],VSpacer:v["a"],VToolbarTitle:b["a"]});var k=r("bee2"),x=r("d4ec"),y=(r("e9c4"),Object(k["a"])((function e(){Object(x["a"])(this,e)})));y.install=function(e){this.ErrorEvent=new e,e.showErrorModal=function(e){var t=e.detail||e.non_field_errors||JSON.stringify(e),r={data:t};y.ErrorEvent.$emit("show",r)},e.prototype.$showErrorModal=function(e){var t=e.detail||e.non_field_errors||JSON.stringify(e),r={data:t};y.ErrorEvent.$emit("show",r)}};var E=y,_={components:{NavBar:w},name:"app",data:function(){return{showErrorModal:!1,modalContent:null}},beforeMount:function(){var e=this;return Object(u["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:E.ErrorEvent.$on("show",(function(t){e.modalContent=t.data,e.showErrorModal=!0}));case 1:case"end":return t.stop()}}),t)})))()}},O=_,A=(r("034f"),r("7496")),j=r("b0af"),R=r("99d9"),M=r("169a"),C=r("f6c4"),S=Object(d["a"])(O,a,o,!1,null,null,null),I=S.exports;f()(S,{VApp:A["a"],VBtn:m["a"],VCard:j["a"],VCardActions:R["a"],VCardText:R["b"],VCardTitle:R["c"],VDialog:M["a"],VMain:C["a"]});r("3ca3"),r("ddb0");var V=r("8c4f");n["default"].use(V["a"]);var P={routes:[{path:"/",name:"MainPage",component:function(){return Promise.all([r.e("chunk-350f4156"),r.e("chunk-64698555"),r.e("chunk-2d0a43e1")]).then(r.bind(null,"0638"))},meta:{requiresAuth:!0}},{path:"/closest_raw_values/:id",name:"ClosestRawValues",component:function(){return Promise.all([r.e("chunk-350f4156"),r.e("chunk-64698555"),r.e("chunk-5eea4817")]).then(r.bind(null,"87f3"))},meta:{requiresAuth:!0}},{path:"/login",name:"Login",component:function(){return Promise.all([r.e("chunk-350f4156"),r.e("chunk-0ed90b40")]).then(r.bind(null,"578a"))},meta:{requiresAuth:!1}}],linkExactActiveClass:"active"},T=new V["a"](P),L=T,$=r("bc3a"),H=r.n($),N=r("5f5b"),q=(r("f9e3"),r("2dd8"),r("c740"),r("99af"),r("2f62")),B=r("ba6a");n["default"].use(q["a"]);var D=function(){return{user:null,isAuthenticated:!1,anomalies:[]}},J=new q["a"].Store({state:D,mutations:{setUser:function(e,t){e.user=t},setAuthenticated:function(e,t){e.isAuthenticated=t},setAnomalies:function(e,t){e.anomalies=t}},actions:{setAnomalies:function(e){return Object(u["a"])(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return t.next=2,B["a"].getList("Anomaly",{},!0);case 2:r=t.sent.data,e.commit("setAnomalies",r);case 4:case"end":return t.stop()}}),t)})))()},addItem:function(e,t){return Object(u["a"])(regeneratorRuntime.mark((function r(){var n,a,o,u;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return n=t.data,a=t.mutation,r.next=4,B["a"].createItem(t.url,n,!0);case 4:o=r.sent.data,u=e.state[t.items_name],u.push(o),e.commit(a,u);case 8:case"end":return r.stop()}}),r)})))()},updateItem:function(e,t){return Object(u["a"])(regeneratorRuntime.mark((function r(){var a,o,u,c,s,i;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return a=t.data,o=t.mutation,u=t.dataID,r.next=5,B["a"].updateItem(t.url,u,a,!0);case 5:c=r.sent.data,s=e.state[t.items_name],i=s.findIndex((function(e){return e.id==u})),-1!=i&&n["default"].set(s,i,c),e.commit(o,s);case 10:case"end":return r.stop()}}),r)})))()},login:function(e,t){return Object(u["a"])(regeneratorRuntime.mark((function r(){var a,o,u,c,s;return regeneratorRuntime.wrap((function(r){while(1)switch(r.prev=r.next){case 0:return a=t.token,localStorage.setItem("api_token",a),o=!1,r.prev=3,r.next=6,H.a.get("/check_token",{headers:B["a"].getHeaders()});case 6:o=!0,r.next=14;break;case 9:if(r.prev=9,r.t0=r["catch"](3),localStorage.removeItem("api_token"),u=r.t0.response.data,u.detail)n["default"].showErrorModal(u.detail);else{for(s in c="",u)c+="".concat(s,": ").concat(u[s],"\n");n["default"].showErrorModal(c)}case 14:return r.next=16,e.dispatch("checkAuth");case 16:return r.abrupt("return",o);case 17:case"end":return r.stop()}}),r,null,[[3,9]])})))()},logout:function(e){return Object(u["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:localStorage.removeItem("api_token"),e.commit("setAuthenticated",!1);case 2:case"end":return t.stop()}}),t)})))()},checkAuth:function(e){return Object(u["a"])(regeneratorRuntime.mark((function t(){var r;return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:return e.commit("setAuthenticated",!0),t.prev=1,t.next=4,H.a.get("/check_token",{headers:B["a"].getHeaders()});case 4:if(r=t.sent,200==r.status){t.next=8;break}return e.commit("setAuthenticated",!1),t.abrupt("return");case 8:e.commit("setAuthenticated",!0),t.next=14;break;case 11:t.prev=11,t.t0=t["catch"](1),e.commit("setAuthenticated",!1);case 14:case"end":return t.stop()}}),t,null,[[1,11]])})))()}}}),F=J,K=r("f309"),U=r("e1bf"),z=r("1072");n["default"].use(K["a"]);var G={lang:{current:"ru",locales:{ru:U["a"],en:z["a"]}}},Q=new K["a"](G);n["default"].use(E),n["default"].use(N["a"]),L.beforeEach((function(e,t,r){e.matched.some((function(e){return e.meta.requiresAuth}))?F.state.isAuthenticated?r():r({name:"Login",query:{redirect:e.fullPath}}):r()})),n["default"].config.productionTip=!1,F.dispatch("checkAuth").then((function(){new n["default"]({router:L,store:F,vuetify:Q,render:function(e){return e(I)}}).$mount("#app")})),H.a.defaults.headers.common["Content-Type"]="application/json"},"85ec":function(e,t,r){},ba6a:function(e,t,r){"use strict";var n=r("1da1"),a=(r("96cf"),r("b64b"),r("99af"),r("fb6a"),r("bc3a")),o=r.n(a),u=r("2b0e");t["a"]={urls:{Anomaly:"/api/anomaly/",ClosestRawValue:"/api/closest_raw_values/"},getFilterValues:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t){var r,n,a;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:if(r="",0!=Object.keys(t).length){for(n in r="?",t)a=t[n],r+="".concat(n,"=").concat(a,"&");r=r.slice(0,r.lastIndexOf("&"))}return e.abrupt("return",r);case 3:case"end":return e.stop()}}),e)})));function t(t){return e.apply(this,arguments)}return t}(),getHeaders:function(){return{Authorization:"Token ".concat(localStorage.getItem("api_token"))}},getList:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t){var r,n,a,c=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return r=c.length>1&&void 0!==c[1]?c[1]:{},n=c.length>2&&void 0!==c[2]&&c[2],e.next=4,this.getFilterValues(r);case 4:return a=e.sent,e.prev=5,e.next=8,o.a.get("".concat(this.urls[t]).concat(a),{headers:this.getHeaders()});case 8:return e.abrupt("return",e.sent);case 11:if(e.prev=11,e.t0=e["catch"](5),!n){e.next=16;break}return u["default"].showErrorModal(e.t0.response.data),e.abrupt("return",{data:[]});case 16:return e.abrupt("return",e.t0.response);case 17:case"end":return e.stop()}}),e,this,[[5,11]])})));function t(t){return e.apply(this,arguments)}return t}(),getItem:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r){var n,a=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=a.length>2&&void 0!==a[2]&&a[2],e.prev=1,e.next=4,o.a.get("".concat(this.urls[t]).concat(r,"/"),{headers:this.getHeaders()});case 4:return e.abrupt("return",e.sent);case 7:if(e.prev=7,e.t0=e["catch"](1),!n){e.next=12;break}return u["default"].showErrorModal(e.t0.response.data),e.abrupt("return",{data:{}});case 12:return e.abrupt("return",e.t0.response);case 13:case"end":return e.stop()}}),e,this,[[1,7]])})));function t(t,r){return e.apply(this,arguments)}return t}(),createItem:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r){var n,a=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=a.length>2&&void 0!==a[2]&&a[2],e.prev=1,e.next=4,o.a.post("".concat(this.urls[t]),r,{headers:this.getHeaders()});case 4:return e.abrupt("return",e.sent);case 7:if(e.prev=7,e.t0=e["catch"](1),!n){e.next=12;break}return u["default"].showErrorModal(e.t0.response.data),e.abrupt("return",{data:r});case 12:return e.abrupt("return",e.t0.response);case 13:case"end":return e.stop()}}),e,this,[[1,7]])})));function t(t,r){return e.apply(this,arguments)}return t}(),updateItem:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r,n){var a,c=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return a=c.length>3&&void 0!==c[3]&&c[3],e.prev=1,e.next=4,o.a.put("".concat(this.urls[t]).concat(r,"/"),n,{headers:this.getHeaders()});case 4:return e.abrupt("return",e.sent);case 7:if(e.prev=7,e.t0=e["catch"](1),!a){e.next=12;break}return u["default"].showErrorModal(e.t0.response.data),e.abrupt("return",{data:n});case 12:return e.abrupt("return",e.t0.response);case 13:case"end":return e.stop()}}),e,this,[[1,7]])})));function t(t,r,n){return e.apply(this,arguments)}return t}(),deleteItem:function(){var e=Object(n["a"])(regeneratorRuntime.mark((function e(t,r){var n,a=arguments;return regeneratorRuntime.wrap((function(e){while(1)switch(e.prev=e.next){case 0:return n=a.length>2&&void 0!==a[2]&&a[2],e.prev=1,e.next=4,o.a.delete("".concat(this.urls[t]).concat(r,"/"),{headers:this.getHeaders()});case 4:return e.abrupt("return",e.sent);case 7:return e.prev=7,e.t0=e["catch"](1),n&&u["default"].showErrorModal(e.t0.response.data),e.abrupt("return",e.t0.response);case 11:case"end":return e.stop()}}),e,this,[[1,7]])})));function t(t,r){return e.apply(this,arguments)}return t}()}}});
//# sourceMappingURL=app.16dcec71.js.map