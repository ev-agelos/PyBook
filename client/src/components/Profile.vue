<template>
    <div class="modal is-active is-half">
        <div class="modal-background" @click="$emit('close')"></div>
        <div class="modal-card">
            <div class="box">
                <tabs>
                    <tab name="Profile" :selected="true">
                        <div class="field">
                            <label class="label">Username</label>
                            <div class="control">
                                <input v-model="username" class="input" type="text">
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">Email</label>
                            <div class="control">
                                <input v-model="email" class="input" type="email">
                            </div>
                        </div>
                        <button @click="updateProfile" class="button is-pulled-right is-primary">Update</button>
                    </tab>

                    <tab name="Password">
                        <div class="field">
                            <label class="label">Current password</label>
                            <div class="control">
                                <input v-model="currentPassword" class="input" type="password">
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">New password</label>
                            <div class="control">
                                <input v-model="newPassword" class="input" type="password">
                            </div>
                        </div>
                        <div class="field">
                            <label class="label">Confirm password</label>
                            <div class="control">
                                <input v-model="confirmPassword" class="input" type="password">
                            </div>
                        </div>
                        <button @click="updatePassword" class="button is-pulled-right is-primary">Change password</button>
                    </tab>
                </tabs>
            </div>
        </div>
    </div>
</template>


<script>
import {putUser} from '../api.js'
import tabs from './tabs.vue'
import tab from './tab.vue'

export default {
  name: 'Profile',
  components: {
    tabs,
    tab
  },
  data() {
      return {
        username: '',
        email: '',
        currentPassword: '',
        newPassword: '',
        confirmPassword: ''
      }
  },
  created(){
      this.username = this.$root.user.username;
      this.email = this.$root.user.email;
  },
  methods: {
    updateProfile() {
        const payload = {'username': this.username, 'email': this.email};
        putUser(this.$root.user.id, payload)
            .then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    if (this.username !== this.$root.user.username) {
                        this.$root.user.username = this.username;
                        this.$buefy.toast.open('Username updated');
                    }
                    if (this.email !== this.$root.user.email) {
                        this.$buefy.toast.open(`A verification email has been sent to ${this.email}`);
                    }
                }
            })
    },
    updatePassword() {
        const payload = {'currentPassword': this.currentPassword, 'newPassword': this.newPassword, 'confirmPassword': this.confirmPassword};
        putUser(this.$root.user.id, payload)
            .then(data => {
                if (data.message || data.status) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    this.$buefy.toast.open('Password updated');
                }
            })
    }
  }
}
</script>
