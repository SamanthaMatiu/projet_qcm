<template>
  <div class="row">
    <div class="col-1">
      <router-link :to="{ name: 'Consultation'}">
        <i class="retour fas fa-arrow-circle-left fa-2x"></i>
      </router-link>
    </div>
    <div class="col-11 center-tab">
      <div class="card text-center">
        <div class="card-header">Titre</div>
        <div class="card-body">
          <p>
            A faire
          </p>
        </div>
        <div class="card-footer text-muted">
          <button type="button" class="btn btn-primary btn-sm">Modifier</button>
          <button type="button" class="btn btn-danger btn-sm">Supprimer</button>
        </div>
      </div>  
    </div>
  </div>
</template>

<script>
  import axios from 'axios';

export default {
  name: 'DetailQcm',
  methods: {
    getQcm(){
      const path = `http://localhost:5000/api/qcm/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getQcm()
  }
}
</script>

<style scoped lang="scss">

  .card-footer {
    text-align: right;  
  }

  .retour {
    color: #3f51b5;
  }

  .center-tab {
    max-width: 80%;
    left: 4%;
  }

  thead {
    background-color: #d5deff;
  }

  .tableau {
    text-align: center;
    width: 70%;
  }
</style>
