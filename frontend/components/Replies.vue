<template>
  <div class="container">
    <div v-if="expanded" class="replies">
      <div class="expander box link interact" v-if="hidden_amount > 0" @click="expanded = false">
        Collapse {{ hidden_amount }} replies.
      </div>
      <Reply v-for="pk in reply_set" :key="pk" :pk="pk"/>
    </div>
    <div v-else class="replies">
      <div class="expander box link interact" v-if="hidden_amount > 0" @click="expand()">
        Load {{ hidden_amount }} more replies.
      </div>
      <Reply v-for="pk in latest" :key="pk" :pk="pk"/>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.replies {
  margin-top: 5px;
}
.expander {
  position: sticky;
  top: 0px;
  z-index: 2;
}
</style>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Reply from "~/components/Reply";

const PREVIEW_REPLIES = 3;

export default {
  components: { ProfilePreview, Reply },
  props: ["pk", "reply_set"],
  data: () => {return {
    expanded: false,
  }},
   methods: {
    ...mapActions(['reply_list']),
    expand() {
      this.reply_list(this.pk).then((nonce) => {
        this.expanded = true;
      });
    },
  },
  computed: {
    latest() {
      return this.reply_set.slice(-PREVIEW_REPLIES)
    },
    hidden_amount() {
      return Math.max(this.reply_set.length - PREVIEW_REPLIES, 0);
    }
  }
}
</script>