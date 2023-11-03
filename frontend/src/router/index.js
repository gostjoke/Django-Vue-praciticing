// frontend/src/router/index.js

import {createWebHistory, createRouter} from "vue-router";
import HomeView from "@/views/HomeView.vue";
import ArticleDetail from "@/views/ArticleDetail.vue";

const routes = [
    {
        path: "/",
        name: "HomeView",
        component: HomeView,
    },
    {
        path: "/article/:id", //http://localhost:8080/article/1
        name: "ArticleDetail",
        component: ArticleDetail
    }
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

export default router;