<script setup>

import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// all form field 
const start_date = ref("")
const deadline = ref("")

const job_title = ref("")
const job_type = ref("on-site")
const job_description = ref("")

const skills_required = ref("")
const eligibility_criteria = ref("")
const min_cgpa = ref("")
const eligible_year = ref("")

const location = ref("")
const salary = ref("")
const bond_details = ref("")
const openings_count = ref(1)


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

// adding eligible branches  
function addBranch(branch){
  if(!selectedBranches.value.includes(branch)){
    selectedBranches.value.push(branch)
  }
}

// deselecting a branch 
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
        job_type:job_type.value,
        job_description:job_description.value,
        skills_required:skills_required.value,

        eligibility_criteria:eligibility_criteria.value,
        eligible_branches:selectedBranches.value.join(","),
        min_cgpa:Number(min_cgpa.value),
        eligible_year:eligible_year.value,

        start_date:start_date.value,
        application_deadline:deadline.value,

        openings_count: Number(openings_count.value),
        bond_details:bond_details.value,
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

  <div class="container mt-4" style="max-width:700px">
    <h3 class="mb-4">Create placement drive</h3>

    <!-- Job details  -->
    <h6 class="mb-2">Job Details</h6>

    <input v-model="job_title" class="form-control mb-2" placeholder="Job Title">
    
    <select v-model="job_type" class="form-select mb-2">
      <option value="on-site">On Site</option>
      <option value="remote">Remnote</option>
      <option value="hybrid">Hybrid</option>
    </select>

    <textarea v-model="job_description" class="form-control mb-2" placeholder="Job description"></textarea>
    <input v-model="skills_required" class="form-control mb-3" placeholder="Skills required">

    <h6 class="mb-2">Eligibility</h6>

    <textarea v-model="eligibility_criteria" class="form-control mb-2" placeholder="Any desirable skillsets..(optional for students)"></textarea>

    <input type="number" v-model="min_cgpa" class="form-control mb-2" placeholder="Minimum CGPA ">

    <select v-model="eligible_year" class="form-select mb-3">
      <option disabled value="">Select eligible year</option>
      <option>3rd Year</option>
      <option>4th Year</option>
    </select>

    <input class="form-control mb-2" type="number" v-model="salary" placeholder="Salary CTC"></input>

    <input v-model="location" class="form-control mb-4" placeholder="Company location">

    <!-- Branch selection -->
     <label class="form-label">Eligible branches</label>

     <select class="form-select mb-2" @change="addBranch($event.target.value); $event.target.value=''">
      <option disabled selected>Select all eligible branches</option>

      <option v-for="branch in ALL_BRANCHES" :key="branch" :value="branch">
        {{ branch }}
      </option>
     </select>

     <div class="mb-3">
      <span v-for="branch in selectedBranches" :key="branch" class="badge bg-primary me-2 p-2">
        {{ branch }}

        <button class="btn-close btn-close-white ms-2" style="font-size: 8px" @click="removeBranch(branch)"></button>
      </span>
     </div>

     <!-- Drive detauils -->
      <h6 class="mb-2">Drive details</h6>

      <label class="form-label">Start Date</label>
      <input type="datetime-local" class="form-control mb-2" v-model="start_date">

      <label class="form-label">Application deadline</label>
      <input type="datetime-local" v-model="deadline" class="form-control mb-2">

      <input type="number" class="form-control mb-2" v-model="openings_count" placeholder="Number of openings">

      <input v-model="bond_details" class="form-control mb-3" placeholder="Bond details (if any)">



      
      <button class="btn btn-success mb-5" @click="createDrive">Create Drive</button>

  </div>
</template>