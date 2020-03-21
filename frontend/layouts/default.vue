<template>
  <div>
    <nuxt v-if="connection_guard" />
    <div v-else>Connecting...</div>
  </div>
</template>

<style>
html {
  font-family: 'Arial', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>

<script>
export default {
  computed: {
    connection_guard() {
      return this.$store.state.socket.connection_guard
    }
  }
}
</script>