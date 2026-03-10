<script setup>

const props = defineProps({
    students: Array
})

const emit = defineEmits(["view", "blacklist"])
</script>

<template>
    <div class="col mt-5">
      <!-- Registered Studentss-->
       <div class="col">
        <h4>Registered Students</h4>

        <table class="table table-striped">

            <colgroup>
              <col style="width: 60%">
              <col style="width: 30%">
              <col style="width: 10%">
              <col style="width: 1%">
            </colgroup>

          <thead>
            <tr>
              <th>Student Name</th>
              <th>Branch</th>
              <th>CGPA</th>
              <th></th>
            </tr>
          </thead>

          <tbody class="table-group-divider">
            <tr v-for="student in students" :key="student.id">

              <td>{{ student.name }}</td>
              <td>{{ student.branch }}</td>
              <td>{{ student.cgpa }}</td>

              <td>
                <div class="d-flex">
                  <button class="btn btn-primary btn-sm me-2" @click="emit('view', student.id)">View</button>
                  <button class="btn btn-danger btn-sm me-2" @click="emit('blacklist', student.id)">Blacklist</button>
                </div>                
              </td>
            </tr>
          </tbody>
        </table>
       </div>
    </div>
</template>