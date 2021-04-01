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
              <th></th>
              <th scope="col">Nom</th>
              <th scope="col">Prénom</th>
              <th scope="col">Mail</th>
              <th scope="col">Statut</th>
              <th scope="col">Groupe</th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, index) in users" :key="index">
              <td><input type="checkbox" :id="user.id_utilisateur" :value="user.id_utilisateur" v-model="selected"></td>
              <td>{{ user.nom }}</td>
              <td>{{ user.prenom }}</td>
              <td>{{ user.mail }}</td>
              <td>{{ user.droit }}</td>
              <td>{{ user.nom_groupe }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.modif-groupe-modal @click="getInfosEleve(user)">Modifier groupe</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteUser(user)">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.select-modal>Modifier groupe de la sélection</button>
      </div>
    </div>

    <b-modal ref="modifGroupeModal" id="modif-groupe-modal" title="Modification du groupe" hide-footer>
      <p class="my-4"><b>Nom :</b> {{ infosUser.nom}} </p>
      <p class="my-4"><b>Prénom :</b> {{ infosUser.prenom}} </p>
      <p class="my-4"><b>Mail :</b> {{ infosUser.mail}} </p>
      <p class="my-4"><b>Statut :</b> {{ infosUser.droit}} </p>
      <b-form @submit="onSubmitModifGroupe" class="w-100">
      <b-form-select v-model="infosUser.groupe" class="mb-2">
        <b-form-select-option :value="null">Choisir un groupe</b-form-select-option>
        <b-form-select-option v-for="(option, index) in groupes" :key="index" v-bind:value="option.id_groupe">{{option.nom}}</b-form-select-option>
      </b-form-select>
      <b-button-group>
        <b-button type="submit" variant="primary">Valider</b-button>
      </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="selectModal" id="select-modal" title="Choisir groupe" hide-footer>
      <p class="my-4"><b>Selected :</b> {{ selected}} </p>
    </b-modal>
  </div>
 
</template>

<script>
import axios from 'axios';
//import router from '../router';

export default {
  data() {
    return {
      selected: [],
      users: [],
      groupes: [],
      infosUser : {
        nom: '',
        prenom: '',
        mail: '',
        droit: '',
        groupe: '',
        id_utilisateur: ''
      }
    };
  },
  methods: {
    getUsers() {
      const path = `http://localhost:5000/api/utilisateursvalides`;
      axios.get(path)
        .then((res) => {
          this.users = res.data['data'];
          console.log(res.data['message']);
        })
        .catch((error) => {
          console.error(error);
        });
    },
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
    getInfosEleve(user){
      this.infosUser=user;
    },
    setGroupe(payload, user_id) {
      const path = `http://localhost:5000/api/groupesutilisateurs/${user_id}`;
      axios.patch(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitModifGroupe(evt) {
      evt.preventDefault();
      this.$refs.modifGroupeModal.hide();
      const user = {
        groupe_id: this.infosUser.groupe,
      };
      this.setGroupe(user, this.infosUser.id_utilisateur);
    }
  },
  created() {
    //if (!(localStorage.getItem('token'))){
    //  router.push({ name: "Connexion", params: {}});
    //}
    this.getUsers();
    this.getGroups();
  },
};
</script>