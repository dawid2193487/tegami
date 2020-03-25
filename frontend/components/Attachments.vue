<template>
    <div class="attachments box" v-if="set.length > 0">
        <Attachment v-for="attachment in set" :data="attachment" :key="attachment.name"/>
    </div>
</template>

<style lang="scss" scoped>
.attachments {
    display: flex;
    flex-wrap: wrap;
}
</style>

<script>
import Attachment from "~/components/Attachment";
export default {
    components: { Attachment },
    props: ["set"]
}
</script>