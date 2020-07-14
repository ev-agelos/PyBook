<template>
        <div class="columns">
            <div class="column is-7 is-offset-2">
                <br>
                <Bookmark v-for="bookmark in bookmarks" :key="bookmark.id" ref="Bookmark" :bookmark="bookmark" />

                <nav class="pagination is-centered" role="navigation" aria-label="pagination">
                    <a @click="fetchBookmarks('?page=' + $root.pagination.previous_page)" class="pagination-previous" :disabled="$root.pagination.previous_page == null">Previous</a>
                    <a @click="fetchBookmarks('?page=' + $root.pagination.next_page)" class="pagination-next" :disabled="$root.pagination.next_page == null">Next page</a>
                    <ul class="pagination-list">
                        <li v-if="$root.pagination.total_pages > 3">
                            <a v-text="$root.pagination.first_page" class="pagination-link" :aria-label="'Goto page ' + $root.pagination.first_page"></a>
                        </li>
                        <li v-if="$root.pagination.total_pages > 3">
                            <span class="pagination-ellipsis">&hellip;</span>
                        </li>
                        <li v-if="$root.pagination.previous_page">
                            <a @click="fetchBookmarks('?page=' + $root.pagination.previous_page)" v-text="$root.pagination.previous_page" class="pagination-link" :aria-label="'Goto page ' + $root.pagination.previous_page"></a>
                        </li>
                        <li>
                            <a v-text="$root.pagination.page" class="pagination-link is-current" :aria-label="'Page ' + $root.pagination.page" aria-current="page"></a>
                        </li>
                        <li v-if="$root.pagination.next_page">
                            <a @click="fetchBookmarks('?page=' + $root.pagination.next_page)" v-text="$root.pagination.next_page" class="pagination-link" :aria-label="'Goto page ' + $root.pagination.next_page"></a>
                        </li>
                        <li v-if="$root.pagination.total_pages > 3">
                            <span class="pagination-ellipsis">&hellip;</span>
                        </li>
                        <li v-if="$root.pagination.total_pages > 3">
                            <a v-text="$root.pagination.last_page" class="pagination-link" :aria-label="'Goto page' + $root.pagination.last_page"></a>
                        </li>
                    </ul>
                </nav>
            </div>

            <div class="column is-1">
                <br>
                <div class="dropdown is-hoverable">
                    <div class="dropdown-trigger">
                        <button class="button" aria-haspopup="true" aria-controls="dropdown-menu4" :disabled="bookmarks.length < 2">
                            <span class="icon">
                                <i class="mdi mdi-sort-variant" aria-hidden="true"></i>
                            </span>
                            <span>Sort</span>
                        </button>
                    </div>
                    <div v-if="bookmarks.length > 1" class="dropdown-menu" id="dropdown-menu4" role="menu">
                        <div class="dropdown-content">
                            <a @click="orderBy('date')" class="dropdown-item">New</a>
                            <a @click="orderBy('-date')" class="dropdown-item">Oldest</a>
                            <a @click="orderBy('rating')" class="dropdown-item">Top</a>
                            <a @click="orderBy('-rating')" class="dropdown-item">Unpopular</a>
                        </div>
                    </div>
                </div>
            </div>
        </div>
</template>

<script>
import {getBookmarks} from '../api.js'
import Bookmark from './Bookmark.vue'

export default {
  name: 'Bookmarks',
  components: {
      Bookmark
  },
  methods: {
      orderBy(by) {
          getBookmarks("?sort=" + by).then(data => {
              this.$root.bookmarks = data.bookmarks;
              this.$root.pagination = data.pagination;
          });
      },
      fetchBookmarks(queryString) {
          getBookmarks(queryString).then(data => {
              this.$root.bookmarks = data.bookmarks;
              this.$root.pagination = data.pagination;
          });
      }
  },
  mounted() {
      getBookmarks().then(data => {
          this.$root.bookmarks = data.bookmarks;
          this.$root.pagination = data.pagination;
      });
  },
  computed: {
    bookmarks: function() {
        return this.$root.bookmarks
    }
  }
}
</script>
