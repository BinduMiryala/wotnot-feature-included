<template>
  <div class="fixed inset-0 bg-black bg-opacity-20 flex justify-center items-center p-3 z-[10000]"
  @click.self="$emit('close')">
    <div class="phone-frame relative flex flex-col items-center justify-start p-4">
      <div class="w-full flex justify-end px-2 pt-2">
        <!-- <span class="close" @click="$emit('close')">&times;</span> -->
      </div>
      <div class="screen w-full h-max-[60vh] overflow-y-auto ">
        <slot />
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'PopUp_preview'
}
</script>

<style scoped>
.phone-frame {
  width: 390px;
  height: 750px;
  background-color: #3b3b3b;
  border-radius: 40px;
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.3);
  border: 6px solid #2d2d2d;
}

.screen {
  flex-grow: 1;
  border-radius: 10px;
  margin-top: 20px;
}

.close {
  font-size: 24px;
  color: white;
  cursor: pointer;
}
</style>
