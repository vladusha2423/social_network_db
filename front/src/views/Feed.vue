<template>
    <div class="feed">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <v-toolbar-title class="ml-4">Новости</v-toolbar-title>
        </v-app-bar>
        <p v-if="feed.length === 0" class="ml-4"> Постов нет </p>
        <v-row class="ml-4" v-for="(item, i) in feed" :key="i">
            <v-card class="mt-2" max-width="600px" width="90%" >
                <v-row class="mt-3">
                    <img :src="item[2] || require('../assets/images/group_icon.png')"
                         alt="post_owner"
                         class="ml-7"
                         style="width:40px;height:40px;border-radius:50%"/>
                    <h4 class="mt-2 ml-2">{{ item[1] }}</h4>
                </v-row>
                <v-row class="ml-4 mt-4" style="width: 95%">
                    {{item[0].text}}
                </v-row>
                <v-row class="ml-4">
                    <v-btn icon>
                        <v-icon>mdi-heart</v-icon>
                    </v-btn>
                    <div class="mt-1">
                        {{item[0].likes}}
                    </div>
                    <v-btn icon class="ml-8">
                        <v-icon>mdi-comment</v-icon>
                    </v-btn>
                    <div class="mt-1">
                        {{item[0].views}}
                    </div>
                </v-row>
            </v-card>
            <p style="color: gray;" class="ml-2 mt-4"> {{ item.time}}</p>
        </v-row>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Feed",
        data(){
            return{
                feed: Array,
            }
        },
        created(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/me/feed",
                        {headers: {'x-access-token': localStorage.getItem('token')}})
                    .catch(function(error){
                        console.log(error);
                    })
                    .then(response => this.after_request(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_request(response){
                console.log('Feed: ', response);
                this.feed = response.data;
            }
        }
    }
</script>

<style scoped>

</style>