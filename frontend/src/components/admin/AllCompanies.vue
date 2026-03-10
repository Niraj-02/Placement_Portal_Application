<script setup>
const props = defineProps({
  companies: Array
})

const emit = defineEmits(["view","blacklist"])
</script>

<template>

    <div class="col mt-5">
        <h4>Registered Companies</h4>
        <table class="table table-striped">

            <colgroup>
                <col style="width:60%">
                <col style="width:20%">
                <col style="width:20%">
                <col style="width:1%">
            </colgroup>

            <thead>
                <tr>
                    <th>Name</th>
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

                        <button class="btn btn-danger btn-sm" @click="emit('blacklist', company.id)">Blacklist</button>
                        </div>

                    </td>
                </tr>
            </tbody>
        </table>
    </div>
</template>