<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

import AllCompanies from '@/components/admin/AllCompanies.vue'
import RegisteredStudents from '@/components/admin/RegisteredStudents.vue'
import OngoingDrives from '@/components/admin/OngoingDrives.vue'
import PendingDrives from '@/components/admin/PendingDrives.vue'
import StudentApplication from '@/components/admin/StudentApplication.vue'
import PendingCompanies from '@/components/admin/PendingCompanies.vue'


const allCompanies = ref([])
const allStudents = ref([])
const pendingDrives = ref([])
const ongoingDrives = ref([])
const pendingCompanies = ref([])
const studentApplications = ref([])

const selectedCompany = ref(null)
const selectedStudent = ref(null)
const selectedDrive = ref(null)
const selectedApplication = ref(null)

// Company Functions

// Fetching all companies 
async function getAllCompanies(){
  const response = await fetch(
    "http://127.0.0.1:5000/api/companies",
    {
    headers : { Authorization: "Bearer "+localStorage.getItem("token") }
    })
    const data = await response.json()

    allCompanies.value = data
    pendingCompanies.value = data.filter(d => d.status === "pending")
  }   

// approving companies 
async function approveCompany(id){
  await fetch(
    `http://127.0.0.1:5000/api/companies/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body: JSON.stringify({
        status:"approved"
      })
    }
  )

  getPendingCompanies()
  getAllCompanies()
  }

// rejecting companies 
async function rejectCompany(id){
  await fetch(
    `http://127.0.0.1:5000/api/companies/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body: JSON.stringify({
        status:"rejected"
      })
    }
  )

  getPendingCompanies()
}

// post blacklist api 
async function blacklistCompany(id){
  await fetch(`http://127.0.0.1:5000/api/companies/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization: "Bearer "+localStorage.getItem("token")
      },
      body : JSON.stringify({
        blacklist:true
    })
  })
  // To refresh the companies list 
  getAllCompanies() 
}

// fetching id specific company 
async function viewCompany(id){

  const response = await fetch(
    `http://127.0.0.1:5000/api/companies/${id}`,
    {
    headers:{
    Authorization:"Bearer "+localStorage.getItem("token")
    }
    })

  selectedCompany.value = await response.json()

  const modal = new bootstrap.Modal(document.getElementById('companyModal'))
  modal.show()

}

// Student function 

// Fetching all studtens 
async function getAllStudents(){
  const response = await fetch (
    "http://127.0.0.1:5000/api/students",
    {
      headers:{ Authorization: "Bearer "+localStorage.getItem("token") }
    }
  )
  const data = await response.json()

  allStudents.value = data
  studentApplications.value = data.filter(d => d.status === "pending")
}

// Blackilisting students 
async function blacklistStudent(id){
  await fetch(`http://127.0.0.1:5000/api/students/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type":"application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body : JSON.stringify({
        blacklist:true
    })
  })
  // To refresh the students list 
  getAllStudents() 
}

// Fetching id specific student 
async function viewStudent(id){

  const response = await fetch(
    `http://127.0.0.1:5000/api/students/${id}`,
    {
    headers:{
    Authorization:"Bearer "+localStorage.getItem("token")
    }
    })

  selectedStudent.value = await response.json()

  const modal = new bootstrap.Modal(document.getElementById('studentModal'))
  modal.show()

}


// Placement Drive related functions

// Fetching all drives 
async function getAllDrives() {
  const response = await fetch(
    "http://127.0.0.1:5000/api/drives",
    {
      headers: { Authorization: "Bearer "+localStorage.getItem("token")  }
    }
  )
  const data = await response.json()

  pendingDrives.value = data.filter(d => d.status === "pending")
  ongoingDrives.value = data.filter(d => d.status === "approved")
}

// View drive function 
async function viewDrive(id){
  const response = await fetch(
    `http://127.0.0.1:5000/api/drives/${id}`,
    {
      headers:{ Authorization:"Bearer "+localStorage.getItem("token") }
    }
  )
  selectedDrive.value = await response.json()

  const modal = new bootstrap.Modal(document.getElementById('driveModal'))
  modal.show()
}

