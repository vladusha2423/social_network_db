<template>
    <v-navigation-drawer
            v-model="drawer"
            absolute
            bottom
            temporary
    >
        <v-list
                nav
                dense
        >
            <v-list-item-group
                    active-class="deep-purple--text text--accent-4"
            >
                <v-list-item @click="redirect('/journals')">
                    <v-list-item-title>Journals</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/releases')">
                    <v-list-item-title>Releases</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/rubrics')">
                    <v-list-item-title>Rubricators</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/posts')">
                    <v-list-item-title>Posts</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/report1')">
                    <v-list-item-title>Releases by journals</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/report2')">
                    <v-list-item-title>Posts by rubricators</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/journals2020')">
                    <v-list-item-title>Jornals havin' 2020 releases</v-list-item-title>
                </v-list-item>

                <v-list-item @click="redirect('/rubrics2posts')">
                    <v-list-item-title>Rubrics havin' >= 2 posts</v-list-item-title>
                </v-list-item>
            </v-list-item-group>
        </v-list>
    </v-navigation-drawer>
</template>

<script>
    export default {
        name: "Navigation",
        props: {
            drawer: Boolean,
        },
        methods: {
            redirect: function(path){
                this.$router.push(path);
            }
        },
    }
</script>

<style scoped>

</style>