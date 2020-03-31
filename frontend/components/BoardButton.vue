<template>
    <nuxt-link class="board" :to="{name: 'boards-pk', params: { pk: pk }}">
        <div class="interact link button" 
        :class="{'active': open}"
        :style="{backgroundColor: color, color: text_color}">
        {{board.name}}
    </div>
    </nuxt-link>
</template>

<style lang="scss" scoped>
.board {
    margin-right: 7px;
}
.active {
    border-radius: 3px;
}
</style>

<script>
import { rgb_to_hsl } from '~/assets/rgb_to_hsl';

export default {
    props: ["pk", "open_pk"],
    computed: {
        board() {
            return this.$store.state.boards[this.pk] || {};
        },
        open() {
            return this.open_pk == this.pk;
        },
        color() {
            if (this.open) {
                return "#ffffff";
            }
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