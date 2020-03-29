<template>
  <div class="contain">
    <div class="compose box" :class="{'open': enabled}" @keydown.esc="enabled=false">
      <div class="uploading" v-if="uploading">
        <div class="progress" :style="`right: calc(100% - ${progress})`"></div>
        <div class="label">Uploading...</div>
      </div>
      <textarea ref="input" placeholder="Type your message here..." v-model="message">
      </textarea>
      <div class="navigation">
        <div class="interact button add send" @click="upload">
          <font-awesome-icon icon="reply"/>
          <span class="hint" v-if="hint">{{hint}}</span>
        </div>
        <div class="interact button close" @click="enabled=false">
          <font-awesome-icon icon="times"/>
        </div>
        <input type="file" v-if="uploads" ref="upload" multiple>
      </div>
    </div>
    <div class="box navigation navmargin" :class="{'collapse': enabled}">
      <div class="interact button reply add" @click="enable">
        <font-awesome-icon icon="reply"/>
        <span class="hint" v-if="hint">{{hint}}</span>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.contain {
  position: relative;
}

.uploading {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: var(--background);
  animation: upload 0.3s ease-in-out;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.5
}

.progress {
  z-index: 0;
  position: absolute;
  top: 0;
  bottom: 0;
  left: 0;
  transition: right linear 0.2s;
  background-color: var(--green);
  opacity: 0.7;
}

.label {
  z-index: 1;
}

@keyframes upload {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 0.5;
  }
}


.desc {
  margin-left: 0.6ch;
}

.navigation {
  display: flex;
  align-items: center;
  max-height: 50px;
  transition: max-height 0.3s ease-in-out, opacity 0.3s ease-in-out;

  &.collapse {
    overflow: hidden;
    max-height: 0;
    padding-top: 0;
    padding-bottom: 0;
    opacity: 0;
  }

  .navmargin {
    padding: 10px;
  }

  .close {
    justify-self: flex-end;
  }
}

.compose {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  max-height: 0px;
  overflow: hidden;
  padding-top: 0;
  padding-bottom: 0;
  transition: max-height 0.2s ease-in-out, opacity 0.2s ease-in-out;
  opacity: 0;

  &.open {
    padding: 8px;
    max-height: 100px;
    opacity: 1;
  }

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

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

export default {
  props: ["text", "uploads"],
  data: () => {return {
    message: "",
    enabled: false,
    upload_tokens: [],
    uploading: false,
  }},
  computed: {
    hint() {
      return this.text || "";
    },
    progress() {
      let files = this.$refs.upload.files.length;
      let complete = this.upload_tokens.length;
      return `${Math.ceil((complete/files) * 100)}%`;
    }
  },
  methods: {
    upload() {
      const files = new Array(...this.$refs.upload.files);
      this.uploading = true;
      files.reduce((curr, attachment) => {
        return curr.then(() => {
          return fetch("http://localhost:8000/upload/").then((response) => {
            return response.json().then((json) => {
              let form = new FormData();
              form.append("attachment", attachment);
              return fetch("http://localhost:8000/upload/", {
                method: "POST", 
                body: form, 
                credentials: "include",
                headers: {
                  "X-CSRFToken": getCookie('csrftoken')
                }
              })
            }).then((response) => {
              if (response.ok) {
                return response.json().then((json) => {
                  this.upload_tokens.push(json.upload_token)
                });
              } else {
                return Promise.reject("File upload failed.");
              }
            });
          })
        })
      }, Promise.resolve()).then(()=>{
        this.send();
      }).catch(() => {
        this.uploading = false;
      })
    },
    send() {
      this.$emit('send', {
        message: this.message, 
        upload_tokens: this.upload_tokens
      });
      this.uploading = false;
      this.upload_tokens = [];
      this.enabled = false;
      this.message = "";
      this.$refs.upload.value = "";
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