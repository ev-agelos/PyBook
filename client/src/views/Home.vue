<template>
    <div>
        <div class="is-pulled-left">
            <SidePanel />
        </div>

        <div class="">
            <Header />
        </div>

        <Bookmarks />
    </div>
</template>

<script>
import Header from '../components/Header.vue'
import SidePanel from '../components/SidePanel.vue'
import Bookmarks from '../components/Bookmarks.vue'

export default {
  name: 'Home',
  components: {
    Header,
    SidePanel,
    Bookmarks
  },
  methods: {
    dangerNotification(msg) {
        this.$buefy.notification.open({
            message: msg,
            indefinite: true,
            type: 'is-white',
            hasIcon: true
        })
    }
  },
  mounted() {
    this.$root.$on('notification', (msg) => {
        this.dangerNotification(msg);
    })
  }
}
</script>
