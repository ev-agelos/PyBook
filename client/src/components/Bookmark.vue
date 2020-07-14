<template>
    <div class="box">
        <div class="columns">
            <div class="column is-narrow">
                <div class="box" style="width: 104px;">
                    <figure class="image is-64x64">
                        <img v-if="bookmark.image" :src="bookmark.image" alt="Image">
                        <img v-else src="../assets/img/default.png" alt="Image">
                    </figure>
                </div>
            </div>

            <div class="column">
                <div class="content">
                    <div class="is-pulled-right">
                        <a v-if="bookmark.user.id === this.$root.user.id" @click="deleteBookmark" class="button" aria-label="delete">
                            <span class="icon">
                                <i class="mdi mdi-delete" aria-hidden="true"></i>
                            </span>
                            <span>delete</span>
                        </a>
                        <a v-if="bookmark.user.id === this.$root.user.id" @click="showBookmarkForm = true" class="button" aria-label="edit">
                            <span class="icon">
                                <i class="mdi mdi-pencil" aria-hidden="true"></i>
                            </span>
                            <span>edit</span>
                        </a>
                        <button @click="favouriteBookmark" class="button" aria-label="like">
                            <span class="icon">
                                <i v-if="favourite" class="has-text-primary mdi mdi-heart" aria-hidden="true"></i>
                                <i v-else class="has-text-primary mdi mdi-heart-outline" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>

                    <p>
                        <strong><a :href="bookmark.url" v-text="bookmark.title" target="_blank" rel="noopener noreferrer"></a></strong>
                    </p>
                </div>
            </div>
        </div>
        <div class="columns is-vcentered">
            <div class="column is-narrow">
                <div class="level" style="width: 104px;">
                    <div class="level-left">
                        <button v-if="voteDirection === true" @click="upVote" class="button is-success has-background-success-light">
                            <span class="icon">
                                <i class="mdi mdi-plus mdi-18px" aria-hidden="true"></i>
                            </span>
                        </button>
                        <button v-else @click="upVote" class="button is-success is-inverted">
                            <span class="icon">
                                <i class="mdi mdi-plus mdi-18px" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>

                    <p>{{bookmark.rating}}</p>

                    <div class="level-right">
                        <button v-if="voteDirection === false" @click="downVote" class="button is-danger has-background-danger-light">
                            <span class="icon">
                                <i class="mdi mdi-minus mdi-18px" aria-hidden="true"></i>
                            </span>
                        </button>
                        <button v-else @click="downVote" class="button is-danger is-inverted">
                            <span class="icon">
                                <i class="mdi mdi-minus mdi-18px" aria-hidden="true"></i>
                            </span>
                        </button>
                    </div>
                </div>
            </div>
            <div class="column">
                <div class="level">
                    <div class="level-left">
                        <span>added {{bookmark.created_on}} by
                            <div v-if="this.$root.store.isAuthenticated && bookmark.user.id !== this.$root.user.id" @mouseover="showFollowCheckbox = true" @mouseleave="showFollowCheckbox = false" class="is-inline">
                                <b-tooltip v-if="showFollowCheckbox" label="Follow ?" position="is-bottom">
                                    <label class="checkbox has-text-warning">
                                        {{bookmark.user.username}}<input type="checkbox" @change="followUser($event.target.checked)" :checked="isFollowing">
                                    </label>
                                </b-tooltip>
                                <b-tooltip v-else label="Unfollow ?" position="is-bottom">
                                    <label class="has-text-warning">{{bookmark.user.username}}</label>
                                </b-tooltip>
                            </div>
                            <div v-else class="is-inline">
                                <label class="has-text-warning">{{bookmark.user.username}}</label>
                            </div>
                        </span>
                    </div>

                    <div class="leve-right">
                        <div class="tags">
                            <span v-for="tag in bookmark.tags" :key="tag.name" v-text="'#' + tag.name" class="tag"></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <BookmarkForm v-if="showBookmarkForm" @close="showBookmarkForm = false"
                    :bookmark="bookmark"
                    :updateMode="true">
            <template slot="header">Edit bookmark</template>
            <template slot="footer">Update</template>
        </BookmarkForm>
    </div>
</template>

<script>
import {getVote, postVote, putVote, deleteVote, postFavourite, deleteFavourite, postSubscription, deleteSubscription, deleteBookmark} from '../api.js'
import BookmarkForm from './BookmarkForm.vue'

