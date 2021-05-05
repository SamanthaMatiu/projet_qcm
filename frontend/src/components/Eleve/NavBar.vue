<template>
  <div>
    <mdb-navbar position="top" dark color="indigo" scrolling>
      <mdb-navbar-brand to="/dashboardEleve/home">QCM - Bolamano</mdb-navbar-brand>
      <mdb-navbar-toggler>
        <mdb-navbar-nav>
          <mdb-nav-item to="/dashboardEleve/home" waves-fixed>Home</mdb-nav-item>
          <mdb-nav-item to="/dashboardEleve/afaire" waves-fixed>A faire</mdb-nav-item>
          <mdb-nav-item to="/dashboardEleve/fait" waves-fixed>En cours de correction</mdb-nav-item>
          <mdb-nav-item to="/dashboardEleve/corriges" waves-fixed>Corrigés</mdb-nav-item>
        </mdb-navbar-nav>
        <mdb-form-inline>
        <mdb-btn outline="success" type="button" @click="logout()">Déconnexion</mdb-btn>
        </mdb-form-inline>
      </mdb-navbar-toggler>
    </mdb-navbar>
    
  </div>
</template>

<script>
  import {
    mdbNavbar,
    mdbNavItem,
    mdbNavbarNav,
    mdbNavbarToggler,
    mdbNavbarBrand,
    mdbBtn, mdbFormInline
  } from "mdbvue";
  import router from '../../router';

  export default {
    name: "Navbar",
    components: {
      mdbNavbar,
      mdbNavItem,
      mdbNavbarNav,
      mdbNavbarToggler,
      mdbNavbarBrand,
      mdbBtn, mdbFormInline
    },
    props: {
        navElements: Array
    },
    data() {
      return {
      };
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('statut');
        router.push({ name: "Connexion", params: {}});
      },
    },
    created() {
      if (!(localStorage.getItem('token'))){
        router.push({ name: "Connexion", params: {}});
      }
      if (!((localStorage.getItem('statut')==="Élève") || (localStorage.getItem('statut')==="élève"))){
        localStorage.removeItem('token');
        localStorage.removeItem('statut');
        router.push({ name: "Connexion", params: {}});
      }
    },
  };
  </script>

  <style scoped>
  .view {
    background: url("https://mdbootstrap.com/img/Photos/Others/img (50).jpg")
      no-repeat center center;
    background-size: cover;
    height: 100%;
  }

  .navbar .dropdown-menu a:hover {
    color: inherit !important;
  }
  .btn-outline-success {
    border: 2px solid white !important;
    background-color: transparent !important;
    color: white !important;
} 
 .btn-outline-success:not([disabled]):not(.disabled):active {
    border-color: white !important;
}
</style>