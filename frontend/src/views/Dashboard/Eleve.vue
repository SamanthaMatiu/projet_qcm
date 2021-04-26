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

import Navbar from '@/components/Eleve/NavBar.vue'

export default {
  name: 'Eleve',
  components: {
    Navbar
  }
}
</script>

<style scoped>
  .page {
    margin-top: 90px;
  }
</style>