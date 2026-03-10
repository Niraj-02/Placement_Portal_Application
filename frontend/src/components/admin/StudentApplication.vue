<script setup>

const props = defineProps({
  applications: Array
})

const emit = defineEmits(["view","student"])

</script>

<template>

    <div class="col mt-5">

        <h4>Student Applications</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>Application ID</th>
                    <th>Student ID</th>
                    <th>Drive ID</th>
                    <th>Status</th>
                    <th>Applied At</th>
                    <th></th>
                </tr>
            </thead>

            <tbody class="table-group-divider">

                <tr v-for="app in applications" :key="app.id">

                    <td>{{ app.id }}</td>
                    <td>{{ app.student_id }}</td>
                    <td>{{ app.placement_drive_id }}</td>
                    <td> 
                        <span class="badge bg-info"> {{ app.status }} </span> 
                    </td>

                    <td>{{ app.applied_at }}</td>

                    <td>
                        <div class="d-flex">
                            <button class="btn btn-primary btn-sm me-2" @click="emit('view', app.id)">View</button>
                        </div>
                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</template>