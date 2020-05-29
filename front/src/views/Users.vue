<template>
    <div class="users">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <v-toolbar-title class="ml-4">Пользователи</v-toolbar-title>
        </v-app-bar>
        <v-row class="ml-4 mt-4"
               v-for="(item, i) in users"
               @click="redirect('/user/' + item.id)"
               :key="i">
            <v-card class="d-flex flex-row pl-3 pt-3" max-width="600" width="90%" hover>
                <div>
                    <img :src="item.avatar || require('../assets/images/user_logo.png')"
                         alt="user avatar"
                         class="users-photo" />
                </div>
                <div class="ml-3">
                    <h3>{{item.name + ' ' + item.surname}}</h3>
                    <p>{{item.nick}}<br />{{item.descr}}</p>
                </div>


            </v-card>
        </v-row>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Users",
        data(){
            return {
                users: Array,
            }
        },
        created(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/users")
                    .then(response => this.after_request(response));
            else
                this.$router.push('/login');
        },
        methods: {
            redirect(path){
                this.$router.push(path);
            },
            after_request(response){
                console.log('Route', this.$route.name);
                console.log('Users: ', response);
                this.users = response.data;
            }
        }
    }
</script>

<style lang="scss" scoped>
.users{
    &-photo{
        width: 80px;
        height: 80px;
        border-radius: 50%;
        @media(max-width: 550px){
            width: 40px;
            height: 40px;
        }
    }
}
</style>