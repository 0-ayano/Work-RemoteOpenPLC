<template>
	<div id="str-title"> Running </div>
	<TopicPath id="topicpath"></TopicPath>
	<div>
		<img class="camera" v-bind:src="video_url" alt="Camera" />
	</div>

	<div class="gauge-container">
		<RunGauge v-for="(form, index) in forms" :key="index" :dataURL=form.URL :title=form.TITLE :max=form.MAX
			:min=form.MIN :unit=form.UNIT></RunGauge>
	</div>

	<div class="line-container">
		<RunLine v-for="(form, index) in forms" :key="index" :dataURL=form.URL :title=form.TITLE :max=form.MAX :min=form.MIN
			:unit=form.UNIT :numDataPoints="10">
		</RunLine>
	</div>

	<div id="buttons">
		<div id="contens-center">
			<!-- now mode : {{ experiment.now_mode() }} -->
			<RunController ></RunController>
		</div>
	</div>
</template>
  
<script setup>
import TopicPath from '@/components/TopicPath.vue';
import RunGauge from '@/components/RunGauge.vue';
import RunLine from '@/components/RunLine.vue';
import RunController from '@/components/RunController.vue';

import { ref, onMounted } from 'vue';

const video_url = ref("http://127.0.0.1:8000/camera/0");
const forms = ref([]);

onMounted(async () => {
	try {
		const response = await fetch("../../public/display.json");
		const data = await response.json();
		forms.value = data;
	} catch (error) {
		console.error("Error fetching data:", error);
	}
});
</script>
  
<style scoped>
.camera {
	position: absolute;
	top: 17vh;
	right: 5vw;
	width: 25%;
	background-color: #84b1ed;
	aspect-ratio: 16 / 11;
}

.gauge-container {
	position: absolute;
	bottom: 9vh;
	left: 7vw;
	width: 60%;
	height: 35%;
	display: flex;
	align-items: center;
	white-space: nowrap;
	overflow-x: auto;

	border-top: solid 5px #5d627b;
	box-shadow: 0 3px 5px rgba(0, 0, 0, 0.22);
}

.line-container {
	position: absolute;
	top: 17vh;
	left: 7vw;
	width: 60%;
	height: 35%;
	display: flex;
	align-items: center;
	white-space: nowrap;
	overflow-x: auto;

	border-top: solid 5px #5d627b;
	box-shadow: 0 3px 5px rgba(0, 0, 0, 0.22);
}

#buttons {
	position: absolute;
	bottom: 9vh;
	right: 5vw;
	width: 25%;
	height: 35%;
}

#contens-center {
	position: absolute;
	width: 80%;
	height: 100%;
	left: 45%;
	transform: translateX(-50%);
}
</style>

<!-- 
	Reference
    - [【CSS】おしゃれなボックスデザイン（囲み枠）のサンプル30](https://saruwakakun.com/html-css/reference/box)
    - []()
 -->