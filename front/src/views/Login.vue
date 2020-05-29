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
                        <v-toolbar-title>Авторизация</v-toolbar-title>
                        <v-spacer></v-spacer>
                        <v-btn @click="redirect('/registration')">Регистрация</v-btn>
                    </v-toolbar>
                    <v-card-text>
                        <v-form @submit="auth()">
                            <v-text-field
                                    label="Login"
                                    name="login"
                                    type="text"
                                    v-model="login"
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
                        <v-btn color="primary" @click="auth()">Login</v-btn>
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
                password: '',
            }
        },
        methods: {
            auth(){
                axios
                    .post('http://dvv2423.fvds.ru:84/api/login',
                        {
                            login: this.login,
                            password: this.password,
                        },
                    )
                    .then((response) => this.after_login(response));
            },
            after_login(response){
                localStorage.setItem('token', response.data.token);
                console.log('User', response);
                this.$router.push('/');
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