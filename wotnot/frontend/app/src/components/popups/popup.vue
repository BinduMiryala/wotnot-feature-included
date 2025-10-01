<template>
    <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-5 z-[10000] text-left shadow-lg">
      <div class="bg-[#ffffff] p-6 rounded-md w-[1000px]  relative max-h-[750px]">
        <div class="flex ">
          <span class="close" @click="$emit('close')" hover>&times;</span> 
        </div>
          
        <slot/>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'PopUp'
  }
  </script>
  
  <style scoped>
.close{

  margin-left: auto;
  font-size: 25px;
  cursor: pointer;
}
</style>