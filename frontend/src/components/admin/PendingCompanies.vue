<script setup>

const props = defineProps({
  applications: Array
})

const emit = defineEmits(["view","accept","reject"])

</script>

<template>

    <div class="col mt-5">

        <h4>Company Applications</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>Company</th>
                    <th>Drive</th>
                    <th>Date</th>
                    <th></th>
                </tr>
            </thead>

            <tbody class="table-group-divider">

                <tr v-for="app in applications" :key="app.id">

                    <td>{{ app.company_name }}</td>
                    <td>{{ app.drive_name }}</td>
                    <td>{{ app.created_at }}</td>

                <td>

                <div class="d-flex">
                <button class="btn btn-primary btn-sm me-2" @click="emit('view', app.id)">View</button>
                <button class="btn btn-success btn-sm me-2" @click="emit('accept', app.id)">Accept</button>
                <button class="btn btn-danger btn-sm" @click="emit('reject', app.id)">Reject</button>
                </div>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>