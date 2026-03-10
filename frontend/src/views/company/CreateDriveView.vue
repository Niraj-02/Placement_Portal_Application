<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const job_title = ref("")
const job_description = ref("")
const location = ref("")
const salary = ref("")
const deadline = ref("")

const selectedBranches = ref([])

const ALL_BRANCHES = [
  "Computer Science",
  "Information Technology",
  "Data Science",
  "Electronics and Communication",
  "Electrical Engineering",
  "Mechanical Engineering",
  "Civil Engineering",
  "Chemical Engineering",
  "Metallurgical Engineering"
]

function addBranch(branch){
  if(!selectedBranches.value.includes(branch)){
    selectedBranches.value.push(branch)
  }
}

function removeBranch(branch){
  selectedBranches.value =
    selectedBranches.value.filter(b => b !== branch)
}


async function createDrive(){

  const res = await fetch(
    "http://127.0.0.1:5000/api/drives",
    {
      method:"POST",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body:JSON.stringify({
        job_title:job_title.value,
        job_type:"on-site",
        job_description:job_description.value,
        eligibility_criteria:"NA",
        eligible_branches:selectedBranches.value.join(","),
        min_cgpa:6,
        eligible_year:"2025",
        application_deadline:deadline.value,
        salary:Number(salary.value),
        location:location.value
      })
    }
  )

  const data = await res.json()

  alert(data.message)

  router.push('/company_dashboard')

}

</script>


<template>

<div class="container mt-4">

<h3>Create Drive</h3>

<input v-model="job_title" placeholder="Job Title" class="form-control mb-2">

<textarea v-model="job_description" placeholder="Description" class="form-control mb-2"></textarea>

<input v-model="location" placeholder="Location" class="form-control mb-2">

<input type="number" v-model="salary" placeholder="Salary" class="form-control mb-2">

<input type="datetime-local" v-model="deadline" class="form-control mb-3">


<!-- Branch Selector -->

<label class="form-label">Eligible Branches</label>

<select class="form-select mb-2" @change="addBranch($event.target.value)">

<option disabled selected>Select branch</option>

<option v-for="b in ALL_BRANCHES" :key="b" :value="b">
{{ b }}
</option>

</select>


<!-- Selected Branch Tags -->

<div class="mb-3">

<span
v-for="b in selectedBranches"
:key="b"
class="badge bg-primary me-2 p-2"
>

{{ b }}

<button
class="btn-close btn-close-white ms-2"
style="font-size:10px"
@click="removeBranch(b)">
</button>

</span>

</div>


<button class="btn btn-success" @click="createDrive">
Create Drive
</button>

</div>

</template>