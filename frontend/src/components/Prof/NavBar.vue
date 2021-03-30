<template>
  <div>
    <mdb-navbar position="top" dark color="indigo" scrolling>
      <mdb-navbar-brand to="/dashboardProf/home">QCM - Bolamano</mdb-navbar-brand>
      <mdb-navbar-toggler>
        <mdb-navbar-nav>
          <mdb-nav-item to="/dashboardProf/home" waves-fixed>Home</mdb-nav-item>
          <mdb-nav-item to="/dashboardProf/creation" waves-fixed>Création</mdb-nav-item>
          <mdb-nav-item to="/dashboardProf/consultation" waves-fixed>Mes QCMs</mdb-nav-item>
          <mdb-nav-item to="/dashboardProf/correction" waves-fixed>Correction</mdb-nav-item>
        </mdb-navbar-nav>
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
    mdbNavbarBrand
  } from "mdbvue";

  export default {
    name: "Navbar",
    components: {
      mdbNavbar,
      mdbNavItem,
      mdbNavbarNav,
      mdbNavbarToggler,
      mdbNavbarBrand
    },
    props: {
        navElements: Array
    }
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
  </style>