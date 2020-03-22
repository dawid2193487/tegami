<template>
  <div class="container">
    <div class="thread box" v-if="ready">
      <div class="meta">
        <span class="poster"><ProfilePreview :pk="thread.posted_by"/></span>
        &bull;
        <span class="date">{{thread.posted_at}}</span>
      </div>
      <div class="message">{{thread.message}}</div>
      <Replies :reply_set="thread.reply_set"/>
    </div>
    <div class="thread box loading" v-else-if="loading">
      Loading...
    </div>
  </div>
</template>

<style lang="scss" scoped>
// .thread {
//   background-color: rgb(255, 255, 255);
//   padding: 0.5em;
//   box-shadow: 0px 1px 2px var(--shadow);
//   transition: box-shadow 0.05s ease-in-out;
//   max-width: 800px;
// }
</style>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Replies from "~/components/Replies";

export default {
  components: { ProfilePreview, Replies },
  props: ["pk"],
  data: () => { return {
    request_nonce: null,
  }},
  methods: {
    ...mapActions(['thread_detail'])
  },
  computed: {
    thread() {
      return this.$store.state.threads[this.pk] || {};
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
    this.thread_detail(this.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>