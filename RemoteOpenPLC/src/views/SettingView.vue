<template>
    <div id="str-title">Setting</div>
    <TopicPath id="topicpath"></TopicPath>

    <div id="forms" class="forms-container">
        <h1>表示するデータを入力してください</h1>
        <div v-for="(form, index) in forms" :key="index" class="form-replication_target">
            <p>データ名：<input type="text" v-model="form.TITLE" name="TITLE"></p>
            <p>URL &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;：<input type="text" v-model="form.URL" name="URL"></p>
            <p>最大値　：<input type="number" v-model="form.MAX" name="MAX"></p>
            <p>最小値　：<input type="number" v-model="form.MIN" name="MIN"></p>
            <p>単位　　：<input type="text" v-model="form.UNIT" name="UNIT"></p>
            <button @click="addForm" :disabled="forms.length >= 3">追加する</button>
            <button @click="removeForm(index)" :disabled="forms.length <= 1">削除する</button>
        </div>

        <button @click="memoryData()">保存する</button>
    </div>
</template>

<script setup>
import TopicPath from '@/components/TopicPath.vue';
import { ref, onMounted } from 'vue';

const forms = ref([
    { TITLE: '', URL: '', MAX: null, MIN: null, UNIT: '' }
]);

const addForm = () => {
    if (forms.value.length < 3) {
        forms.value.push({ TITLE: '', URL: '', MAX: null, MIN: null, UNIT: '' });
    }
};

const removeForm = (index) => {
    if (forms.value.length > 1) {
        forms.value.splice(index, 1);
    }
};

onMounted(async () => {
    try {
        const response = await fetch("../../public/display.json");
        const data = await response.json();
        forms.value = data;
    } catch (error) {
        console.error("Error fetching data:", error);
    }
});

const memoryData = () => {
    const isValid = forms.value.every((form) => {
        const isNotEmpty = (formItem) =>
            formItem.TITLE.trim() !== '' &&
            formItem.URL.trim() !== '' &&
            formItem.MAX !== null &&
            formItem.MIN !== null &&
            formItem.UNIT.trim() !== '';
        const isNumeric = !isNaN(form.MAX) && !isNaN(form.MIN);
        const isMinLessThanMax = form.MIN < form.MAX;
        const isSameTitle = new Set(forms.value.map(item => item.TITLE)).size !== forms.value.length;

        return isNotEmpty(form) && isNumeric && isMinLessThanMax && !isSameTitle;
    });

    if (isValid) {
        const jsonData = JSON.stringify(forms.value, null, 2);
        const blob = new Blob([jsonData], { type: 'application/json' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'display.json';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    }
    else {
        alert('Input Erro: Please fill in all fields properly before saving.');
    }
};
</script>

<style scoped>
#forms {
    position: absolute;
    left: 50%;
    top: 50%;
    transform: translate(-50%, -45%);
    height: 80vh;
    width: 90vw;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    align-items: center;
}

.form-replication_target {
    margin-bottom: 10px;
}

.form-replication_target:last-child {
    margin-bottom: 0;
}
</style>