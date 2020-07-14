<template>
    <form>
        <div class="field">
            <label class="label">New password</label>
            <div class="control">
                <input v-model="password" class="input" type="password">
            </div>
        </div>
        <div class="field">
            <label class="label">Confirm password</label>
            <div class="control">
                <input v-model="confirmPassword" class="input" type="password">
            </div>
        </div>
        <button @click="resetOldPassword" class="button is-pulled-right is-primary">Change password</button>
    </form>
</template>

<script>
import {resetPassword} from '../api.js'

export default {
    name: 'ResetPassword',
    data() {
        return {
            password: '',
            confirmPassword: '',
            token: ''
        }
    },
    methods: {
        resetOldPassword() {
            const payload = {'newPassword': this.newPassword, 'confirmNewPassword': this.confirmNewPassword, 'token': this.token};
            resetPassword(payload).then(data => {
                if (data && (data.message || data.status)) {
                    this.$root.$emit('notification', data.message || data.status);
                } else {
                    this.$buefy.notification.open({message: 'Password succesfully changed. You can now login with your new password.'});
                }
            })
        }
    },
    created() {
        const params = new URLSearchParams(window.location.search);
        this.token = params.get('token');
    }
}
</script>
