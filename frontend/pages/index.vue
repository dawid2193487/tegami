<template>
  <div class="container">
    <div class="board_list">
      <ul>
        <li v-for="(board, pk) in boards" v-bind:key="pk">
          <nuxt-link :to="{name: 'boards-pk', params: { pk: pk }}">{{ board.name }}</nuxt-link>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>

export default {
  computed: {
    boards() {
      console.log(this.$store.state.boards);
      return this.$store.state.boards
    }
  }
}
</script>

