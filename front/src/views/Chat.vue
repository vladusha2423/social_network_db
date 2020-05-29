<template>
    <div class="chat">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <div class="chat-photo">
                <img :src="chat.avatar || require('../assets/images/user_logo.png')"
                     alt="user avatar"
                     style="width: 100%; height: 100%;"
                     class="users-photo" />
            </div>
            <v-toolbar-title class="ml-4">{{chat.title}}</v-toolbar-title>
        </v-app-bar>
        <v-card width="100%" min-height="50px" max-height="100px">
            <v-row>
                <v-text-field
                        class="ml-4"
                        v-model="text"
                        label="Введите сообщение"
                ></v-text-field>
                <v-btn color="primary" :small="width < 620" @click="send_msg()" class="mt-4">Отправить</v-btn>
            </v-row>



        </v-card>
        <div class="d-flex flex-column-reverse">
            <v-row class="ml-4 mt-4"
                   v-for="(item, i) in msgs"
                   :key="i">
                <div class="chat-photo">
                    <img :src="msgAvatar(item.sentby) || require('../assets/images/user_logo.png')"
                         alt="user avatar"
                         style="width: 100%; height: 100%;"
                         class="users-photo" />
                </div>

                <v-card class="d-flex flex-row pl-3 pt-3 ml-2" max-width="600" width="calc(90% - 45px)">
                    {{item.text}}
                </v-card>
                <p style="color: gray;" class="ml-2 mb-0"> {{ item.time}}</p>
            </v-row>
        </div>

    </div>
</template>

<script>
    import axios from 'axios';
    export default {
        name: "Chat",
        data(){
            return{
                chat: Object,
                msgs: [],
                text: '',
                width: Number,
                height: Number,
            }
        },
        beforeCreate(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/chat/" + this.$route.params.id,
                        {headers: {'x-access-token': localStorage.getItem('token')}})
                    .catch(function(error){
                        console.log(error);
                    })
                    .then(response => this.after_chat(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_chat(response){
                console.log('Route', this.$router);
                console.log('Chat: ', response);
                this.chat = response.data;
                this.get_msgs();
            },
            after_msgs(response){
                console.log('Route', this.$router);
                console.log('Msgs: ', response);
                this.msgs = response.data;
            },
            get_msgs(){
                if(localStorage.getItem('token'))
                    axios
                        .get("http://dvv2423.fvds.ru:84/api/me/chat/" + this.$route.params.id,
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_msgs(response));
                else
                    this.$router.push('/login');
            },
            msgAvatar(id){
                console.log(this.chat.members[0]);
                for(let m = 0; m < this.chat.members.length; m++){
                    if(this.chat.members[m].id === id)
                        return this.chat.members[m].avatar;
                }
                return require('../assets/images/user_logo.png')
            },
            send_msg(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/message/" + this.$route.params.id,
                            {text: this.text},
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function(error){
                            console.log(error);
                        })
                        .then(response => this.after_msg(response));
                else
                    this.$router.push('/login');
            },
            after_msg(resp){
                console.log(resp.data);
                this.get_msgs();

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

<style lang="scss" scoped>
    .chat{

        &-photo{
            width: 45px;
            height: 45px;
            border-radius: 50%;
            background: white;
            overflow: hidden;
        }
    }
</style>