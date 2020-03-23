<template>
  <div class="contain">
    <div class="compose box" v-if="enabled">
      <textarea placeholder="Type your message here..." v-model="message">
      </textarea>
      <button class="box interact button add send" @click="send">
        <font-awesome-icon icon="reply"/>
      </button>
      <button class="box interact button" @click="enabled=false">
        <font-awesome-icon icon="times"/>
      </button>
    </div>
    <div class="box interact button add" v-else @click="enabled=true">
      <font-awesome-icon icon="reply"/>
      <span class="desc">Reply</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.desc {
  margin-left: 0.6ch;
}

.contain {
  transition: 0.5s height ease-in-out;
}

.compose {
  display: flex;
  align-items: center;
  justify-content: space-around;

  button {
    border: unset;
    margin-top: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    height: 50px;
    width: 50px;
  }

  textarea {
    flex-basis: 80%;
    font-family: Arial, Helvetica, sans-serif;
    border: unset;
    padding: 0.4em;
    resize: none;
    border-bottom: 1px solid var(--shadow);
  }
}

</style>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Reply from "~/components/Reply";

const PREVIEW_REPLIES = 3;

export default {
  data: () => {return {
    message: "",
    enabled: false,
  }},
  methods: {
    send() {
      this.$emit('send', this.message);
      this.enabled = false;
      this.message = "";
    }
  }
}
</script>