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

  --shadow: rgba(0, 0, 0, 0.50);
  --half-shadow: rgba(0, 0, 0, 0.25);
}

body {
  margin: 0;
}

a {
  text-decoration: unset;
  color: unset;
}

.link {
  color: unset;
  text-decoration: underline;
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