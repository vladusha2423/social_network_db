<template>
    <div class="me">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <v-toolbar-title class="ml-4">Моя страница</v-toolbar-title>
        </v-app-bar>
        <v-row :class="{'ml-2': width >= 550, 'ml-1': width < 550}"
               :justify="width < 550 ? 'center' : ''"
               :align="width < 550 ? 'center' : ''">
            <div>
                <v-card class="flex-column mt-4 pt-2" width="200">
                    <v-row align="center" justify="center">
                        <img
                                :src="user.avatar || require('../assets/images/user_logo.png')"
                                class="me-avatar mt-3"
                                alt="user avatar" />
                    </v-row>
                    <v-row align="center" justify="center">
                        <v-btn class="mt-4"
                               @click="getSubs()">
                            Подписчики
                        </v-btn>
                    </v-row>
                    <v-row align="center" justify="center">
                        <v-btn
                                @click="getPubs()"
                                class="mt-4 mb-3">
                            Группы
                        </v-btn>
                    </v-row>

                </v-card>
            </div>
            <div class="d-flex flex-column ml-5 mt-2 me-description">
                <v-row>
                    <v-card class="flex-column mt-2 pr-2 pl-2 pt-2" max-width="600px" width="90%">
                        <h3>{{user.name + ' ' + user.surname}}</h3>
                        <p class="mt-4">{{user.descr}}</p>
                        <p><b>{{user.nick}}</b></p>
                    </v-card>
                </v-row>
                <v-row class="mt-1">
                        <v-card class="mt-2 pr-2 pl-2" max-width="600px" width="90%">
                            <v-textarea
                                    name="user_post"
                                    label="Что нового?"
                                    rows="2"
                                    value=""
                                    v-model="text"
                            ></v-textarea>
                            <v-btn class="mb-2" @click="new_post()">Запостить!</v-btn>
                        </v-card>
                </v-row>
            </div>

        </v-row>

        <div class="d-flex flex-column-reverse">
            <v-row class="ml-2 " v-for="(item, i) in posts" :key="i">
                <v-card class="mt-3" max-width="775px" width="93%">
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

        <v-dialog
                v-model="subscribersModal"
                max-width="290"
        >
            <v-card>
                <v-list subheader>
                    <v-subheader>Подписчики</v-subheader>

                    <p v-if="subs.length === 0" class="ml-4"> Подписчиков пока нет </p>
                    <v-list-item
                            v-for="item in subs"
                            :key="item.title"
                            @click="redirect('/user/' + item.id)"
                    >
                        <v-list-item-avatar>
                            <v-img :src="item.avatar || require('../assets/images/user_logo.png')"></v-img>
                        </v-list-item-avatar>

                        <v-list-item-content>
                            <v-list-item-title v-text="item.name + ' ' + item.surname"></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

            </v-card>
        </v-dialog>
        <v-dialog
                v-model="publicsModal"
                max-width="290"
        >
            <v-card>
                <v-list subheader>
                    <v-subheader>Мои группы</v-subheader>

                    <p v-if="pubs.length === 0" class="ml-4"> Вы не подписаны ни на одну группу </p>

                    <v-list-item
                            v-for="item in pubs"
                            :key="item.title"
                            @click="redirect('/public/' + item.id)"
                    >
                        <v-list-item-avatar>
                            <v-img :src="item.avatar || require('../assets/images/group_icon.png')"></v-img>
                        </v-list-item-avatar>

                        <v-list-item-content>
                            <v-list-item-title v-text="item.title"></v-list-item-title>
                        </v-list-item-content>
                    </v-list-item>
                </v-list>

            </v-card>
        </v-dialog>
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
            },
            subs: Array,
            pubs: Array,
            subscribersModal: false,
            publicsModal: false,
            posts: [],
            text: '',
            width: Number,
            height: Number,
        }),
        beforeCreate(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/me",
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
            after_subs(response){
                console.log('Route: ', this.$router);
                console.log('My subscribers: ', response);
                this.subs = response.data;
            },
            after_pubs(response){
                console.log('Route: ', this.$router);
                console.log('My publics: ', response);
                this.pubs = response.data;
            },
            getSubs(){
                if(localStorage.getItem('token'))
                    axios
                        .get("http://dvv2423.fvds.ru:84/api/me/subscribers",
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_subs(response));
                else
                    this.$router.push('/login');

                this.subscribersModal = true;
            },
            getPubs(){
                if(localStorage.getItem('token'))
                    axios
                        .get("http://dvv2423.fvds.ru:84/api/me/publics",
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_pubs(response));
                else
                    this.$router.push('/login');

                this.publicsModal = true;
            },
            after_posts(response){
                console.log('Route', this.$router);
                console.log('Posts: ', response);
                this.posts = response.data;
            },
            get_posts(){
                if(localStorage.getItem('token'))
                    axios
                        .get("http://dvv2423.fvds.ru:84/api/posts/user/" + this.user.id)
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_posts(response));
                else
                    this.$router.push('/login');
            },
            redirect(path){
                this.$router.push(path);
            },
            new_post(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/posts",
                            {'text': this.text, 'photo': '', 'views': 0, 'likes': 0})
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => this.connect_post_user(response.data));
                else
                    this.$router.push('/login');
            },
            connect_post_user(resp){
                console.log('RESP :', resp)
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/post/" + resp.post_id + "/2user",
                            {'text': this.text, 'photo': '', 'views': 0, 'likes': 0},
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => this.after_connect(response.data));
                else
                    this.$router.push('/login');
            },
            after_connect(data){
                console.log(data);
                this.get_posts();
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
        &-description{
            max-width: 600px;
            width: calc(95% - 200px);
            min-width: 200px;
            @media(max-width: 550px){
                width: 95%;
            }
        }
    }
</style>