export default {
    name: "Bookmark",
    props: ["bookmark"],
    components: {
        BookmarkForm
    },
    data() {
        return {
            voteDirection: null,
            voteId: null,
            favourite: null,
            isFollowing: false,
            showFollowCheckbox: false,
            showBookmarkForm: false
        }
    },
    methods: {
        deleteBookmark() {
            this.$buefy.dialog.confirm({
                    title: 'Deleting bookmark',
                    message: 'Are you sure you want to <b>delete</b> the bookmark ?',
                    confirmText: 'Delete bookmark',
                    type: 'is-danger',
                    hasIcon: true,
                    onConfirm: () => {
                        deleteBookmark(this.bookmark.id)
                            .then(data => {
                                if (data.message || data.status) {
                                    this.$root.$emit('notification', data.message || data.status);
                                } else {
                                    this.$destroy();
                                    this.$el.parentNode.removeChild(this.$el);
                                    this.$buefy.toast.open('Bookmark deleted!');
                                }
                            })
                    }
                })
        },
        upVote() {
            if (this.voteDirection == null) {
                postVote(this.bookmark.id, 1)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            getVote(data.location.split('/').pop()).then(data => {
                                this.$root.user.votes.push(data);
                                this.voteDirection = data.direction;
                                this.voteId = data.id;
                                this.bookmark.rating += 1;
                            });
                        }
                    })
            } else if (this.voteDirection === true) {
                deleteVote(this.voteId)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            for (let i=0; i < this.$root.user.votes.length; i++) {
                                if (this.$root.user.votes[i].id === this.voteId) {
                                    this.$root.user.votes.splice(i, 1);
                                    break;
                                }
                            }
                            this.voteDirection = null;
                            this.voteId = null;
                            this.bookmark.rating -= 1;
                        }
                    })
            } else {
                putVote(this.voteId, 1)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            for (let i=0; i < this.$root.user.votes.length; i++) {
                                if (this.$root.user.votes[i].id === this.voteId) {
                                    this.$root.user.votes[i].direction = true;
                                    break;
                                }
                            }
                            this.voteDirection = true;
                            this.bookmark.rating += 2;
                        }
                    })
            }
        },
        downVote() {
            if (this.voteDirection == null) {
                postVote(this.bookmark.id, -1)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            getVote(data.location.split('/').pop()).then(data => {
                                this.$root.user.votes.push(data);
                                this.voteDirection = data.direction;
                                this.voteId = data.id;
                                this.bookmark.rating -= 1;
                                })
                        }
                    })
            } else if (this.voteDirection === false) {
                deleteVote(this.voteId)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            for (let i=0; i < this.$root.user.votes.length; i++) {
                                if (this.$root.user.votes[i].id === this.voteId) {
                                    this.$root.user.votes.splice(i, 1);
                                    break;
                                }
                            }
                            this.voteDirection = null;
                            this.voteId = null;
                            this.bookmark.rating += 1;
                        }
                    })
            } else {
                putVote(this.voteId, -1)
                    .then(data => {
                        if (data.message || data.status) {
                            this.$root.$emit('notification', data.message || data.status);
                        } else {
                            for (let i=0; i < this.$root.user.votes.length; i++) {
                                if (this.$root.user.votes[i].id === this.voteId) {
                                    this.$root.user.votes[i].direction = false;
                                    break;
                                }
                            }
                            this.voteDirection = false;
                            this.bookmark.rating -= 2;
                        }
                    })
            }
        },
        favouriteBookmark() {
            if (this.favourite != null) {
                deleteFavourite(this.favourite.bookmark_id);
                for (let i=0; i < this.$root.user.favourites.length; i++) {
                    if (this.$root.user.favourites[i].bookmark_id === this.bookmark.id) {
                        this.$root.user.favourites.splice(i, 1);
                        break
                    }
                }
                this.favourite = null;
                return;
            }
            postFavourite(this.bookmark.id).then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                    return;
                }
                this.favourite = {'bookmark_id': this.bookmark.id};
                this.$root.user.favourites.push(this.favourite);
            }) 
        },
        followUser(checked) {
            if (checked) {
                postSubscription(this.bookmark.user.id).then(data => {
                    if (data.message || data.status) {
                        this.$root.$emit('notification', data.message || data.status);
                        return;
                    }
                    this.$root.user.subscribed.push(this.bookmark.user);
                    this.isFollowing = true;
                })
            } else {
                deleteSubscription(this.bookmark.user.id).then(data => {
                    if (data.message || data.status) {
                        this.$root.$emit('notification', data.message || data.status);
                        return;
                    }
                })
                this.isFollowing = false;
                // remove user from subscribed
                for (let i=0; i<this.$root.user.subscribed.length; i++) {
                    if (this.$root.user.subscribed[i].id === this.bookmark.user.id) {
                        this.$root.user.subscribed.splice(i, 1);
                        break;
                    }
                }
            }
            // FIXME check if in api.js can throw the notification instead of handling all over the place

        },
        setFollowing() {
            this.isFollowing = false;
            for (let user of this.$root.user.subscribed) {
                if (user.id === this.bookmark.user.id) {
                    this.isFollowing = true;
                    return;
                }
            }
        }
    },
    mounted() {
      this.$root.$on('authenticated', () => {
        this.setFollowing();
        for (let f of this.$root.user.favourites) {
            if (f.bookmark_id === this.bookmark.id) {
                this.favourite = f;
                break;
            }
        }
        for (let v of this.$root.user.votes) {
            if (v.bookmark_id === this.bookmark.id) {
                this.voteDirection = v.direction;
                this.voteId = v.id;
                break;
            }
        }
      });
        this.$root.$on('unauthenticated', () => {
            this.favourite = null;
            this.voteDirection = null;
            this.voteId = null;
            this.isFollowing = false;
        })
    },
}
</script>
