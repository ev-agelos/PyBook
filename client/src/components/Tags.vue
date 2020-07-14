<template>
    <div v-if="show === true" class="modal is-active">
        <div class="modal-background" @click="show = false"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">Find bookmarks by tag</p>
                <button @click="show = false" class="delete is-pulled-right" aria-label="close"></button>
            </header>
            <section class="modal-card-body">
                <article class="media">
                    <div class="media-content">
                        <div class="content">
                            <div class="tags are-large">
                                <span v-for="tag in tags" :key="tag.name" class="tag">
                                    <a v-text="'#' + tag.name" @click="fetchBookmarksByTag(tag.name)"></a>-{{tag.count}}
                                </span>
                            </div>
                        </div>
                    </div>
                </article>
            </section>
        </div>
    </div>
</template>


<script>
import {getTags, getBookmarks} from '../api.js'

export default {
    name: "Tags",
    data() {
        return {
            show: false,
            tags: []
        }
    },
    methods: {
        open() {
            this.show = true;
            getTags().then(data => this.tags = data);
        },
        fetchBookmarksByTag(tag){
            getBookmarks("?tag=" + tag).then(data => this.$root.bookmarks = data.bookmarks);
            this.show = false;
        }
    }
}
</script>
