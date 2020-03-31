<template>
  <div class="expander" v-if="open">
    <div class="close" @click="close">
      <div class="icon">
        <font-awesome-icon icon="times"/>
      </div>
    </div>
    <img class="image" v-if="image" :src="fullpath" alt=""/>
    <video class="image" v-if="video" :src="fullpath" autoplay controls/>
  </div>
</template>

<style lang="scss" scoped>
.expander {
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10;
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
}

.close {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
}

.icon {
  z-index: 10;
  position: absolute;
  width: 50px;
  height: 50px;
  background-color: black;
  top: 0;
  right: 0;
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 30px;
}

.image {
  max-height: 100vh;
  max-width: 100vw;
  z-index: 1;
  margin: 10px;
}
</style>

<script>
import { mapMutations } from 'vuex';

export default {
  computed: {
    fullpath() {
      const path = this.$store.state.preview;
      return `http://localhost:8000${path}`;
    },
    open() {
      return this.$store.state.preview != "";
    },
    extension() {
      const split = this.fullpath.split(".")
      if (split.length>1) {
        return split[split.length-1].toLowerCase()
      } else {
        return ""
      }
    },
    image() {
      return {
        "jpg": 1,
        "jpeg": 1,
        "png": 1,
        "gif": 1,
      }[this.extension];
    },
    video() {
      return {
        "mp4": 1,
        "webm": 1,
      }[this.extension];
    },
  },
  methods: {
    ...mapMutations(["set_preview"]),
    close() {
      this.set_preview("");
    }
  }
}
</script>