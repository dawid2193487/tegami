<template>
    <div class="topbar" :style="{backgroundColor: color,  color: text_color}" :class="{'shade': shade}">
        <nuxt-link class="home interact link button" to="/">
            <div>
                <font-awesome-icon icon="home"/>
            </div>
        </nuxt-link>
        <BoardButton v-for="subboard in boards" :key="subboard.pk" :pk="subboard.pk" :open_pk="board.pk" />
    </div>
</template>

<style lang="scss" scoped>
.topbar {
    position: sticky;
    top: 0;
    display: flex;
    padding: 5px;
    z-index: 15;
    transition: box-shadow 0.3s ease-in-out;
    padding-left: 6vw;
    padding-right: 6vw;
}

.home {
    margin-right: 7px;
}

.shade {
    box-shadow: 0px 0px 6px var(--shadow);
}
</style>

<script>
import { mapActions } from 'vuex';
import { rgb_to_hsl } from '~/assets/rgb_to_hsl';
import BoardButton from '~/components/BoardButton';

export default {
    props: ["board", "shade"],
    components: { BoardButton }, 
    data: () => { return {
        request_nonce: null,
    }},
    computed: {
        boards() {
            return this.$store.state.boards
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
    },
    methods: {
        ...mapActions(['board_list']),
        /*get_text_color(rgbcode) {
            let l = rgb_to_hsl(rgbcode)[2];
            if (l < 0.5) {
                return "#ffffff";
            }
            return "#000000";
        }*/
    },
    mounted() {
        this.board_list().then((nonce) => {
            this.request_nonce = nonce;
        });
    }
}
</script>