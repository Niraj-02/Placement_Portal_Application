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

    drives.value = data.filter(d => d.hiring_status === "ongoing")
}

function viewApplications(id){
    router.push(`/company/drive/${id}/applications`)
}

// Mark as completed function 
async function markComplete(id){

  const res = await fetch(
    `http://127.0.0.1:5000/api/drives/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body: JSON.stringify({
        hiring_status:"completed"
      })
    }
  )
  const data = await res.json()

  alert(data.message)

  getDrives()
}

onMounted(getDrives)

</script>

<template>

<h4 class="mb-3">Ongoing Drives</h4>

<div v-for="drive in drives" :key="drive.id" class="card mb-3 p-3">

    <h5>{{ drive.job_title }}</h5>
    <p>Location: {{ drive.location }}</p>
    <p>Salary: {{ drive.salary }}</p>

    <div class="d-flex gap-2">

        <button
        class="btn btn-outline-primary"
        @click="viewApplications(drive.id)">
        View Applications
        </button>

        <button
        class="btn btn-outline-danger"
        @click="markComplete(drive.id)">
        Mark Complete
        </button>

    </div>

</div>

</template>