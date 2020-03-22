<template>
    <span>
      <span v-if="pk">{{profile.display_name}}</span>
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
  data: () => { return {
    request_nonce: null,
  }},
  methods: {
    ...mapActions(['profile_detail'])
  },
  computed: {
    profile() {
      return this.$store.state.profiles[this.pk] || {};
    },
    ready() {
      if (this.request_nonce == null) {
        return false;
      }
      return this.$store.state.requests[this.request_nonce] == "complete" || this.pk == null;
    },
    loading() {
      if (this.request_nonce == null) {
        return true;
      }
      return this.$store.state.requests[this.request_nonce] == "pending";
    }
  },
  mounted () {
    if (this.pk == null) {
      return;
    }

    this.profile_detail(this.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>