<template>
  <div class="compose">
    <textarea v-model="message" cols="80" rows="3">
    </textarea>
    <button class="send" @click="$emit('send', message)">Send</button>
  </div>
</template>

<script>
import { mapActions } from 'vuex';
import ProfilePreview from "~/components/ProfilePreview";
import Reply from "~/components/Reply";

const PREVIEW_REPLIES = 3;

export default {
  data: () => {return {
    message: ""
  }},
}
</script>