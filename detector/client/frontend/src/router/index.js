import Vue from 'vue'
import VueRouter from 'vue-router'


Vue.use(VueRouter)

let opts = {
  routes: [
    {
      path: "/",
      name: "MainPage",
      component: () => import('../components/Anomalies.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/closest_raw_values/:id",
      name: "ClosestRawValues",
      component: () => import('../components/RawValues.vue'),
      meta: {
        requiresAuth: true
      }
    },
    {
      path: "/login",
      name: "Login",
      component: () => import('../components/Login.vue'),
      meta: {
        requiresAuth: false
      }
    },
  ],
  linkExactActiveClass: 'active'
};
const router = new VueRouter(opts);

export default router
