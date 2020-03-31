<template>
      <div class="board_header" :style="{backgroundColor: color,  color: text_color}">
        <div class="title">{{board.name}}</div>
        <div class="description">{{board.description}}</div>
      </div>
</template>

<style lang="scss" scoped>
.board_header {
  background-color: var(--orange);
  color: white;
  padding: 1em;
  padding-left: 6vw;
  padding-right: 6vw;
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
import { rgb_to_hsl } from '~/assets/rgb_to_hsl';

export default {
  props: ["board"],
  computed: {
    color() {
      return this.board["color"] || "#ffffff";
    },
    text_color() {
      let l = rgb_to_hsl(this.color)[2];
      if (l < 0.5) {
        return "#ffffff";
      }
      return "#000000";
    },
  }
}
</script>