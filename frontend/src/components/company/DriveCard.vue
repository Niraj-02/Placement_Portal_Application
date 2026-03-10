<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  drive: Object,
  showCompleteButton: Boolean
})

const router = useRouter()

function viewApplications(){
  router.push(`/company/drive/${props.drive.id}/applications`)
}

async function markComplete(){
  await fetch(`http://127.0.0.1:5000/api/drives/${props.drive.id}`,{
    method:"PATCH",
    headers:{
      Authorization:"Bearer "+localStorage.getItem("token")
    }
  })

  location.reload()
}
</script>

<template>

    <div class="card p-3 mb-3">

        <h5>{{ drive.job_title }}</h5>

        <p>Location: {{ drive.location }}</p>
        <p>Salary: {{ drive.salary }}</p>
        <p>Status: {{ drive.hiring_status }}</p>

        <div class="d-flex gap-2">

            <button class="btn btn-primary" @click="viewApplications">View Applications</button>
            <button v-if="showCompleteButton" class="btn btn-danger" @click="markComplete">Mark Complete</button>

        </div>

    </div>

</template>