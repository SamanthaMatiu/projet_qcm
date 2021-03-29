<template>
  <div class="container">
    <!--button type="button" class="btn btn-dark btn-sm" @click="logout()">Deconnexion</button-->
    <br><br>
    <div class="row">
      <div class="col-sm-10">
        <h2>A valider</h2>
        <hr><br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col"><b>Nom</b></th>
              <th scope="col"><b>Prénom</b></th>
              <th scope="col"><b>Mail</b></th>
              <th scope="col"><b>Statut</b></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in usersAValider" :key="index">
              <td>{{ user.nom }}</td>
              <td>{{ user.prenom }}</td>
              <td>{{ user.mail }}</td>
              <td>{{ user.droit }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Valider</button>
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
      usersAValider: [],
    };
  },
  methods: {
    getUsers() {
      const path = `http://localhost:5000/api/validation`;
      axios.get(path)
        .then((res) => {
          this.usersAValider = res.data['data'];
          console.log(res.data['message']);
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
    this.getUsers();
  },
};
</script>