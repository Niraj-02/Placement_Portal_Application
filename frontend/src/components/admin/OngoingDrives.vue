<script setup>

const props = defineProps({
  drives: Array
})

const emit = defineEmits(["view"])

</script>

<template>

    <div class="col mt-5">

        <h4>Ongoing Drives</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>Drive Name</th>
                    <th>Company</th>
                    <th>Status</th>
                    <th></th>
                </tr>
            </thead>
            <tbody class="table-group-divider">
                <tr v-for="drive in drives" :key="drive.id">

                    <td>{{ drive.job_title }}</td>
                    <td>{{ drive.company_id }}</td>
                    <td>{{ drive.status }}</td>

                    <td>
                    <button class="btn btn-primary btn-sm" @click="emit('view', drive.id)">View</button>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>