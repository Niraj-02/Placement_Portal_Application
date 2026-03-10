<template>
    <div class="container-fluid mt-5">
        <div class="row justify-content-center">
            <div class="col-6 mb-5"> 
                <h1 class="text-center mb-4">Student Registration</h1>
                <form v-on:submit.prevent="registerStudent">

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

                    <!-- student name -->
                    <div class="mb-3">
                        <label class="form-label">Student Name</label>
                        <input type="text" class="form-control" v-model="studentName">
                    </div>

                    <!-- branch -->
                    <div class="mb-3">
                    <label class="form-label">Branch</label>

                    <select class="form-select" v-model="branch">

                        <option disabled value="">Select Branch</option>

                        <option>Computer Science</option>
                        <option>Information Technology</option>
                        <option>Data Science</option>
                        <option>Electronics and Communication</option>
                        <option>Electrical Engineering</option>
                        <option>Mechanical Engineering</option>
                        <option>Civil Engineering</option>
                        <option>Chemical Engineering</option>
                        <option>Metallurgical Engineering</option>

                    </select>

                    </div>

                    <!-- cgpa -->
                    <div class="mb-3">
                        <label class="form-label">CGPA</label>
                        <input type="number" class="form-control" v-model="cgpa" min="0" max="10" step="any">
                    </div>

                    <!-- year of passing -->
                    <div class="mb-3">
                        <label class="form-label">Year of Passing</label>
                        <input type="text" class="form-control" v-model="yearOfPassing">
                    </div>

                    <!-- skills -->
                    <div class="mb-3">
                        <label class="form-label">Skills</label>
                        <input type="text" class="form-control" v-model="skills">
                    </div>

                    <!-- resume -->
                    <div class="mb-3">
                        <label class="form-label">Upload resume (PDF)</label>
                        <input type="file" class="form-control" @change="onFileChange">
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
const studentName = ref('');
const branch = ref('');
const cgpa = ref('');
const yearOfPassing = ref('');
const skills = ref('');
const resume = ref(null);


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

function onFileChange(event) {
    resume.value = event.target.files[0]

}


async function registerStudent() {
    if (!validatePassword()){
        alert('Invalid Password length')
        return;
    }

    if (email.value === '' || password.value === '' || studentName.value === '' || branch.value === '' || cgpa.value === '' || yearOfPassing.value === '' || skills.value === '' || !resume.value) {
        alert('Please fill in all fields');
        return;
    }

    const formData = new FormData();
    formData.append('email', email.value);
    formData.append('password', password.value);
    formData.append('name', studentName.value);
    formData.append('branch', branch.value);
    formData.append('cgpa', cgpa.value);
    formData.append('year_of_passing', yearOfPassing.value);
    formData.append('skills', skills.value);
    formData.append('resume', resume.value);


    try {
        const response = await fetch('http://localhost:5000/api/register/student', {
            method: 'POST',
            
            body: formData
        });

        const data = await response.json()

        console.log(data)
        console.log(response)

        if (!response.ok) {
            alert(data.message || 'Something went wrong! Please try again.');
        } else {
            alert('Registration successful! Please login to continue.');
            router.push('/')
            return;
        }

    } catch (error) {
        console.error(error)
    }
}
</script>