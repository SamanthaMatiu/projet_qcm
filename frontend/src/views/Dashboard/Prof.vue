<template>
  <div>
    <Navbar/>
    <div class="page">
      <router-view/>
    </div>
  </div>
</template>

<script>
/* eslint-disable vue/no-unused-components */

import Navbar from '@/components/Prof/NavBar.vue'
import Home from '@/components/Prof/Home.vue'

export default {
  name: 'Prof',
  components: {
    Navbar,
    Home
  }
}
</script>

<style scoped>
  .page {
    margin-top: 90px;
  }
</style>