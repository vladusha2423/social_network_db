<template>
    <div class="me">
        <v-row :class="{'ml-2': width >= 550, 'ml-1': width < 550}"
               :justify="width < 550 ? 'center' : ''"
               :align="width < 550 ? 'center' : ''">
            <div>
                <v-card class="flex-column mt-4 pt-4 pb-4" width="200">
                    <v-row align="center" justify="center">
                        <img
                                :src="pub.avatar || require('../assets/images/group_icon.png')"
                                class="me-avatar mt-3"
                                alt="user avatar" />
                    </v-row>
                    <v-row align="center" justify="center">
                        <v-btn class="mt-6"
                               @click="subscribe()">
                            Подписаться
                        </v-btn>
                    </v-row>

                </v-card>
            </div>
            <div class="d-flex flex-column ml-5 mt-2 me-description">
                <v-row>
                    <v-card class="flex-column mt-2 pr-2 pl-2 pt-2" max-width="600px" width="90%">
                        <h3>{{pub.title}}</h3>
                        <p class="mt-4">{{pub.description}}</p>
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
        <v-row class="ml-2" v-for="(item, i) in posts" :key="i">
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
            pub: {
                avatar: require('../assets/images/group_icon.png'),
                title: 'Название',
                description: 'Описание',
            },
            posts: [],
            isAdmin: true,
            text: '',
            width: Number,
            height: Number,
        }),
        beforeCreate(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/public/" + this.$route.params.id)
                    .catch(function(error){
                        console.log(error);
                    })
                    .then(response => this.after_public(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_public(response){
                console.log('Route', this.$router);
                console.log('Public: ', response);
                this.pub = response.data;
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
                        .get("http://dvv2423.fvds.ru:84/api/posts/public/" + this.$route.params.id)
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_posts(response));
                else
                    this.$router.push('/login');
            },
            subscribe() {
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/public/" + this.pub.id + "/subscribe", {},
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => alert(response.data));
                else
                    this.$router.push('/login');
            },
            new_post(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/posts",
                            {'text': this.text, 'photo': '', 'views': 0, 'likes': 0})
                        .catch(function(error){
                            alert(error);
                        })
                        .then(response => this.connect_post_public(response.data));
                else
                    this.$router.push('/login');
            },
            connect_post_public(resp){
                console.log('RESP :', resp)
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/post/" + resp.post_id + "/" + this.pub.id + "/2public")
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
    }
</style>