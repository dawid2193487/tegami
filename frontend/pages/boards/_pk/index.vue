<template>
  <div class="container">
    <BoardHeader :board="board"/>
    <div class="threads" v-if="ready">
      <Thread class="thread_container" v-for="pk in board.threads" :pk="pk" :key="pk"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.threads {
  display: flex;
  flex-wrap: wrap;
}

.thread_container {
  flex-basis: 100%;
  margin: 10px;
}
</style>

<script>
import { mapActions } from 'vuex';
import BoardHeader from "~/components/BoardHeader";
import Thread from "~/components/Thread";

export default {
  components: { BoardHeader, Thread },
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
