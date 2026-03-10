<script setup>

const props = defineProps({
  drives: Array
})

const emit = defineEmits(["view","approve","reject"])

</script>

<template>

    <div class="col mt-5">

        <h4>Pending Drive Approvals</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>Drive</th>
                    <th>Company</th>
                    <th></th>
                </tr>
            </thead>

            <tbody class="table-group-divider">

                <tr v-for="drive in drives" :key="drive.id">

                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.company_name }}</td>

                    <td>
                        <div class="d-flex">
                            <button class="btn btn-primary btn-sm me-2" @click="emit('view', drive.id)">View</button>
                            <button class="btn btn-success btn-sm me-2" @click="emit('approve', drive.id)">Approve</button>
                            <button class="btn btn-danger btn-sm"@click="emit('reject', drive.id)">Reject</button>
                        </div>
                    </td>

                </tr>

            </tbody>

        </table>

    </div>

</template>