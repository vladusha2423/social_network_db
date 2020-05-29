<template>
    <div class="messages">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <v-toolbar-title class="ml-4">Сообщения</v-toolbar-title>
        </v-app-bar>
        <v-list three-line max-width="800px" width="90%" class="ml-4 mt-4">
            <template v-for="(item, index) in messages">
                <v-list-item
                        :key="index"
                        @click="redirect('/chat/' + item.id)"
                >
                    <v-list-item-avatar>
                        <v-img :src="item.avatar"></v-img>
                    </v-list-item-avatar>

                    <v-list-item-content>
                        <v-list-item-title v-html="item.title"></v-list-item-title>
                        <v-list-item-subtitle v-html="item.count + ' участника'"></v-list-item-subtitle>
                    </v-list-item-content>
                </v-list-item>

                <v-divider
                        :key="index"
                        inset
                ></v-divider>
            </template>
<!--            <v-list-item v-for="(item, i) in messages" :key="i">-->
<!--                <v-list-item-avatar>-->
<!--                    <v-img :src="item.avatar"></v-img>-->
<!--                </v-list-item-avatar>-->
<!--                <v-list-item-content>-->
<!--                    <v-list-item-title v-html="item.title"></v-list-item-title>-->
<!--                    <v-list-item-subtitle v-html="item.count"></v-list-item-subtitle>-->
<!--                </v-list-item-content>-->
<!--            </v-list-item>-->
        </v-list>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Messages",
        data(){
            return {
                messages: Array,
            }
        },
        created(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/me/chats",
                        {headers: {'x-access-token': localStorage.getItem('token')}})
                    .then(response => this.after_request(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_request(response){
                console.log('Route', this.$route.name);
                console.log('messages: ', response);
                this.messages = response.data;
            },
            redirect(path){
                this.$router.push(path);
            }
        }
    }
</script>

<style scoped>

</style>