// Drive Approve function 
async function approveDrive(id){
  await fetch(
    `http://127.0.0.1:5000/api/drives/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type": "application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body: JSON.stringify({
        status:"approved"
      })
    })

    getAllDrives()
}
  

// Rejecting drive with id 
async function rejectDrive(id){
  await fetch(
    `http://127.0.0.1:5000/api/drives/${id}`,
    {
      method:"PATCH",
      headers:{
        "Content-Type": "application/json",
        Authorization:"Bearer "+localStorage.getItem("token")
      },
      body: JSON.stringify({
        status:"rejected"
      })
    })

    getAllDrives()
}
  

// Application related stuff 
async function getAllApplications(){
  const response = await fetch(
    "http://127.0.0.1:5000/api/application",
    {
      headers:{
        Authorization:"Bearer "+localStorage.getItem("token")
      }
    }
  )

  const data = await response.json()
  studentApplications.value = data
}

async function viewApplication(id){

  const response = await fetch(
    `http://127.0.0.1:5000/api/application/${id}`,
    {
      headers:{
        Authorization:"Bearer "+localStorage.getItem("token")
      }
    }
  )
  selectedApplication.value = await response.json()
  const modal = new bootstrap.Modal(document.getElementById('applicationModal'))
  modal.show()

}
const router = useRouter()
onMounted(()=>{

  const token = localStorage.getItem("token")
  if (!token) {
    // alert admin login is required to access admin dashboard
    alert("Admin Login required!!")
    router.push("/login")
  }

  getAllCompanies()
  getAllStudents()
  getAllDrives()
  getAllApplications()
})

</script>

<template>

  <div class="container mt-5">
    
    <!-- Companies Component -->
    <AllCompanies :companies="allCompanies"  @view="viewCompany"  @blacklist="blacklistCompany"/>


    <!-- Registered Students -->
     <RegisteredStudents :students="allStudents" @view="viewStudent" @blacklist="blacklistStudent" />


    <!-- Ongoing Drives -->
    <OngoingDrives :drives="ongoingDrives" @view="viewDrive" />

    <!-- pending drives -->
    <PendingDrives :drives="pendingDrives" @view="viewDrive" @approve="approveDrive" @reject="rejectDrive" />
    
    <!-- Pending Companies -->
    <PendingCompanies :companies="pendingCompanies" @view="viewCompany" @approve="approveCompany" @reject="rejectCompany" />

    <!-- Student applications lsit -->
    <StudentApplication :applications="studentApplications" @view="viewApplication"  />
  </div>


  <!-- Company view Modal -->
  <div class="modal fade" id="companyModal">
    <div class="modal-dialog modal-dialog-centered">

      <div class="modal-content">

        <div class="modal-header bg-info-subtle">
        <h5 class="modal-title">Company Details</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="selectedCompany">
          <table class="table table-borderless align-middle mb-0">
            <tbody>
              <tr>
              <td><strong>Name</strong></td>
              <td>{{ selectedCompany.name }}</td>
              </tr>

              <tr>
              <td><strong>Industry</strong></td>
              <td>{{ selectedCompany.industry }}</td>
              </tr>

              <tr>
              <td><strong>HR</strong></td>
              <td>{{ selectedCompany.hr_name }}</td>
              </tr>

              <tr>
              <td><strong>HR Email</strong></td>
              <td>{{ selectedCompany.hr_email }}</td>
              </tr>

              <tr>
              <td><strong>Company Email</strong></td>
              <td>{{ selectedCompany.email }}</td>
              </tr>

              <tr>
              <td><strong>Website</strong></td>
              <td>{{ selectedCompany.website }}</td>
              </tr>
            </tbody>
          </table>

        </div>

      </div>
    </div>
  </div>


  <!-- Drive modal -->
  
  <div class="modal fade" id="driveModal">
    <div class="modal-dialog modal-dialog-centered modal-lg">

      <div class="modal-content">
        <div class="modal-header bg-info-subtle">
          <h5 class="modal-title">Drive Details</h5>
          <button class="btn-close" data-bs-dismiss="modal"></button>
        </div>

        <div class="modal-body" v-if="selectedDrive">
          <table class="table table-borderless">

            <tbody>
              <tr>
                <td><strong>Job Title</strong></td>
                <td>{{ selectedDrive.job_title }}</td>
              </tr>

              <tr>
                <td><strong>Company ID</strong></td>
                <td>{{ selectedDrive.company_id }}</td>
              </tr>

              <tr>
                <td><strong>Salary</strong></td>
                <td>{{ selectedDrive.salary }}</td>
              </tr>

              <tr>
                <td><strong>Location</strong></td>
                <td>{{ selectedDrive.location }}</td>
              </tr>

              <tr>
                <td><strong>Status</strong></td>
                <td>{{ selectedDrive.status }}</td>
              </tr>

            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>


