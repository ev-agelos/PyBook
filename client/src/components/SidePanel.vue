<template>
    <div>
        <nav class="panel" style="width: 200px;">
            <p class="panel-heading">
                <a href="/">
                    <img src="../assets/img/logo_200x200.png">
                </a>
            </p>
            <div class="panel-block">
                <div class="control has-icons-left">
                    <input class="input" type="text" placeholder="Search" disabled>
                    <span class="icon is-left">
                        <i class="mdi mdi-magnify" aria-hidden="true"></i>
                    </span>
                </div>
            </div>
        </nav>

        <aside class="menu">
            <ul class="menu-list">
                <li><a @click="fetchBookmarks"><span><i class="mdi mdi-bookmark"></i></span> Home</a></li>
                <li @click="openTags"><a><span><i class="mdi mdi-tag-multiple"></i></span> Tags</a></li>
                <li @click="openUsers"><a><span><i class="mdi mdi-account-supervisor"></i></span> Users</a></li>
                <hr class="divider">
                <div v-if="this.$root.store.isAuthenticated">
                    <li><a @click="fetchSubscriptionBookmarks"><span><i class="mdi mdi-bookmark"></i></span> Subscriptions</a></li>
                    <li><a @click="fetchUserBookmarks(user.id)"><span><i class="mdi mdi-bookmark"></i></span> Your bookmarks</a></li>
                    <li><a @click="fetchFavouriteBookmarks"><span><i class="mdi mdi-heart"></i></span> Saved</a></li>
                    <hr class="divider">
                    <p class="menu-label">Subscriptions</p>
                    <li>
                        <a v-for="user in user.subscribed" :key="user.id" @click="fetchUserBookmarks(user.id)">
                            <span class="icon">
                                <i class="mdi mdi-account"></i>
                            </span>{{user.username}}
                        </a>
                    </li>
                </div>
            </ul>
        </aside>
    <Tags ref="Tags" />
    <Users ref="Users" />
    </div>
</template>

<script>
import {getBookmarks, getFavourites} from '../api.js'
import Tags from './Tags.vue'
import Users from './Users.vue'

export default {
  name: 'SidePanel',
  components: {
      Tags,
      Users
  },
  data() {
    return {
        user: {}
    }
  },
  methods: {
      openTags() {
          this.$refs.Tags.open();
      },
      openUsers() {
          this.$refs.Users.open();
      },
      fetchBookmarks() {
        getBookmarks().then(data => this.$root.bookmarks = data.bookmarks);
      },
      fetchSubscriptionBookmarks() {
        if (this.user.subscribed.length) {
          let queryString = this.user.subscribed.length ? "?user_id=" + this.user.subscribed.map(x => x.id).join('&user_id=') : '';
          getBookmarks(queryString).then(data => this.$root.bookmarks = data.bookmarks);
        } else {
            this.$root.bookmarks = [];
        }
      },
      fetchUserBookmarks(user_id) {
          getBookmarks("?user_id=" + user_id).then(data => this.$root.bookmarks = data.bookmarks);
      },
      fetchFavouriteBookmarks() {
          getFavourites().then(data => {
            this.$root.user.favourites = data;
            if (data.length) {
                let queryString = "?id=" + data.map(x => x['bookmark_id']).join("&id=");
                getBookmarks(queryString).then(data => this.$root.bookmarks = data.bookmarks);
            } else {
                this.$root.bookmarks = [];
            }
        })
      }
  },
  mounted() {
      this.$root.$on('authenticated', () => {
        this.user = this.$root.user
      })
  }
}
</script>
