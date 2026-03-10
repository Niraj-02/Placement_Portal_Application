<script setup>

import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const driveId = route.params.id

const applications = ref([])

async function getApplications(){

  const res = await fetch(
    `http://127.0.0.1:5000/api/application?drive_id=${driveId}`,
    {
      headers:{
        Authorization:"Bearer "+localStorage.getItem("token")
      }
    }
  )

  const data = await res.json()

  applications.value = data

}

async function updateStatus(appId,status){

  await fetch(
    `http://127.0.0.1:5000/api/application/${appId}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body:JSON.stringify({
        status:status
      })
    }
  )

  getApplications()

}

onMounted(getApplications)

</script>

<template>

<div class="container mt-4">

<h3>Drive Applications</h3>

<table class="table">

<thead>
<tr>
<th>Application ID</th>
<th>Student ID</th>
<th>Status</th>
<th>Actions</th>
</tr>
</thead>

<tbody>

<tr v-for="app in applications" :key="app.id">

<td>{{ app.id }}</td>
<td>{{ app.student_id }}</td>
<td>{{ app.status }}</td>

<td>

<button class="btn btn-sm btn-success me-1"
@click="updateStatus(app.id,'shortlisted')">
Shortlist
</button>

<button class="btn btn-sm btn-primary me-1"
@click="updateStatus(app.id,'interview')">
Interview
</button>

<button class="btn btn-sm btn-warning me-1"
@click="updateStatus(app.id,'selected')">
Select
</button>

<button class="btn btn-sm btn-danger"
@click="updateStatus(app.id,'rejected')">
Reject
</button>

</td>

</tr>

</tbody>

</table>

</div>

</template>