<template>
  <div class="container">
    <div class="reply box" :class="{loading}" v-if="ready || old_available">
      <div class="meta">
        <span class="poster"><ProfilePreview :pk="reply.posted_by"/></span>
        &bull;
        <span class="date">{{reply.posted_at}}</span>
      </div>
      <div class="message">{{reply.message}}</div>
      <Attachments :set="reply.attachments"/>
    </div>
    <div class="reply box loading" v-else-if="loading">
      Loading...
    </div>
  </div>
</template>

<style lang="scss" scoped>
// .reply {
//   background-color: rgb(255, 255, 255);
//   padding: 0.5em;
//   box-shadow: 0px 1px 2px var(--shadow);
//   transition: box-shadow 0.05s ease-in-out;
//   max-width: 800px;
//   margin-top: 1px;
// }

</style>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Attachments from "~/components/Attachments";

export default {
  components: { ProfilePreview, Attachments },
  props: ["pk"],
  data: () => { return {
    request_nonce: null,
  }},
  methods: {
    ...mapActions(['reply_detail'])
  },
  computed: {
    reply() {
      return this.$store.state.replies[this.pk] || {};
    },
    ready() {
      if (this.request_nonce == null) {
        return false;
      }
      return this.$store.state.requests[this.request_nonce] == "complete" || this.pk == null;
    },
    old_available() {
      return this.$store.state.replies[this.pk] !== undefined
    },
    loading() {
      if (this.request_nonce == null) {
        return true;
      }
      return this.$store.state.requests[this.request_nonce] == "pending";
    }
  },
  mounted () {
    this.reply_detail(this.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>