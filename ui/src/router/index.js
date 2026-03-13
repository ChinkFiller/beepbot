import { createRouter, createWebHistory } from 'vue-router';


const routes = [
    {
        path: '/',
        name: 'Index',
        component:() => import('@/views/index/index.vue'),
        meta:{
        }
    },
    {
        path: '/search',
        name: 'Search',
        component:() => import('@/views/search/index.vue'),
        meta:{
        }
    }
];


const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;
