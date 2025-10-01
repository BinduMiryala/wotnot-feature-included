<template>
  <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-5 z-[10000] text-left shadow-lg">
    <div class="bg-[#ffffff]  p-6 rounded-md">
      <div class="flex">
        <span class="close" @click="$emit('close')">&times;</span>  
      </div>
 
      <slot/>
    </div>
  </div>


</template>

<script>
export default {
  name: 'PopUpSmall'
}
</script>

<style scoped>


.close{

  margin-left: auto;
  font-size: 25px;
  cursor: pointer;
}
.action-buttons {
  display: flex; /* Align buttons side by side */
  gap: 10px; /* Space between buttons */
}

.action-buttons button {
  padding: 10px;
  border: none;
  border-radius: 4px;
  background-color: #007bff; /* Button background color */
  color: white; /* Button text color */
  cursor: pointer;
  flex: 1; /* Make buttons fill available space evenly */
}

.action-buttons button:last-child {
  background-color: #dc3545; /* Different color for delete button */
}
</style>
