import {createRouter, createWebHistory} from 'vue-router'
import Auth from '../views/Auth.vue'
import Main from '../views/Main.vue'
import {YANDEX_CLIENT_ID, YANDEX_CLIENT_SECRET, YANDEX_REDIRECT} from "@/config.ts";

const router = createRouter({
    history: createWebHistory(import.meta.env.BASE_URL),
    routes: [
        {path: '/', name: 'main', component: Main, meta: { requiresAuth: false }},
        {path: '/auth', name: 'auth', component: Auth},
    ],
});

router.beforeEach((to, from, next) => {
    setToken().then(() => {
        const isAuthenticated = localStorage.getItem('token') // Проверка авторизации

        if (to.meta.requiresAuth && !isAuthenticated) {
            next('/auth')
        } else {
            next()
        }
    });
});

async function setToken() {
    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');

    if (code) {
        const response = await fetch('https://oauth.yandex.ru/token', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: new URLSearchParams({
                grant_type: 'authorization_code',
                code: code,
                client_id: YANDEX_CLIENT_ID,
                client_secret: YANDEX_CLIENT_SECRET,
                redirect_uri: YANDEX_REDIRECT
            })
        });

        const data = await response.json();
        if (response.ok) {
            localStorage.setItem('token', data.access_token);
        }
    }
}

export default router
