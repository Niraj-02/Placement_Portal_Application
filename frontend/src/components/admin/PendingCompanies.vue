<script setup>

const props = defineProps({
  companies: Array
})

const emit = defineEmits(["view","approve","reject"])

</script>

<template>

    <div class="col mt-5">

        <h4>Company Applications</h4>

        <table class="table table-striped">

            <thead>
                <tr>
                    <th>Company Name</th>
                    <th>Industry</th>
                    <th>Status</th>
                    <th></th>
                </tr>
            </thead>

            <tbody class="table-group-divider">

                <tr v-for="company in companies" :key="company.id">

                    <td>{{ company.company_name }}</td>
                    <td>{{ company.industry }}</td>
                    <td>{{ company.status }}</td>

                <td>

                <div class="d-flex">
                <button class="btn btn-primary btn-sm me-2" @click="emit('view', company.id)">View</button>
                <button class="btn btn-success btn-sm me-2" @click="emit('approve', company.id)">Approve</button>
                <button class="btn btn-danger btn-sm" @click="emit('reject', company.id)">Reject</button>
                </div>
                </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>