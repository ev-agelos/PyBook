<template>
    <header>
        <nav class="navbar has-background-white-ter" role="navigation" aria-label="main navigation">
            <div class="navbar-brand">
                <a role="button" class="navbar-burger burger" aria-label="menu" aria-expanded="false"
                    data-target="navbarBasicExample">
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                    <span aria-hidden="true"></span>
                </a>
            </div>

            <div class="navbar-menu">
                <div class="navbar-start">
                    <a class="navbar-item" href="https://github.com/ev-agelos/pybook" target="_blank" rel="noopener noreferrer"><i class="mdi mdi-github mdi-24px" aria-hidden="true"></i></a>
                    <a class="navbar-item" href="/api/v1/documentation" target="_blank" rel="noopener noreferrer">API</a>
                </div>
            </div>

            <div class="navbar-end">
                <div class="navbar-item">
                    <div class="buttons">
                        <div v-if="this.$root.store.access_token">
                            <a class="button is-primary" @click="showBookmarkForm = true">
                                <span class="icon"><i class="mdi mdi-plus"></i></span>
                                <span>New</span>
                            </a>
                            <b-dropdown position="is-bottom-left" append-to-body aria-role="menu">
                                <a class="navbar-item" slot="trigger" role="button">
                                    <span>Menu</span>
                                    <b-icon icon="menu-down"></b-icon>
                                </a>

                                <b-dropdown-item custom aria-role="menuitem">
                                    Logged as <b>{{this.$root.user.username}}</b>
                                </b-dropdown-item>
                                <hr class="dropdown-divider">
                                <b-dropdown-item @click="showProfileForm = true" value="profile" aria-role="menuitem">
                                    <b-icon icon="account-circle"></b-icon>
                                    Profile
                                </b-dropdown-item>
                                <hr class="dropdown-divider" aria-role="menuitem">
                                <b-dropdown-item @click="logoutUser" value="logout" aria-role="menuitem">
                                    <b-icon icon="logout"></b-icon>
                                    Logout
                                </b-dropdown-item>
                            </b-dropdown>
                        </div>
                        <div v-else class="navbar-buttons">
                            <a @click="showRegisterForm = true" class="button is-primary"><strong>Sign up</strong></a>
                            <b-dropdown position="is-bottom-left" append-to-body aria-role="menu" trap-focus>
                                <a
                                    class="navbar-item"
                                    slot="trigger"
                                    role="button">
                                    <span>Login</span>
                                    <b-icon icon="menu-down"></b-icon>
                                </a>

                                <b-dropdown-item
                                    aria-role="menu-item"
                                    :focusable="false"
                                    custom
                                    paddingless>
                                    <div class="modal-card" style="width:300px;">
                                        <form action="">
                                            <section class="modal-card-body">
                                                <b-field label="Email">
                                                    <b-input
                                                        v-model="email"
                                                        type="email"
                                                        placeholder="Your email"
                                                        required>
                                                    </b-input>
                                                </b-field>

                                                <b-field label="Password">
                                                    <b-input
                                                        v-model="password"
                                                        type="password"
                                                        password-reveal
                                                        placeholder="Your password"
                                                        required>
                                                    </b-input>
                                                </b-field>

                                            </section>
                                            <footer class="modal-card-foot">
                                                <button @click="login" :class="{'is-loading':onLogin}" class="button is-primary">Login</button>
                                            </footer>
                                        </form>
                                            
                                        <div class="field is-grouped is-grouped-centered">
                                            <p class="control"><a @click="forgotPassword" href="#">Forgot my password</a></p>
                                        </div>

                                    </div>
                                </b-dropdown-item>
                            </b-dropdown>
                        </div>
                    </div>
                </div>
            </div>
        </nav>

        <RegisterForm v-if="showRegisterForm" @close="showRegisterForm = false" />
        <Profile v-if="showProfileForm" @close="showProfileForm = false" />
        <BookmarkForm v-if="showBookmarkForm" @close="showBookmarkForm = false">
            <template slot="header">Add new bookmark</template>
            <template slot="footer">Add</template>
        </BookmarkForm>

    </header>
</template>

<script>
import {getToken, getAuthUser, logout, requestPasswordReset} from '../api.js'
import Profile from './Profile.vue'
import BookmarkForm from './BookmarkForm.vue'
import RegisterForm from './Register.vue'

export default {
  name: 'Header',
  components: {
    Profile,
    BookmarkForm,
    RegisterForm
  },
  data() {
    return {
        email: '',
        password: '',
        showBookmarkForm: false,
        showProfileForm: false,
        showRegisterForm: false,
        onLogin: false
    }
  },
  methods: {
    login(event) {
        event.preventDefault();
        this.onLogin = true;
        getToken(this.email, this.password).then(data => {
            if (data.message || data.status) {
                this.$root.$emit('unauthenticated');
                this.$root.$emit('notification', data.message || data.status);
                this.onLogin = false;
                return;
            }
            this.$root.store.access_token = data.token;
            getAuthUser().then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                    this.onLogin = false;
                    return;
                }
                this.$root.user = data;
                this.$root.$emit('authenticated');
                this.onLogin = false;
            })
        })
    },
    logoutUser() {
        logout().then(response => {
            this.$root.$emit('unauthenticated');
            this.$root.store.access_token = '';
            this.$root.user = Object();
            if (!response.ok) {
                return response.json()
            }
        }).then(data => {
            if (data && (data.message || data.status)) {
                this.$root.$emit('notification', data.message || data.status);
            }
        })
    },
    forgotPassword() {
        this.$children[0].toggle()
        this.$buefy.dialog.prompt({
            message: "What is your email address?",
            trapFocus: true,
            onConfirm: (value) => {
                requestPasswordReset(value);
                this.$buefy.notification.open({message: `An email was sent to ${value}, please follow the instructions to reset your password.`, indefinite: true, type: 'is-white', hasIcon: true });
            }
        })
    }
  }
}
</script>
