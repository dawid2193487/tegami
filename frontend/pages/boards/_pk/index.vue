<template>
  <div class="container">
    <BoardHeader :board="board"/>
    <div class="threads" v-if="ready">
      <Thread class="thread_container" v-for="pk in threads" :pk="pk" :key="pk"/>
      <div v-if="display < this.board.thread_set.length" @click="display+=10" class="thread_container load box orange interact link">Load 10 more...</div>
    </div>
    <Composer :uploads="true" @send="new_thread" class="thread_container composer" text="Post a thread"/>
  </div>
</template>

<style lang="scss" scoped>
.threads {
  display: flex;
  flex-wrap: wrap;
  z-index: 1;
}

.composer {
  position: sticky;
  bottom: 0px;
  z-index: 2;
}

.thread_container {
  flex-basis: 100%;
  margin: 10px;
}

.load {
  padding-left: 10px;
  padding-top: 10px;
  padding-bottom: 10px;
  max-width: 800px;
}
</style>

<script>
import { mapActions } from 'vuex';
import BoardHeader from "~/components/BoardHeader";
import Thread from "~/components/Thread";
import Composer from "~/components/Composer";

export default {
  components: { BoardHeader, Thread, Composer },
  data: () => { return {
    request_nonce: null,
    subscription_nonce: null,
    display: 10,
  }},
  computed: {
    pk() {
      return this.$route.params.pk;
    },
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
    },
    threads() {
      return this.board.thread_set.slice().reverse().slice(0, this.display);
    }
  },
  methods: {
    ...mapActions(['board_detail', 'watch_board', 'post_thread']),
    new_thread({message, upload_tokens}) {
      this.post_thread({pk: this.pk, message: message, upload_tokens})
    }
  },
  mounted () {
    this.board_detail(this.$route.params.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
    this.watch_board(this.$route.params.pk).then((nonce) => {
      this.subscription_nonce = nonce;
    });
  }
}
</script>
