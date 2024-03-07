import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import axios from 'axios';

// export const useCounterStore = defineStore('counter', () => {
//     const count = ref(0)
//     const doubleCount = computed(() => count.value * 2)
//     function increment() {
//         count.value++
//     }

//     return { count, doubleCount, increment }
// })

export const result_experiment = defineStore('result', () => {
    const result = ref({})

    function cleate_dict(title) {
        result.value[title] = []
    }

    function push_result(title, newResult) {
        if ( !(title in result.value) ) {
            result.value[title] = []
        }
        result.value[title].push(newResult)
    }

    function clear_result() {
        result.value = {}
    }

    function get_result(title){
        return result.value[title]
    }

    function get_new_result(title){
        if ( !(title in result.value) ) {
            return 0
        }
        else {
            return result.value[title].slice(-1)[0]
        }
    }

    return{ result, cleate_dict, push_result, clear_result, get_result, get_new_result }
})

export const control_experiment = defineStore('control_experiment', () => {
    const mode = ref(false)

    async function start_experiment() {
        const res = await axios.get("http://127.0.0.1:8000/start_coil/" );
        alert(res.data)
        mode.value = true
    }

    async function stop_experiment() {
        const res = await axios.get("http://127.0.0.1:8000/stop_coil/");
        alert(res.data)
        mode.value = false
    }

    function now_mode(){
        return mode.value
    }

    return { start_experiment, stop_experiment, now_mode }
})