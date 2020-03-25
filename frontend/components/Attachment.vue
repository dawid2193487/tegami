<template>
    <div class="attachment box interact">
        <a :href="`http://localhost:8000${data.path}`">
            <img :src="`http://localhost:8000${data.thumb}`"/>
        </a>
        <div class="filename">{{data.name}}</div>
    </div>
</template>

<style lang="scss">
.attachment {
    // width: 200px;
    height: 200px;
    flex-basis: 20%;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    overflow: hidden;
    margin-right: 10px;
    border-radius: 10px;
    padding: 0;
    position: relative;

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