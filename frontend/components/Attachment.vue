<template>
    <div class="attachment box interact" :class="{'noimg': data.thumb == null}">
        <a :href="`http://localhost:8000${data.path}`">
            <img v-if="data.thumb" :src="`http://localhost:8000${data.thumb}`"/>
            <div v-else class="placeholder"><font-awesome-icon icon="file"/></div>
        </a>
        <div class="filename">{{data.name}}</div>
    </div>
</template>

<style lang="scss">
.attachment {
    // width: 200px;
    height: 150px;
    flex-basis: 20%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    //margin-right: 10px;
    border-radius: 10px;
    padding: 0;
    position: relative;
    .placeholder {
        font-size: 400%;
    }
    &.noimg {
        .filename {
            opacity: 1;
        }
    }

    &:hover {
        .filename {
            opacity: 0.7;
            background-image: linear-gradient(to top, var(--background) 60%, transparent 100%);
        }
    }

    .filename {
        padding-top: 10%;
        display: flex;
        justify-content: center;
        overflow-wrap: anywhere;
        position: absolute;
        bottom: 0;
        opacity: 0;
        width: 100%;
        transition: opacity 0.2s ease-in-out;
    }


    a {
        width: 100%;
        height: 100%;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    a > img {
        width: 100%;
        height: 100%;
        object-fit: cover;
    }
}

</style>

<script>
export default {
    props: ["data"],
}
</script>