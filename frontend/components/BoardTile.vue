<template>
    <nuxt-link :to="{name: 'boards-pk', params: { pk: pk }}">
      <div class="box interact yellow board_tile">
        <div class="title link">{{board.name}}</div>
        <div class="description">{{board.description}}</div>
      </div>
    </nuxt-link>
</template>

<style lang="scss" scoped>
.board_tile {
  padding: 1em;
  color: white;
}

.title {
  font-size: 150%;
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
    ...mapActions(['board_detail'])
  },
  computed: {
    board() {
      return this.$store.state.boards[this.pk] || {};
    },
    ready() {
      if (this.request_nonce == null) {
        return false;
      }
      return this.$store.state.requests[this.request_nonce] == "complete";
    },
    loading() {
      if (this.request_nonce == null) {
        return true;
      }
      return this.$store.state.requests[this.request_nonce] == "pending";
    }
  },
  mounted () {
    this.board_detail(this.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>