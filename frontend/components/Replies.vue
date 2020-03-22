<template>
  <div class="container">
      <Reply v-for="pk in replies_pks" :key="pk" :pk="pk"/>
  </div>
</template>

<style lang="scss" scoped>
.thread {
  background-color: rgb(255, 255, 255);
  padding: 0.5em;
  box-shadow: 0px 1px 1px var(--shadow);
  transition: box-shadow 0.05s ease-in-out;
  max-width: 800px;
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
import ProfilePreview from "~/components/ProfilePreview";
import Reply from "~/components/Reply";

export default {
  components: { ProfilePreview, Reply },
  props: ["pk"],
  data: () => { return {
    request_nonce: null,
  }},
  methods: {
    ...mapActions(['reply_list'])
  },
  computed: {
    replies_pks() {
      return this.$store.state.threads[this.pk].replies || {};
    },
    ready() {
      if (this.request_nonce == null) {
        return false;
      }
      return this.$store.state.requests[this.request_nonce] == "complete" || this.pk == null;
    },
    loading() {
      if (this.request_nonce == null) {
        return true;
      }
      return this.$store.state.requests[this.request_nonce] == "pending";
    }
  },
  mounted () {
    if (this.pk == null) {
      return;
    }

    this.reply_list(this.pk).then((nonce) => {
      this.request_nonce = nonce;
    });
  }
}
</script>