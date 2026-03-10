<script setup>

import { ref, onMounted } from 'vue'

const drives = ref([])

async function getDrives(){

    const res = await fetch(
        "http://127.0.0.1:5000/api/drives",
        {
            headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
            }
        }
    )

    const data = await res.json()

    drives.value = data.filter(d => d.status === "pending")

}

onMounted(getDrives)

</script>


<template>

<h4 class="mb-3">Pending Approval Drives</h4>

<div v-if="drives.length === 0">
    <p class="text-muted">No pending drives</p>
</div>

<div v-for="drive in drives" :key="drive.id" class="card p-3 mb-3">

    <h5>{{ drive.job_title }}</h5>

    <p>Location: {{ drive.location }}</p>
    <p>Salary: {{ drive.salary }}</p>

    <span class="badge bg-warning">
        Awaiting Admin Approval
    </span>

</div>

</template>