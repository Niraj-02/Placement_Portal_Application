<script setup>

import {ref,onMounted} from "vue"
import { useRouter } from "vue-router";

const companies = ref([])
const router = useRouter()

async function getCompanies() {
    const response = await fetch(
        "http://127.0.0.1:5000/api/companies",
        {
            headers:{
            Authorization:"Bearer "+localStorage.getItem("token")
        }
    })

    companies.value = await response.json()

}

function viewCompany(id){
    router.push(`/student/company/${id}`)
}

onMounted(getCompanies)

</script>

<template>
    <h4 class="mb-3">Organizations</h4>

    <table class="table table-striped">
        <thead>
            <tr>
                <th>Company Name</th>
                <th>Location</th>
                <th></th>
            </tr>
        </thead>

        <tbody>
            <tr v-for="company in companies" :key="company.id">
                <td>{{ company.company_name }}</td>
                <td>{{ company.location }}</td>

                <td>
                    <button class="btn btn-primary btn-sm" @click="viewCompany(company.id)">View</button>
                </td>
            </tr>
        </tbody>
    </table>
</template>