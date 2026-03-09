<template>
    <div class="container-fluid mt-5">
        <div class="row justify-content-center">
            <div class="col-6"> 
                <h1 class="text-center mb-4">Login</h1>
                <form v-on:submit.prevent="loginUser">
                    <div class="mb-3">
                        <label for="exampleInputEmail1" class="form-label">Email address</label>
                        <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp" v-model="email">
                        <div id="emailHelp" class="form-text">We'll never share your email with anyone else.</div>
                    </div>
                    <div class="mb-3">
                        <label for="exampleInputPassword1" class="form-label">Password</label>
                        <input type="password" class="form-control" id="exampleInputPassword1" v-model="password" @input="validatePassword">
                        <div id="passwordlHelp" class="form-text">{{ passwordError }}</div>
                    </div>                   
                    <button type="submit" class="btn btn-primary">Submit</button>
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

async function loginUser() {
    if (!validatePassword()){
        alert('Invalid Password length')
        return;
    }

    if (email.value === '' || password.value === '') {
        alert('Please fill in all fields');
        return;
    }

    const user = {
        email: email.value,
        password: password.value
    }

    try {
        const response = await fetch('http://localhost:5000/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(user)
        });

        const data = await response.json()

        // console.log(data)
        console.log(response)

        if (!response.ok) {
            alert(data.message || 'An error occurred while logging in');
        } else {
            localStorage.setItem('token', data.access_token);
            alert('Login successful');

            if (data.role === 'admin') {
                router.push('/admin_dashboard');

            } else if (data.role === 'student') {
                router.push('/student_dashboard');
            } else if (data.role === 'company') {
                router.push('/company_dashboard');
            } else {
                alert('Unknown user role');
            }
            return;
        }

    } catch (error) {
        console.error(error)
    }
}
</script>