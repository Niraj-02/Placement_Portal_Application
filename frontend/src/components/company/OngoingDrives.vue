<script setup>

import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drives = ref([])
const selectedDrive = ref(null)

async function getDrives(){
    const res = await fetch("http://127.0.0.1:5000/api/drives",{
        headers:{
            Authorization:"Bearer "+localStorage.getItem("token")
        }
    })

    const data = await res.json()

    drives.value = data.filter(d => d.hiring_status === "ongoing" && d.status === "approved")
}

function openModal(drive){
  selectedDrive.value = drive

  const modal = new bootstrap.Modal(
    document.getElementById("driveModal")
  )

  modal.show()
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

  <h5 class="mb-3">Ongoing Drives</h5>

    <div v-if="drives.length === 0">
        <p class="text-muted">No ongoing drives</p>
    </div>

    <div class="table-responsive" style="max-height:400px; overflow-y: auto;">
        <table class="table table-bordered table-hover">
            <thead class="table-light sticky-top">
                <tr>
                    <th>ID</th>
                    <th>Job Title</th>
                    <th>Location</th>
                    <th>Deadline</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.location }}</td>
                    <td>{{ new Date(drive.application_deadline).toLocaleDateString() }}</td>
                    <td>
                      <div class="d-flex">
                        <button class="btn btn-outline-info me-2" @click="openModal(drive)"> View drive details</button>
                        <button class="btn btn-outline-primary me-2" @click="viewApplications(drive.id)">View Applications</button>
                        <button class="btn btn-outline-danger me-2" @click="markComplete(drive.id)">Mark Complete</button>
                      </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>


    <!-- Modal -->

<div class="modal fade" id="driveModal" tabindex="-1">

  <div class="modal-dialog modal-lg">
    <div class="modal-content">

      <div class="modal-header">
        <h5 class="modal-title">Drive Details</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <div class="modal-body" v-if="selectedDrive">

        <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>

        <p><strong>Description:</strong> {{ selectedDrive.job_description }}</p>

        <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>

        <p><strong>Location:</strong> {{ selectedDrive.location }}</p>

        <p><strong>Eligible Branches:</strong> {{ selectedDrive.eligible_branches }}</p>

        <p><strong>Minimum CGPA:</strong> {{ selectedDrive.min_cgpa }}</p>

        <p><strong>Eligibility:</strong> {{ selectedDrive.eligibility_criteria }}</p>

        <p><strong>Skills Required:</strong> {{ selectedDrive.skills_required }}</p>

        <p>
          <strong>Application Deadline:</strong>
          {{ new Date(selectedDrive.application_deadline).toLocaleString() }}
        </p>

      </div>

    </div>
  </div>

</div>

</template>