<template>
  <div class="container">
    <br><br>
    <div class="row">
      <div class="col-sm-10">
        <h2>Tous les groupes</h2>
        <hr><br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Nom</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(groupe, index) in groupes" :key="index">
              <td>{{ groupe.nom }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Modifier</button>
                  <button type="button" class="btn btn-danger btn-sm">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
 
</template>

<script>
import axios from 'axios';
//import router from '../router';

export default {
  data() {
    return {
      groupes: [],
    };
  },
  methods: {
    getGroups() {
      const path = `http://localhost:5000/api/groupes`;
      axios.get(path)
        .then((res) => {
          this.groupes = res.data['data'];
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    //if (!(localStorage.getItem('token'))){
    //  router.push({ name: "Connexion", params: {}});
    //}
    this.getGroups();
  },
};
</script>