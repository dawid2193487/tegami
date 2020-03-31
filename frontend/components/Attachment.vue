<template>
    <div 
        class="attachment box interact" 
        :class="{'noimg': data.thumb == null}"
        @click="open">
        <img v-if="data.thumb" :src="`http://localhost:8000${data.thumb}`"/>
        <div v-else class="placeholder"><font-awesome-icon icon="file"/></div>
        <div class="filename">{{data.name}}</div>
    </div>
</template>

<style lang="scss">
.attachment {
    // width: 200px;
    height: 150px;
    flex-basis: 20%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    //margin-right: 10px;
    //border-radius: 10px;
    padding: 0;
    position: relative;
    .placeholder {
        font-size: 400%;
    }
    &.noimg {
        .filename {
            opacity: 1;
        }
    }

    &:hover {
        .filename {
            opacity: 0.7;
            background-image: linear-gradient(to top, var(--background) 60%, transparent 100%);
        }
    }

    .filename {
        padding-top: 10%;
        display: flex;
        justify-content: center;
        overflow-wrap: anywhere;
        position: absolute;
        bottom: 0;
        opacity: 0;
        width: 100%;
        transition: opacity 0.2s ease-in-out;
    }


    a {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    a > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

</style>

<script>
import { mapMutations } from 'vuex';

export default {
    props: ["data"],
    computed: {
        extension() {
            const split = this.data.path.split(".")
            if (split.length>1) {
                return split[split.length-1]
            } else {
                return ""
            }
        },
        fullpath() {
            return `http://localhost:8000${this.data.path}`;
        },
    },
    methods: {
        ...mapMutations(["set_preview"]), 
        previewable(ext) {
            return {
                "jpg": 1,
                "jpeg": 1,
                "png": 1,
                "gif": 1,
                "webm": 1,
                "mp4": 1,
            }[ext.toLowerCase()];
        },
        open() {
            if (this.previewable(this.extension)){
                this.set_preview(this.data.path);
            } else {
                window.open(this.fullpath, '_blank');
            }
        }
    }
}
</script>