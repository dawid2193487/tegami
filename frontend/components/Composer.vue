<template>
  <div class="contain">
    <div class="compose box" v-if="enabled" @keydown.esc="enabled=false">
      <textarea ref="input" placeholder="Type your message here..." v-model="message">
      </textarea>
      <div class="navigation">
        <div class="interact button add send" @click="send">
          <font-awesome-icon icon="reply"/>
          <span class="hint" v-if="hint">{{hint}}</span>
        </div>
        <div class="interact button close" @click="enabled=false">
          <font-awesome-icon icon="times"/>
        </div>
      </div>
    </div>
    <div class="box navigation navmargin" v-else>
      <div class="interact button reply add" @click="enable">
        <font-awesome-icon icon="reply"/>
        <span class="hint" v-if="hint">{{hint}}</span>
      </div>
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

.navigation {
  display: flex;
  align-items: center;

  .navmargin {
    padding: 10px;
  }

  .close {
    justify-self: flex-end;
  }
}

.compose {
  display: flex;
  flex-wrap: wrap;

  .button {
    margin-right: 10px;

  }


  textarea {
    background-color: var(--background);
    color: var(--color);
    *::placeholder {
      color: var(--color);
    }
    flex-basis: 100%;
    font-family: Arial, Helvetica, sans-serif;
    border: unset;
    padding: 0.4em;
    margin-bottom: 5px;
    resize: none;
    border-bottom: 1px solid var(--shadow);
  }
}

.hint {
  margin-left: 5px;
}

</style>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Reply from "~/components/Reply";

const PREVIEW_REPLIES = 3;

export default {
  props: ["text"],
  data: () => {return {
    message: "",
    enabled: false,
  }},
  computed: {
    hint() {
      return this.text || "";
    }
  },
  methods: {
    send() {
      this.$emit('send', this.message);
      this.enabled = false;
      this.message = "";
    },
    enable() {
      this.enabled = true;
      this.$nextTick(() => {
        this.$refs.input.focus();
      })
    }
  }
}
</script>