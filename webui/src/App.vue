<script>
</script>

<template>
  <div id="app">  
    <router-view v-slot="{Component}">
      <transition name="slide">
        <component :is="Component" />
      </transition>
    </router-view>
  </div>
</template>

<style scoped>
  .slide-enter-from{
    transform: translateX(-100%);
  }

  .slide-enter-to {
    transform: translateX(0);
  }

  .slide-enter-active,
  .slide-leave-active {
    transition: all 1s ease-in-out;
  }

  .slide-left-leave-from {
    transform: translateX(0);
  }

  .slide-leave-to{
    transform: translateX(100%)
  }
</style>
<style scoped>
  body {
    background: #F0F8FF;
  }
  

</style>

