<template>
  <div class="container">
    <div class="reply box loading" v-if="$fetchState.pending">
      Loading...
    </div>
    <div class="reply box" v-else>
      <div class="meta">
        <span class="poster"><ProfilePreview :pk="reply.posted_by"/></span>
        &bull;
        <span class="date">{{date}}</span>
      </div>
      <div class="message">{{reply.message}}</div>
      <Attachments :set="reply.attachments"/>
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
import { format } from 'timeago.js';

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
    date() {
      return format(new Date(this.reply.posted_at));
    },
    // ready() {
    //   if (this.request_nonce == null) {
    //     return false;
    //   }
    //   return this.$store.state.requests[this.request_nonce] == "complete" || this.pk == null;
    // },
    // old_available() {
    //   return this.$store.state.replies[this.pk] !== undefined
    // },
    // loading() {
    //   if (this.request_nonce == null) {
    //     return true;
    //   }
    //   return this.$store.state.requests[this.request_nonce] == "pending";
    // }
  },
  async fetch() {
    await this.$store.dispatch('reply_detail', this.pk);
    /*store.dispatch('watch_board', route.params.pk).catch((err) => {
      console.log("err");
    });*/
  },
  // mounted () {
  //   this.reply_detail(this.pk).then((nonce) => {
  //     this.request_nonce = nonce;
  //   });
  // }
  
}
</script>