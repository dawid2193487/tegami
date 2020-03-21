<template>
  <div class="container">
    <div v-if="ready" class="board_list">
      <ul>
        <li v-for="(board, pk) in boards" v-bind:key="pk">
          <nuxt-link :to="{name: 'boards-pk', params: { pk: pk }}">{{ board.name }}</nuxt-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  data: () => { return {
    request_nonce: null,
  }},
  computed: {
    boards() {
      console.log(this.$store.state.boards);
      return this.$store.state.boards
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
  methods: {
    ...mapActions(['board_list'])
  },
  mounted() {
    this.board_list().then((nonce) => {
      this.request_nonce = nonce;
    })
  }
}
</script>

