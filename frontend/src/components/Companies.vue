<script setup>

const companies = {
        name: 'Company C',
        description: 'Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.'
    }

</script>

<template> 
    <div class="container-fluid">
        <div class="row">
            <div class="col-9">
                <h7>{{companies.name}}</h7>
            </div>

            <div class="col-3">
                <button class="btn btn-danger">Blacklist</button>
                <!-- <button class="btn btn-primary">Delete</button> -->
            </div>
        </div>
    </div>
</template>