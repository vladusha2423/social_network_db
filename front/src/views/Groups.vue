<template>
    <div class="groups">
        <v-app-bar color="indigo darken-2" dense dark height="60px">
            <v-toolbar-title class="ml-4">Группы</v-toolbar-title>
            <v-btn class="mx-2" fab dark color="light-blue" @click="publicModal = true">
                <v-icon dark>mdi-plus</v-icon>
            </v-btn>
        </v-app-bar>
        <v-row class="ml-4 mt-4" v-for="(item, i) in groups" :key="i">
            <v-card class="d-flex flex-row pl-3 pt-3" max-width="600px" width="90%" hover @click="$router.push('/public/' + item.id)">
                <div>
                    <img :src="item.avatar || require('../assets/images/group_icon.png')"
                         alt="group avatar"
                         class="groups-photo" />
                </div>
                <div class="ml-3">
                    <h3>{{item.title}}</h3>
                    <p>{{item.description}}</p>
                </div>


            </v-card>
        </v-row>
        <v-dialog
                v-model="publicModal"
                max-width="290"
        >
            <v-card>
                <v-list subheader>
                    <v-card-title class="mt-3"><h3 class="ml-3">Создать группу</h3></v-card-title>
                    <v-card-text>
                        <v-form @submit="create_public()">
                            <v-text-field
                                    label="Название"
                                    name="title"
                                    type="text"
                                    v-model="title"
                            ></v-text-field>
                            <v-text-field
                                    label="Аватарка"
                                    name="avatar"
                                    type="text"
                                    v-model="avatar"
                            ></v-text-field>
                            <v-text-field
                                    label="Описание"
                                    name="description"
                                    type="text"
                                    v-model="description"
                            ></v-text-field>

                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="create_public()">Создать!</v-btn>
                    </v-card-actions>
                </v-list>

            </v-card>
        </v-dialog>
    </div>
</template>

<script>
    import axios from "axios";

    export default {
        name: "groups",
        data(){
            return {
                groups: Array,
                publicModal: false,
                title: '',
                avatar: '',
                description: '',

            }
        },
        created(){
            if(localStorage.getItem('token'))
                axios
                    .get("http://dvv2423.fvds.ru:84/api/publics")
                    .then(response => this.after_request(response));
            else
                this.$router.push('/login');
        },
        methods: {
            after_request(response){
                console.log('Route', this.$route.name);
                console.log('Groups: ', response);
                this.groups = response.data;
            },
            create_public(){
                if(localStorage.getItem('token'))
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/publics",
                            {'title': this.title, 'avatar': this.avatar, 'description': this.description})
                        .catch(error => alert(error))
                        .then(response => this.connect_user_public(response.data));
                else
                    this.$router.push('/login');
            },
            connect_user_public(resp){
                alert(resp);
                if(localStorage.getItem('token')) {
                    axios
                        .post("http://dvv2423.fvds.ru:84/api/me/public/" + resp.public_id + "/subscribe", {},
                            {headers: {'x-access-token': localStorage.getItem('token')}})
                        .catch(function (error) {
                            alert(error);
                        })
                        .then(response => alert(response.data));
                    this.$router.push('/public/' + resp.public_id);
                }
                else
                    this.$router.push('/login');

            }
        }
    }
</script>

<style lang="scss" scoped>
    .groups{
        &-photo{
            width: 80px;
            height: 80px;
            border-radius: 5px;
        }
    }
</style>