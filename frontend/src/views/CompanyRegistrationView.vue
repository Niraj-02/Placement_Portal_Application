<template>
    <div class="container-fluid mt-5">
        <div class="row justify-content-center">
            <div class="col-6 mb-5"> 
                <h1 class="text-center mb-4">Company Registration</h1>
                <form v-on:submit.prevent="registerCompany">
                    <!-- Email -->
                    <div class="mb-3">
                        <label class="form-label">Email address</label>
                        <input type="email" class="form-control" v-model="email">
                    </div>

                    <!-- password  -->
                    <div class="mb-3">
                        <label class="form-label">Password</label>
                        <input type="password" class="form-control" v-model="password" @input="validatePassword">
                        <div class="form-text">{{ passwordError }}</div>
                    </div>

                    <!-- company name -->
                    <div class="mb-3">
                        <label class="form-label">Company name</label>
                        <input type="text" class="form-control" v-model="companyName">
                    </div>

                    <!-- industry -->
                    <div class="mb-3">
                        <label class="form-label">Industry</label>
                        <input type="text" class="form-control" v-model="industry">
                    </div> 

                    <!-- description -->
                    <div class="mb-3">
                        <label class="form-label">Company description</label>
                        <textarea class="form-control" rows="3" v-model="companyDescription"></textarea>
                    </div>

                    <!-- hr_name  -->
                    <div class="mb-3">
                        <label class="form-label">HR Name</label>
                        <input type="text" class="form-control" v-model="hrName">
                    </div>

                    <!-- hr_email -->
                    <div class="mb-3">
                        <label class="form-label">HR Email</label>
                        <input type="email" class="form-control" v-model="hrEmail">
                    </div>

                    <!-- website  -->
                    <div class="mb-3">
                        <label class="form-label">Website</label>
                        <input type="text" class="form-control" v-model="website">
                    </div>

                    <!-- company location -->
                    <div class="mb-3">
                        <label class="form-label">Company Location</label>
                        <input type="text" class="form-control" v-model="companyLocation">
                    </div>

                    <button type="submit" class="btn btn-primary">Register</button>
                </form>
            </div>
        </div>        
    </div>
</template>

<script setup>
import {ref} from 'vue';
import { useRouter } from 'vue-router'

const router = useRouter()

const email = ref('');
const password = ref('');
const companyName = ref('');
const industry = ref('');
const companyDescription = ref('');
const hrName = ref('');
const hrEmail = ref('');
const website = ref('');
const companyLocation = ref('');

const passwordError = ref('');

const validatePassword = () => {
    if (password.value.length < 6) {
        passwordError.value = 'Password must be at least 6 characters long';
        return false;
    } else {
        passwordError.value = '';
        return true;
    }
}

async function registerCompany() {
    if (!validatePassword()){
        alert('Invalid Password length')
        return;
    }

    if (email.value === '' || password.value === '' || companyName.value === '' || industry.value === '' || companyDescription.value === '' || hrName.value === '' || hrEmail.value === '' || website.value === '' || companyLocation.value === '') {
        alert('Please fill in all fields');
        return;
    }

    const company = {
        email: email.value,
        password: password.value,
        company_name: companyName.value,
        industry: industry.value,
        description: companyDescription.value,
        hr_name: hrName.value,
        hr_email: hrEmail.value,
        website: website.value,
        location: companyLocation.value
    }

    try {
        const response = await fetch('http://localhost:5000/api/register/company', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(company)
        });

        const data = await response.json()

        console.log(data)
        console.log(response)

        if (!response.ok) {
            alert(data.message || 'Something went wrong! Please try again.');
        } else {
            alert('Company registration successful! Please wait for admin approval.');
            router.push('/')
            return;
        }

    } catch (error) {
        console.error(error)
    }
}
</script>