<!-- Student Modal -->
<!-- Student View Modal -->
<div class="modal fade" id="studentModal">
  <div class="modal-dialog modal-dialog-centered">

    <div class="modal-content">

      <div class="modal-header bg-info-subtle">
        <h5 class="modal-title">Student Details</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <div class="modal-body" v-if="selectedStudent">

        <table class="table table-borderless align-middle mb-0">
          <tbody>

            <tr>
              <td><strong>Name</strong></td>
              <td>{{ selectedStudent.name }}</td>
            </tr>

            <tr>
              <td><strong>Branch</strong></td>
              <td>{{ selectedStudent.branch }}</td>
            </tr>

            <tr>
              <td><strong>CGPA</strong></td>
              <td>{{ selectedStudent.cgpa }}</td>
            </tr>

            <tr>
              <td><strong>Year of Passing</strong></td>
              <td>{{ selectedStudent.year_of_passing }}</td>
            </tr>

            <tr>
              <td><strong>Skills</strong></td>
              <td>{{ selectedStudent.skills }}</td>
            </tr>

            <tr>
              <td><strong>Resume</strong></td>
              <td>
                <a
                  class="btn btn-primary btn-sm"
                  :href="'http://127.0.0.1:5000/resume_folder/' + selectedStudent.resume"
                  target="_blank"
                >
                  View Resume
                </a>
              </td>
            </tr>

            <tr>
              <td><strong>Blacklisted</strong></td>
              <td>
                <span v-if="selectedStudent.blacklist" class="badge bg-danger">
                  Yes
                </span>

                <span v-else class="badge bg-success">
                  No
                </span>
              </td>
            </tr>

          </tbody>
        </table>

      </div>

    </div>
  </div>
</div>


<!-- Application Modal -->
 <!-- Application View Modal -->
<div class="modal fade" id="applicationModal">
  <div class="modal-dialog modal-dialog-centered">

    <div class="modal-content">

      <div class="modal-header bg-info-subtle">
        <h5 class="modal-title">Application Details</h5>
        <button class="btn-close" data-bs-dismiss="modal"></button>
      </div>

      <div class="modal-body" v-if="selectedApplication">

        <table class="table table-borderless align-middle mb-0">
          <tbody>

            <tr>
              <td><strong>Application ID</strong></td>
              <td>{{ selectedApplication.id }}</td>
            </tr>

            <tr>
              <td><strong>Student ID</strong></td>
              <td>{{ selectedApplication.student_id }}</td>
            </tr>

            <tr>
              <td><strong>Drive ID</strong></td>
              <td>{{ selectedApplication.placement_drive_id }}</td>
            </tr>

            <tr>
              <td><strong>Status</strong></td>
              <td>
                <span class="badge bg-primary">
                  {{ selectedApplication.status }}
                </span>
              </td>
            </tr>

            <tr>
              <td><strong>Applied At</strong></td>
              <td>{{ selectedApplication.applied_at }}</td>
            </tr>

            <tr>
              <td><strong>Updated At</strong></td>
              <td>{{ selectedApplication.updated_at }}</td>
            </tr>

          </tbody>
        </table>

      </div>

    </div>
  </div>
</div>

</template>
