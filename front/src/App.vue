<template>
  <v-app>
      <Sidebar v-if="$route.name !== 'Login' && $route.name !== 'Registration'" :user="user" />
      <div class="content" :style="contentStyle">
          <router-view/>
      </div>
  </v-app>
</template>

<script>

import Sidebar from "@/components/Sidebar";
import axios from "axios";
export default {
  name: 'App',
    components: {Sidebar},
    data: () => ({
        user: {
            avatar: require('./assets/images/user_logo.png'),
            name: 'Имя',
            surname: 'Фамилия',
            descr: 'Описание',
            nick: 'Никнейм',
        },
        width: Number,
        height: Number,
    }),
    watch: {
      $route(){
          if(this.$route.name !== 'Registration')
            this.getUser();
      }
    },
    mounted: function(){
        this.getUser();
    },
    computed: {
        contentStyle(){
            if(this.width < 950)
                return 'width: calc(100% - 56px); left: 56px;';
            return '';
        }
    },
    methods: {
      getUser(){
          if(localStorage.getItem('token'))
              axios
                  .get("http://dvv2423.fvds.ru:84/api/me",
                      {headers: {'x-access-token': localStorage.getItem('token')}})
                  .catch(function(error){
                      console.log(error);
                  })
                  .then(response => this.response(response));
          else
              this.$router.push('/login');
      },
        response(response){
            console.log('Route', this.$router);
            console.log('Ответ: ', response);
            localStorage.setItem('user_id', this.user.id);
            this.user = response.data;
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
};
</script>

<style lang="scss">
    @import 'assets/scss/_partial';
    .content{
        position: absolute;
        left: 256px;
        width: calc(100% - 256px);
        height: 100%;
        background-color: #d7d7d7;

        overflow-y: scroll;
    }
</style>
