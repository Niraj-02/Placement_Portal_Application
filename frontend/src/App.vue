<script setup>
import { RouterLink, RouterView, useRouter, useRoute } from 'vue-router';
import { ref, onMounted, watch } from 'vue';

const router = useRouter()
const route = useRoute()
const role = ref(null)

// Function to sync role from local storage
const updateRole = () => {
  role.value = localStorage.getItem("role")
}

// Update role on initial load
onMounted(updateRole)

// Watch for route changes to update the navbar (handles login/logout transitions)
watch(() => route.path, updateRole)

function logout() {
  localStorage.removeItem("token")
  localStorage.removeItem("role")
  localStorage.removeItem("myID") // Clean up ID as well
  updateRole()
  router.push("/login")
}
</script>

<template>
  <div class="container-fluid"> 
    <nav class="navbar navbar-expand-lg bg-body-tertiary">
      <div class="container-fluid">
        <RouterLink class="navbar-brand" to="/">Placebo</RouterLink>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
          <ul class="navbar-nav me-auto mb-2 mb-lg-0">

            <template v-if="!role">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/login">Login</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/student_registration">Student Registration</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/company_registration">Company Registration</RouterLink>
              </li>
            </template>

            <template v-if="role === 'admin'">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/admin_dashboard">Dashboard</RouterLink>
              </li>
            </template>

            <template v-if="role === 'company'">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/company_dashboard">Dashboard</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/company_edit_profile">Edit Profile</RouterLink>
              </li>
            </template>

            <template v-if="role === 'student'">
              <li class="nav-item">
                <RouterLink class="nav-link" to="/student_dashboard">Dashboard</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/student_edit_profile">Edit Profile</RouterLink>
              </li>
              <li class="nav-item">
                <RouterLink class="nav-link" to="/student_history">History</RouterLink>
              </li>
            </template>

            <li v-if="role" class="nav-item">
              <button class="nav-link btn btn-link" @click="logout" style="text-decoration: none;">
                Logout
              </button>
            </li>
          </ul>

          <form v-if="role === 'admin'" class="d-flex" role="search">
            <input class="form-control me-2" type="search" placeholder="Search"/>
            <button class="btn btn-outline-success" type="submit">Search</button>
          </form>
        </div>
      </div>
    </nav>

    <RouterView/>
  </div>  
</template>