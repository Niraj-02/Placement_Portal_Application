<script setup>
import { ref,onMounted } from 'vue';
import { useRouter } from 'vue-router';

const applications = ref([])
const router = useRouter()


async function getApplications(){
    const response = await fetch(
        "http://127.0.0.1:5000/api/application",
        {
            headers:{
                Authorization:"Bearer "+localStorage.getItem("token")
            }
        }
    )
    applications.value = await response.json()
}


function viewDrive(id){
    router.push(`/student/drive/${id}`)
}

onMounted(getApplications)

</script>


<template>
    <h4 class="mb-3">My Applications</h4>

    <table class="table table-striped">
        <thead>
            <tr>
                <td>Drive ID</td>
                <th>Status</th>
                <th>View</th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="app in applications" :key="app.id">
                <td>{{ app.placement_drive_id }}</td>
                <td>{{ app.status }}</td>

                <td>
                    <button class="btn btn-primary btn-sm" @click="viewDrive(app.placement_drive_id)">View</button>
                </td>
            </tr>
        </tbody>
    </table>



</template>