<template>
  <div class="container" @open_preview="open_preview">
    <FastNavigation :board="board" :shade="!header_visible"/>
    <FileExpander ref="expander"/>
    <div class="content">
      <BoardHeader :board="board" v-observe-visibility="set_header_visibility"/>
      <div class="threads">
        <div 
          class="thread_container stale box interact link green" 
          v-if="stale && !header_visible" 
          @click="scroll_to_top">
          New messages.
          </div>
        <transition-group name="thread-list" tag="div" class="transition">
          <Thread class="thread_container" v-for="pk in threads" :pk="pk" :key="pk"/>
        </transition-group>
        <div 
          v-observe-visibility="load_more"
          v-if="display < displayed_threads.length" 
          @click="display+=10" 
          class="thread_container load box orange interact link">
          Load 10 more...
        </div>
      </div>
      <Composer :uploads="true" @send="new_thread" class="composer" text="Post a thread"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.stale {
  position: sticky;
  top: 50px;
  z-index: 4;
}

.threads {
  display: flex;
  flex-wrap: wrap;
  z-index: 1;
}

.composer {
  position: sticky;
  bottom: 0px;
  z-index: 2;
  margin-left: calc(5vw + 10px);
  margin-right: calc(5vw + 10px);
}

.thread_container {
  flex-basis: 100%;
  margin: 10px;
}

.load {
  padding-left: 10px;
  padding-top: 10px;
  padding-bottom: 10px;
  max-width: 800px;
}

.transition {
  flex-basis: 100%;
}

.thread-list-enter {
  opacity: 0;
}

.thread-list-enter-active, .thread-list-leave-active {
  transition: all 0.5s;
}

.threads {
  margin-left: 5vw;
  margin-right: 5vw;
}
</style>

<script>
import { mapActions } from 'vuex';
import BoardHeader from "~/components/BoardHeader";
import Thread from "~/components/Thread";
import Composer from "~/components/Composer";
import FileExpander from "~/components/FileExpander";
import FastNavigation from "~/components/FastNavigation";

export default {
  components: { BoardHeader, Thread, Composer, FileExpander, FastNavigation },
  data: () => { return {
    request_nonce: null,
    subscription_nonce: null,
    display: 10,
    displayed_threads: [],
    stale: false,
    header_visible: true,
  }},
  watch: {
    board(new_board) {
      console.log(this);
      if (this.displayed_threads.length == 0 || this.header_visible) {
        this.update()
      } else {
        this.stale = true;
      }
    }
  },
  computed: {
    pk() {
      return this.$route.params.pk;
    },
    board() {
      return this.$store.state.boards[this.pk] || {};
    },
    new_threads() {
      return this.board.thread_set || [];
    },
    threads() {
      return this.displayed_threads.slice(0, this.display);
    }
  },
  methods: {
    ...mapActions(['board_detail', 'watch_board', 'post_thread']),
    new_thread({message, upload_tokens}) {
      this.post_thread({pk: this.pk, message: message, upload_tokens})
    },
    update() {
      this.displayed_threads = this.new_threads;
      this.stale = false;
      this.display = 10;
    },
    load_more(vis) {
      if (vis) {
        console.log("loading more");
        this.display += 10;
      }
    },
    set_header_visibility(vis) {
      this.header_visible = vis;
      if (vis) {
        this.update();
      }
    },
    scroll_to_top() {
      window.scrollTo(0,0);
    },
    open_preview(path) {
      console.log("open!");
      this.$refs.expander.show(path)
    }
  },
  async fetch({store, route}) {
    await store.dispatch('board_detail', route.params.pk);
    store.dispatch('watch_board', route.params.pk).catch((err) => {
      console.log("err");
    });
  },
  /*mounted () {
    this.board_detail(this.$route.params.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
    this.watch_board(this.$route.params.pk).then((nonce) => {
      this.subscription_nonce = nonce;
    });
  }*/
}
</script>
