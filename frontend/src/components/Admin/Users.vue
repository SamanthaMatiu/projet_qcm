<template>
  <div class="container">
    <br><br>
    <div class="row">
      <div class="col-sm-10">
        <h2>Tous les utilisateurs</h2>
        <hr><br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">Nom</th>
              <th scope="col">Prénom</th>
              <th scope="col">Mail</th>
              <th scope="col">Statut</th>
              <th scope="col">Groupe</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in usersAValider" :key="index">
              <td>{{ user.nom }}</td>
              <td>{{ user.prenom }}</td>
              <td>{{ user.mail }}</td>
              <td>{{ user.droit }}</td>
              <td>{{ user.nom_groupe }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm">Modifier groupe</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteUser(user)">Supprimer</button>
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
      const path = `http://localhost:5000/api/utilisateursvalides`;
      axios.get(path)
        .then((res) => {
          this.usersAValider = res.data['data'];
          console.log(res.data['message']);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    removeUser(user_id) {
      const path = `http://localhost:5000/api/validation/${user_id}`;
      axios.delete(path)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
          this.getUsers();
        });
    },
    onDeleteUser(user) {
      this.removeUser(user.id_utilisateur);
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