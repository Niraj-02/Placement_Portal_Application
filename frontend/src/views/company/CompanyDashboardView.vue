<template>

<div class="container mt-4">

    <div class="d-flex justify-content-between align-items-center mb-4">

        <h2>Company Dashboard</h2>

        <button class="btn btn-primary" @click="createDrive">
            + Create Drive
        </button>

    </div>

    <PendingDrives />

    <hr><hr>

    <OngoingDrives />

    <hr><hr>

    <CompletedDrives />

</div>

</template>


<script setup>
import { onMounted } from 'vue';
import OngoingDrives from '@/components/company/OngoingDrives.vue'
import CompletedDrives from '@/components/company/CompletedDrives.vue'
import PendingDrives from '@/components/company/PendingDrives.vue'
import { useRouter } from 'vue-router'

const router = useRouter()

function createDrive(){
    router.push('/company/create-drive')
}


onMounted(()=>{

  const token = localStorage.getItem("token")
  const role = localStorage.getItem("role")
  if (!token) {
    // alert admin login is required to access admin dashboard
    alert("Please Login.")
    router.push("/login")
  }
  if(role !== "company"){
    alert("Unauthorized access!!!")
    router.push("login")
  }

})

</script>
