<template>
    <span>
      <span v-if="$fetchState.pending">...</span>
      <span v-else-if="pk">{{profile.display_name}}</span>
      <span v-else>Anonymous</span>
    </span>
</template>

<style lang="scss" scoped>
.board_tile {
  background-color: rgb(196, 67, 196);
  padding: 1em;
  box-shadow: 0px 1px 1px var(--shadow);
  transition: box-shadow 0.05s ease-in-out;
}

.board_tile:hover {
  box-shadow: 0px 3px 1px var(--half-shadow);
}

.title {
  font-size: 150%;
  a {
    color: black;
    font-weight: bold;
  }
}
.description {
  margin-top: 0.4em;
}
</style>

<script>
import { mapActions } from 'vuex';

export default {
  props: ["pk"],
  methods: {
    ...mapActions(['profile_detail'])
  },
  computed: {
    profile() {
      return this.$store.state.profiles[this.pk] || {};
    },
  },
  async fetch() {
    await this.$store.dispatch('profile_detail', this.pk);
  },
  /*mounted () {
    if (this.pk == null) {
      console.log("pk null")
      return;
    }
    console.log("sending request");
    this.profile_detail(this.pk).then((nonce) => {
      console.log("profile detail request sent!")
      this.request_nonce = nonce;
    });
  }*/
}
</script>