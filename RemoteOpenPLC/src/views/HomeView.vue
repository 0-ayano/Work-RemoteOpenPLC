<template>
    <div id="str-title"> Remote OpenPLC </div>
    <div id="contens-center">
        <HomeButton name="Setting" path='../../public/setting.svg' next="set"></HomeButton>
        <HomeButton name="Run OpenPLC" path='../../public/running.svg' next="run"></HomeButton>
    </div>
    <TopicPath id="topicpath"></TopicPath>
</template>

<script setup>
import HomeButton from '@/components/HomeButton.vue';
import TopicPath from '@/components/TopicPath.vue';

</script>

<style scoped>
#contens-center {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -50%);
}
</style>