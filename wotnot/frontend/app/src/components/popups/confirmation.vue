<template>
    
  <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-5 z-[10000] text-left shadow-lg">
    <div class="bg-white p-6 rounded-md w-full max-w-md relative">
        <div class="flex">
            <span class="close" @click="$emit('close')" hover>&times;</span> 
        
        </div>
      
      <!-- Confirmation Message -->
      <div class="text-lg font-medium text-gray-800 mb-6">
        Are you sure you want to proceed?
      </div>

      <!-- Action Buttons -->
      <div class="flex justify-end gap-4">
        <button
          class="px-4 py-2 bg-gray-300 text-gray-800 rounded hover:bg-gray-400"
          @click="$emit('no')"
        >
          No
        </button>
        <button
          class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          @click="$emit('yes')"
        >
          Yes
        </button>
      </div>
    </div>
  </div>
  
</template>

<script>
export default {
  name: 'ConfirmationPopup',
}
</script>

<style scoped>
.close{

  margin-left: auto;
  font-size: 25px;
  cursor: pointer;
}
</style>
