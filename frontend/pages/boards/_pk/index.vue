<template>
  <div class="container">
    <div class="board_detail" v-if="ready">
      <h1>{{ board.name }}</h1>
      <div v-for="(thread, pk) in board.threads" :key="pk">
        {{thread.message}}
      </div>
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
    board() {
      return this.$store.state.boards[this.$route.params.pk] || {};
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
    ...mapActions(['thread_list'])
  },
  mounted () {
    this.thread_list(this.$route.params.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>
