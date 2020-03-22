<template>
      <div class="board_header">
        <div class="title">{{board.name}}</div>
        <div class="description">{{board.description}}</div>
      </div>
</template>

<style lang="scss" scoped>
.board_header {
  background-color: rgb(196, 67, 196);
  padding: 1em;
  box-shadow: 0px 1px 1px var(--shadow);
  transition: box-shadow 0.05s ease-in-out;
}

.board_tile:hover {
  box-shadow: 0px 3px 1px var(--half-shadow);
}

.title {
  font-size: 200%;
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
  props: ["board"],
}
</script>