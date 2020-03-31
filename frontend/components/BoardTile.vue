<template>
    <nuxt-link :to="{name: 'boards-pk', params: { pk: pk }}">
      <div class="box interact board_tile"
        :style="{backgroundColor: color,  color: text_color}">
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
import { rgb_to_hsl } from '~/assets/rgb_to_hsl';

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