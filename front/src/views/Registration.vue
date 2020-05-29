<template>
    <v-container
            class="fill-height login"
            fluid
    >
        <v-row
                align="center"
                justify="center"
        >
            <v-col
                    cols="12"
                    sm="8"
                    md="4"
            >
                <v-card class="elevation-12">
                    <v-toolbar
                            color="primary"
                            dark
                            flat
                    >
                        <v-toolbar-title>Регистрация</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn @click="redirect('/login')">Авторизация</v-btn>
                    </v-toolbar>
                    <v-card-text>
                        <v-form @submit="auth()">
                            <v-text-field
                                    label="Логин"
                                    name="login"
                                    type="text"
                                    v-model="login"
                            ></v-text-field>
                            <v-text-field
                                    label="Имя"
                                    name="name"
                                    type="text"
                                    v-model="name"
                            ></v-text-field>
                            <v-text-field
                                    label="Фамилия"
                                    name="surname"
                                    type="text"
                                    v-model="surname"
                            ></v-text-field>
                            <v-text-field
                                    label="Ссылка на фотку"
                                    name="avatar"
                                    type="text"
                                    v-model="avatar"
                            ></v-text-field>
                            <v-text-field
                                    label="Немного о себе"
                                    name="descr"
                                    type="text"
                                    v-model="descr"
                            ></v-text-field>

                            <v-text-field
                                    id="password"
                                    label="Password"
                                    name="password"
                                    type="password"
                                    v-model="password"
                            ></v-text-field>
                        </v-form>
                    </v-card-text>
                    <v-card-actions>
                        <v-spacer></v-spacer>
                        <v-btn color="primary" @click="auth()">Зарегаться!</v-btn>
                    </v-card-actions>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<script>
    import axios from "axios";

    export default {
        name: "Login",
        data(){
            return{
                login: '',
                name: '',
                surname: '',
                avatar: '',
                descr: '',
                password: '',
            }
        },
        methods: {
            auth(){
                axios
                    .post('http://dvv2423.fvds.ru:84/api/users',
                        {
                            nick: this.login,
                            name: this.name,
                            surname: this.surname,
                            avatar: this.avatar,
                            descr: this.descr,
                            password: this.password,
                        },
                    )
                    .then((response) => this.after_login(response));
            },
            after_login(response){
                localStorage.setItem('token', response.data.token);
                console.log('User', response);
                this.$router.push('/login');
            },
            redirect(path){
                this.$router.push(path);
            }
        }
    }
</script>

<style lang="scss" scoped>
    .login{
        width: calc(100vw + 256px)!important;
    }
</style>