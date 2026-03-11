<script setup>

import { ref, onMounted } from 'vue'

const drives = ref([])
const selectedDrive = ref(null)

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


async function openModal(drives){
    selectedDrive.value = drives

    const modal = new bootstrap.Modal(
        document.getElementById("driveModal")
    )
    modal.show()
}


onMounted(getDrives)

</script>


<template>

    <h5 class="mb-3">Pending Approval Drives</h5>

    <div v-if="drives.length === 0">
        <p class="text-muted">No pending drives</p>
    </div>

    <div class="table-responsive" style="max-height:400px; overflow-y: auto;">
        <table class="table table-bordered table-hover">
            <thead class="table-light sticky-top">
                <tr>
                    <th>ID</th>
                    <th>Job Title</th>
                    <th>Location</th>
                    <th>Deadline</th>
                    <th>Status</th>
                    <th>Hiring status</th>
                    <th></th>
                </tr>
            </thead>

            <tbody>
                <tr v-for="drive in drives" :key="drive.id">
                    <td>{{ drive.id }}</td>
                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.location }}</td>
                    <td>{{ new Date(drive.application_deadline).toLocaleDateString() }}</td>
                    <td>{{ drive.status }}</td>
                    <td>{{ drive.hiring_status }}</td>
                    <td>
                        <button class="btn btn-sm btn-primary" @click="openModal(drive)">View</button>
                    </td>
                    
                    <!-- <td><span class="badge bg-warning">Pending</span></td> -->
                </tr>
            </tbody>
        </table>
    </div>



    <!-- MODAL -->

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

                    <p><strong>Application Deadline:</strong> 
                    {{ new Date(selectedDrive.application_deadline).toLocaleString() }}
                    </p>

                </div>

            </div>
        </div>

    </div>
</template>