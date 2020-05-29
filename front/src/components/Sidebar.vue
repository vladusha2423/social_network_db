<template>
    <v-navigation-drawer
            absolute
            dark
            src="https://cdn.vuetifyjs.com/images/backgrounds/bg-2.jpg"
            class="sidebar"
            :expand-on-hover="width < 950 && width > 550"
            :mini-variant="width < 950"
            permanent
            touchless
    >
        <v-list>
            <v-list-item two-line class="px-0 ml-2">
                <v-list-item-avatar>
                    <img :src="user.avatar || require('../assets/images/user_logo.png')" alt="User avatar">
                </v-list-item-avatar>

                <v-list-item-content>
                    <v-list-item-title>{{user.name + ' ' + user.surname}}</v-list-item-title>
                    <v-list-item-subtitle>{{user.nick}}</v-list-item-subtitle>
                </v-list-item-content>
            </v-list-item>
            <v-list-item
                    v-for="(item, i) in items"
                    :key="i"
                    link
                    @click="redirect(item.link)"
            >
                <v-list-item-icon>
                    <Icon :icon="item.icon" />
                </v-list-item-icon>

                <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                </v-list-item-content>
            </v-list-item>
        </v-list>
        <v-spacer></v-spacer>
        <template v-slot:append>
            <div class="pa-2">
                <v-btn block @click="logout()" :icon="width < 950">
                    <span v-if="width >= 950">Logout</span>
                    <Icon style="font-size: 20px;" v-else icon="sign-out-alt" />
                </v-btn>
            </div>
        </template>
    </v-navigation-drawer>
</template>

<script>
    export default {
        name: "Sidebar",
        props: {
            user: Object,
        },
        data(){
            return{
                items: [
                    {
                        title: 'Моя страница',
                        icon: 'home',
                        link: '/'
                    },
                    {
                        title: 'Лента',
                        icon: 'newspaper',
                        link: '/feed'
                    },
                    {
                        title: 'Пользователи',
                        icon: 'user',
                        link: '/users'
                    },
                    {
                        title: 'Сообщения',
                        icon: 'comment',
                        link: '/chat'
                    },
                    {
                        title: 'Паблики',
                        icon: 'users',
                        link: '/groups'
                    },
                ],
                width: Number,
                height: Number,
            }
        },
        methods: {
            logout(){
                localStorage.removeItem('token');
                this.$router.push('/login');
            },
            redirect(path){
                this.$router.push(path);
            },
            updateSize: function(){
                this.width = window.innerWidth;
                this.height = window.innerHeight;
            },
        },
        created(){
            this.width = window.innerWidth;
            this.height = window.innerHeight;
            window.addEventListener('resize', this.updateSize);
        }

    }
</script>

<style scoped>
</style>