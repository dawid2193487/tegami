<template>
  <div>
    <nuxt v-if="connection_guard" />
    <div class="fail" v-else-if="failed">Could not connect. Reload the page to try again.</div>
    <div v-else>Connecting...</div>
  </div>
</template>

<style type="scss">

@import url('~/assets/global_style.scss');

</style>

<script>
export default {
  computed: {
    connection_guard() {
      return this.$store.state.socket.connection_guard
    },
    failed() {
      return this.$store.state.socket.failed
    },
  }
}
</script>