<template>
    <div class="modal is-active">
        <div class="modal-background"></div>
        <div class="modal-card">
            <header class="modal-card-head">
                <p class="modal-card-title">
                    <slot name="header"></slot>
                </p>
                <button @click="$emit('close')" class="delete" aria-label="close"></button>
            </header>

            <section class="modal-card-body">
                <b-field label="Url">
                    <b-input v-model="url" type="url"></b-input>
                </b-field>

                <b-field label="Title">
                    <b-field>
                        <b-input v-model="title" expanded minlength="10" :disabled="onSuggesting"></b-input>
                        <p class="control">
                            <button @click="fetchTitle" :disabled="onSuggesting" :class="{'is-loading': onSuggesting}" class="button is-info">Suggest</button>
                        </p>
                    </b-field>
                </b-field>

                <b-field label="Tags">
                    <b-taginput
                        v-model="tags"
                        minlength="3"
                        ellipsis
                        icon="label">
                    </b-taginput>
                </b-field>

            </section>

            <footer class="modal-card-foot">
                <button @click="submitForm" class="button is-success">
                    <slot name="footer"></slot>
                </button>
                <button @click="$emit('close')" class="button">Cancel</button>
            </footer>
        </div>
    </div>
</template>

<script>
import {getBookmark, postBookmarks, putBookmark, suggestTitle} from '../api.js'

export default {
  name: 'BookmarkForm',
  props: {
    bookmark: {
        type: Object,
        default: function() {
            return {
                title: '',
                url: '',
                tags: []
            };
        }
    },
    updateMode: {
        type: Boolean,
        default: false
    }
  },
  data() {
    return {
      onSuggesting: false,
      title: '',
      url: '',
      tags: []
    }
  },
  methods: {
    submitForm() {
        if (this.updateMode) {
            this.updateBookmark() 
        } else {
            this.addBookmark()
        }
    },
    addBookmark() {
        postBookmarks({title: this.title, url: this.url, tags: this.tags})
            .then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    getBookmark(data.location.split('/').pop())
                        .then(data => {
                            if (data.message || data.status) {
                                this.$root.$emit('notification', data.message || data.status);
                            } else {
                                this.$root.bookmarks.unshift(data);
                                this.$buefy.toast.open('Bookmark added');
                            }
                        })
                }
            })
    },
    updateBookmark() {
        putBookmark(this.bookmark.id, {'title': this.title, 'url': this.url, 'tags': this.tags})
            .then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    this.bookmark.title = this.title;
                    this.bookmark.url = this.url;
                    this.bookmark.tags = this.tags.map(tag => ({'name': tag}));
                    this.$buefy.toast.open('Bookmark updated');
                }
            })
    },
    fetchTitle() {
        this.onSuggesting = true;
        suggestTitle(this.url).then(data => {
            if (data.message || data.status) {
                this.$root.$emit('notification', data.message || data.status);
            } else {
                this.title = data.title;
            }
            this.onSuggesting = false;
        });
    }
  },
  created() {
      this.title = this.bookmark.title;
      this.url = this.bookmark.url;
      this.tags = this.bookmark.tags.map(tag => tag['name']);
  }
}
</script>
