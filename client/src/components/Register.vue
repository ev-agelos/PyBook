<template>
    <div class="modal is-active">
        <div @click="$emit('close')" class="modal-background"></div>
        <div class="modal-card">
            <div class="box">
                <form @submit="submitForm">
                    <div class="field">
                        <label class="label">Username</label>
                        <div class="control has-icons-left has-icons-right">
                            <input v-model="username" class="input" type="text" value="bulma">
                            <span class="icon is-small is-left">
                                <i class="mdi mdi-account"></i>
                            </span>
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Email</label>
                        <div class="control has-icons-left has-icons-right">
                            <input v-model="email" class="input" type="email" value="hello@">
                            <span class="icon is-small is-left">
                                <i class="mdi mdi-email"></i>
                            </span>
                        </div>
                    </div>

                    <div class="field">
                        <label class="label">Password</label>
                        <p class="control has-icons-left">
                            <input v-model="password" class="input" type="password">
                            <span class="icon is-small is-left">
                                <i class="mdi mdi-lock"></i>
                            </span>
                        </p>
                    </div>

                    <div class="field">
                        <label class="label">Confirm password</label>
                        <p class="control has-icons-left">
                            <input v-model="confirmPassword" class="input" type="password">
                            <span class="icon is-small is-left">
                                <i class="mdi mdi-lock"></i>
                            </span>
                        </p>
                    </div>

                    <div class="field is-grouped is-grouped-centered">
                        <div class="g-recaptcha" :data-sitekey="recaptchaSiteKey"></div>
                    </div>

                    <div class="field is-grouped is-grouped-right">
                        <div class="control">
                            <button @click="$emit('close')" class="button is-link is-light">Cancel</button>
                        </div>
                        <div class="control">
                            <button class="button is-link">Submit</button>
                        </div>
                    </div>
                </form>
            </div>
        </div>

        <button @click="$emit('close')" class="modal-close is-large" aria-label="close"></button>

        <script type="application/javascript" src="https://www.google.com/recaptcha/api.js" async defer></script>
    </div> 
</template>

<script>
import {register} from '../api.js'

export default {
    name: 'RegisterForm',
    data() {
        return {
            username: '',
            email: '',
            password: '',
            confirmPassword: '',
            recaptchaSiteKey: '6LeYXwkUAAAAAAGvRUbL8kl-Wxnp2dm7wZoK3pZE'
        }
    },
    methods: {
        submitForm(event) {
            event.preventDefault()
            const payload = {
                username: this.username,
                email: this.email,
                password: this.password,
                confirmPassword: this.confirmPassword,
                recaptcha: event.target['g-recaptcha-response'].value
            };
            register(payload)
                .then(result => {
                    // TODO handle errors: show them next to each field
                    if (result.ok) {
                        this.$emit('close');
                        this.$root.$emit('notification', result.data.message);
                    } else if (result.data.errors) {
                        this.$root.$emit('notification', JSON.stringify(result.data.errors.json));
                    } else {
                        this.$root.$emit('notification', result.data.message);
                    }
                })
        }
    }
}
</script>
