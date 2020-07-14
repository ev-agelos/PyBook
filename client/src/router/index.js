import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ResetPassword from '../views/ResetPassword.vue'
import store from '../store.js'

Vue.use(VueRouter)

export default new VueRouter({
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Home
        },
        {
            path: '/reset-password',
            name: 'ResetPassword',
            component: ResetPassword,
            beforeEnter: (to, from, next) => {
                console.log(store.access_token)
                if (store.access_token) {
                    next({name: 'Home'});
                } else {
                    next();
                }
            }
        },
    ]
})