<template>
    <div class="me">
        <v-row :class="{'ml-3': width >= 550, 'ml-2': width < 550}"
               :justify="width < 550 ? 'center' : ''"
               :align="width < 550 ? 'center' : ''">
            <div class="mr-1">
                <v-card class="flex-column mt-4 pt-2" width="200">
                    <v-row align="center" justify="center">
                        <img
                                :src="user.avatar || require('../assets/images/user_logo.png')"
                                class="me-avatar mt-3"
                                alt="user avatar" />
                    </v-row>
                    <v-row align="center" justify="center">
                        <v-btn class="mt-4"
                               @click="subscribe()">
                            Подписаться
                        </v-btn>
                    </v-row>
                    <v-row align="center" justify="center">
                        <v-btn
                                @click="write()"
                                class="mt-4 mb-3">
                            Написать
                        </v-btn>
                    </v-row>

                </v-card>
            </div>
            <div class="d-flex flex-column ml-4 mt-2 me-description">
                <v-row>
                    <v-card class="flex-column mt-2 pr-2 pl-2 pt-2" max-width="600px" width="90%">
                        <h3>{{user.name + ' ' + user.surname}}</h3>
                        <p class="mt-4">{{user.descr}}</p>
                        <p><b>{{user.nick}}</b></p>
                    </v-card>
                </v-row>
            </div>

        </v-row>
        <v-row class="ml-3" v-for="(item, i) in posts" :key="i">
            <v-card class="mt-4" max-width="775px" width="93%">
                <v-row class="ml-4 mt-4">
                    {{item.text}}
                </v-row>
                <v-row class="ml-4">
                    <v-btn icon>
                        <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <div class="mt-1">
                        {{item.likes}}
                    </div>
                    <v-btn icon class="ml-8">
                        <v-icon>mdi-comment</v-icon>
                    </v-btn>
                    <div class="mt-1">
                        {{item.views}}
                    </div>
                </v-row>
            </v-card>
        </v-row>
    </div>
</template>

<script>
    import axios from 'axios'
    export default {
        props: {
            source: String,
        },
        data: () => ({
            user: {
                avatar: require('../assets/images/user_logo.png'),
                name: 'Имя',
                surname: 'Фамилия',
                descr: 'Описание',
                nick: 'Никнейм',
                width: Number,
                height: Number,
            },
            posts: [],
        }),
        beforeCreate(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/user/" + this.$route.params.id,
                        {headers: {'x-access-token': localStorage.getItem('token')}})
                    .catch(function(error){
                        console.log(error);
                    })
                    .then(response => this.after_user(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_user(response){
                console.log('Route', this.$router);
                console.log('User: ', response);
                this.user = response.data;
                this.get_posts();
            },
            after_posts(response){
                console.log('Route', this.$router);
                console.log('Posts: ', response);
                this.posts = response.data;
            },
            get_posts(){
                if(localStorage.getItem('token'))
                    axios
                        .get("http://dvv2423.fvds.ru:84/api/posts/user/" + this.$route.params.id)
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_posts(response));
                else
                    this.$router.push('/login');
            },
            subscribe(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/user/subscribe/" + this.$route.params.id,
                            {}, {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => alert(response.data));
                else
                    this.$router.push('/login');
            },
            write(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/chats",
                            {'type': 'dialog', 'title': '', 'avatar': ''})
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => this.after_write(response.data));
                else
                    this.$router.push('/login');
            },
            after_write(resp){
                console.log('RESP:', resp);
                this.connect_user_chat(resp.chat_id, this.user.id);
                this.connect_user_chat(resp.chat_id, localStorage.getItem('user_id'));
                this.$router.push('/chat/' + resp.chat_id);
            },
            connect_user_chat(c_id, u_id){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/chat/" + c_id + "/" + u_id + "/join")
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => console.log(response.data));
                else
                    this.$router.push('/login');
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

<style lang="scss">
    @import '../assets/scss/_partial';
    .me{
        font-family: $font;

        &-avatar{
            width: 150px;
            border-radius: 5px;
        }
    }
</style>