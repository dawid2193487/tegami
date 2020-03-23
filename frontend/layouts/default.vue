<template>
  <div>
    <nuxt v-if="connection_guard" />
    <div class="fail" v-else-if="failed">Could not connect. Reload the page to try again.</div>
    <div v-else>Connecting...</div>
  </div>
</template>

<style type="scss">

@import url('~/assets/global_style.scss');
html {
  font-family: 'Arial', 'Source Sans Pro', -apple-system, BlinkMacSystemFont, 'Segoe UI',
    Roboto, 'Helvetica Neue', Arial, sans-serif;

  --shadow: rgba(0, 0, 0, 0.50);
  --half-shadow: rgba(0, 0, 0, 0.25);
  --red: #df2935;
  --yellow: #e89005;
  --orange: #ec7505;
  --pumpkin: #f42b03;
  --green: #63ff75;
  --background: #ffffff;
  --load: #f0f0f0;
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

.fail {
  margin: 2em;
  padding: 1em;
  font-size: 200%;
  border: 1px solid red;
  border-radius: 5px;
}
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