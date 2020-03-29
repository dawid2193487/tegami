<template>
    <div class="attachments" v-if="set.length > 0">
        <Attachment v-for="attachment in set" :data="attachment" :key="attachment.name"/>
    </div>
</template>

<style lang="scss" scoped>
.attachments {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr 1fr;
    row-gap: 10px;
    column-gap: 10px;
    margin-bottom: 10px;
}
</style>

<script>
import Attachment from "~/components/Attachment";
export default {
    components: { Attachment },
    props: ["set"]
}
</script>