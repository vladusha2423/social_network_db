import Vue from 'vue';
import Router from 'vue-router';
import Main from "@/views/Main";
import Login from "@/views/Login";
import Feed from "@/views/Feed";
import Users from "@/views/Users";
import Groups from "@/views/Groups";
import Messages from "@/views/Messages";
import User from "@/views/User";
import Public from "@/views/Public";
import Chat from "@/views/Chat";
import Registration from "@/views/Registration";

Vue.use(Router);

export default new Router({
    mode: 'history',
    base: process.env.BASE_URL,
    routes: [
        {
            path: '/',
            name: 'Home',
            component: Main,
        },
        {
            path: '/login',
            name: 'Login',
            component: Login,
        },
        {
            path: '/registration',
            name: 'Registration',
            component: Registration,
        },
        {
            path: '/feed',
            name: 'Feed',
            component: Feed,
        },
        {
            path: '/users',
            name: 'Users',
            component: Users,
        },
        {
            path: '/user/:id',
            name: 'User',
            component: User,
        },
        {
            path: '/groups',
            name: 'Groups',
            component: Groups,
        },
        {
            path: '/public/:id',
            name: 'Public',
            component: Public,
        },
        {
            path: '/chat',
            name: 'Chats',
            component: Messages,
        },
        {
            path: '/chat/:id',
            name: 'Chat',
            component: Chat,
        },
    ],
});
