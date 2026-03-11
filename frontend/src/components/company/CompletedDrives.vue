<script setup>

import { ref, onMounted} from 'vue'
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

    drives.value = data.filter(d => d.hiring_status === "completed")

}

async function openModal(drive) {
    
    selectedDrive.value = drive

    const modal = new bootstrap.Modal(  document.getElementById("driveModal"))
    modal.show()
}


function viewStudents(id){
    router.push(`/company/drive/${id}/applications`)
}

onMounted(getDrives)

</script>



<template>

    <h5 class="mb-3">Completed Drives</h5>

    <div v-if="drives.length === 0">
        <p class="text-muted">No completed drives</p>
    </div>

    <div class="table-responsive" style="max-height: 400px; overflow-y:auto;">

        <table class="table table-bordered table-hover">
            <thead class="table-light sticky-top">
                <tr>
                    <th>ID</th>
                    <th>Job Title</th>
                    <th>Location</th>
                    <th>Deadline</th>
                    <th>Actions</th>
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
                            <button class="btn btn-outline-info me-2" @click="openModal(drive)">View Drive</button>
                            <button class="btn btn-outline-primary" @click="viewStudents(drive.id)">View Students</button>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>



<!-- modal  -->
    <div class="modal fade" id="driveModal" tabindex="-1">

        <div class="modal-dialog modal-lg">

            <div class="modal-content">

                <div class="modal-header">
                    <h5 class="modal-title">Drive Details</h5>
                    <button class="btn-close" data-bs-dismiss="modal"></button>
                </div>

                <div class="modal-body" >
                    <div v-if="selectedDrive">
                        <p><strong>Job Title:</strong> {{ selectedDrive.job_title }}</p>

                        <p><strong>Description:</strong> {{ selectedDrive.job_description }}</p>

                        <p><strong>Salary:</strong> {{ selectedDrive.salary }}</p>

                        <p><strong>Location:</strong> {{ selectedDrive.location }}</p>

                        <p><strong>Eligible Branches:</strong> {{ selectedDrive.eligible_branches }}</p>

                        <p><strong>Minimum CGPA:</strong> {{ selectedDrive.min_cgpa }}</p>

                        <p><strong>Skills Required:</strong> {{ selectedDrive.skills_required }}</p>

                        <p>
                        <strong>Application Deadline:</strong>
                        {{ new Date(selectedDrive.application_deadline).toLocaleString() }}
                        </p>
                    </div>

                </div>

            </div>
        </div>
    </div>

</template>