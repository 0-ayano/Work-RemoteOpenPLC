<template>
    <div class="buttonIconText" @click="nextPage()">
        <span class="buttonIconText_icon">
            <img width="32" height="32" viewBox="0 0 24 24" :src="svg_path">
        </span>
        <span class="buttonIconText_text">{{ props.name }}</span>
    </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { ref, onMounted } from 'vue';

const router = useRouter()
const props = defineProps(['name', 'path', 'next'])
const svg_path = ref("")

const nextPage = () => {
    if (props.next === undefined) {
        alert("Undefined Pages Error: Please contact the developer")
    } else {
        router.push(props.next)
    }
}

onMounted(async () => {
    svg_path.value = props.path
    if (props.path === undefined) {
        svg_path.value = "../../public/undefined.svg"
    }
});

</script>

<style scoped>
.buttonIconText {
    display: flex;
    gap: 8px;
    align-items: center;
    width: 100%;
    max-width: 70em;
    height: 64px;
    padding: 8px 40px 8px 8px;
    font-family: sans-serif;
    font-size: 16px;
    color: #0f0f0f;
    text-align: center;
    overflow-wrap: anywhere;
    background-color: #f0b5a4;
    border-radius: 32px;
    margin-bottom: 8%;
}

.buttonIconText__reverse {
    flex-direction: row-reverse;
    padding: 8px 8px 8px 40px;
}

.buttonIconText_icon {
    display: flex;
    flex-shrink: 0;
    align-items: center;
    justify-content: center;
    width: 48px;
    aspect-ratio: 1;
    padding: 4px;
    overflow: hidden;
    background-color: #fff;
    border-radius: 50%;
}

.buttonIconText_text {
    flex-shrink: 1;
    font-weight: bolder;
    font-size: larger;
    width: 100%;
    user-select: none;
}

@media (any-hover: hover) {
    .buttonIconText {
        transition: background-color 0.2s;
    }

    .buttonIconText_icon_item {
        transition: background-color 0.2s;
    }

    .buttonIconText:hover {
        background-color: #ee7785;
    }
}
</style>

<!-- 
    Reference
    - [シンプルで使いやすいHTML・CSSボタンデザイン集11選 - ICS MEDIA](https://ics.media/entry/230629/)
        - アイコンとテキストが横並ぶボタン
 -->