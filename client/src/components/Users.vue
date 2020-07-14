<template>
    <div v-if="show === true" class="modal is-active">
        <div class="modal-background" @click="show = false"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Find bookmarks per user</p>
                <button @click="show = false" class="delete is-pulled-right" aria-label="close"></button>
            </header>
            <section class="modal-card-body">
                <article class="media">
                    <div class="media-content">
                        <div class="content">
                            <ul>
                                <li v-for="user in users" :key="user.username">
                                    <a v-text="user.username" @click="fetchUserBookmarks(user.id)"></a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </article>
            </section>
        </div>
    </div>
</template>


<script>
import {getUsers, getBookmarks} from '../api.js'

export default {
    name: "Users",
    data() {
        return {
            show: false,
            users: []
        }
    },
    methods: {
        fetchUserBookmarks(user_id) {
            getBookmarks("?user_id=" + user_id).then(data => {
                this.$root.bookmarks = data.bookmarks;
            })
            this.show = false;
        },
        open() {
            getUsers().then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    this.users = data;
                    this.show = true;
                }
            })
        }
    }
}
</script>
