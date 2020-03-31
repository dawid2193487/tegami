<template>
  <div class="container">
    <div class="apptitle">Tegami</div>
    <h1 class="title"> Boards </h1>
    <div v-if="ready" class="board_list">
        <BoardTile class="board_listing" :pk="pk" v-for="(board, pk) in boards" v-bind:key="pk"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.container {
  margin-top: 2em;
  margin-left: 10vw;
  margin-right: 10vw;
}

.apptitle {
  opacity: 0.8;
}

.title {
  margin-bottom: 0.5em;
}

.board_list {
  display: flex;
  max-width: 500px;
  flex-wrap: wrap;
}

.board_listing {
  flex-basis: 100%;
  margin-bottom: 10px;
}
</style>

<script>
import { mapActions } from 'vuex';
import BoardTile from '~/components/BoardTile.vue';

export default {
  components: {BoardTile},
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
    ...mapActions(['board_list']),
  },
  mounted() {
    this.board_list().then((nonce) => {
      this.request_nonce = nonce;
    })
  }
}
</script>

