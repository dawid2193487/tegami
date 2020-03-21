<template>
  <div class="container">
    <div class="board_detail">
      <h1>{{ board.name }}</h1>
      <div v-for="thread in board.threads">
        {{thread.message}}
      </div>
    </div>
  </div>
</template>

<script>
import { mapActions } from 'vuex';

export default {
  computed: {
    board() {
      return this.$store.state.boards[this.$route.params.pk] || {};
    }
  },
  methods: {
    ...mapActions(['thread_list'])
  },
  mounted () {
    this.thread_list(this.$route.params.pk);
  }
}
</script>
