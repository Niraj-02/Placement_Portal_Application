<script setup>

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const drives = ref([])

async function getDrives(){

    const res = await fetch("http://127.0.0.1:5000/api/drives",{
        headers:{
            Authorization:"Bearer "+localStorage.getItem("token")
        }
    })

    const data = await res.json()

    drives.value = data.filter(d => d.hiring_status === "completed")

}

function viewDetails(id){
    router.push(`/company/drive/${id}/applications`)
}

onMounted(getDrives)

</script>

<template>

<h4 class="mb-3">Completed Drives</h4>

<div v-for="drive in drives" :key="drive.id" class="card mb-3 p-3">

    <h5>{{ drive.job_title }}</h5>

    <button
    class="btn btn-outline-primary"
    @click="viewDetails(drive.id)">
    View Details
    </button>

</div>

</template>