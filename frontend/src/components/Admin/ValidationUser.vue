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
                  <button v-if="user.droit === 'élève'" type="button" class="btn btn-success btn-sm" v-b-modal.eleve-validation-modal @click="validerEleve(user)">Valider</button>
                  <button v-else type="button" class="btn btn-success btn-sm" >Valider</button>
                  <button type="button" class="btn btn-danger btn-sm">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div> 
  <b-modal id="eleve-validation-modal" title="Validation élève" hide-footer>
    <p class="my-4"><b>Nom :</b> {{ infosUser.id_utilisateur}} </p>
    <p class="my-4"><b>Nom :</b> {{ infosUser.nom}} </p>
    <p class="my-4"><b>Prénom :</b> {{ infosUser.prenom}} </p>
    <p class="my-4"><b>Mail :</b> {{ infosUser.mail}} </p>
    <p class="my-4"><b>Statut :</b> {{ infosUser.droit}} </p>
    <b-form @submit="onSubmitValidationEleve" class="w-100">
    <b-form-select v-model="infosUser.groupe" class="mb-2">
      <b-form-select-option :value="null">Choisir un groupe</b-form-select-option>
      <b-form-select-option v-for="(option, index) in groupes" :key="index" v-bind:value="option.id_groupe">{{option.nom}}</b-form-select-option>
    </b-form-select>
    <p class="my-4">Selected: {{ infosUser.groupe }}</p>
    <b-button-group>
        <b-button type="submit" variant="primary">Valider</b-button>
    </b-button-group>
    </b-form>
  </b-modal>
  </div>
 
</template>

<script>
import axios from 'axios';
//import router from '../router';

export default {
  data() {
    return {
      usersAValider: [],
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
      const path = `http://localhost:5000/api/validation`;
      axios.get(path)
        .then((res) => {
          this.usersAValider = res.data['data'];
          console.log(res.data['message']);
          console.log(this.usersAValider);
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
          console.log(res.data['message']);
          console.log(this.groupes);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    validerEleve(user){
        this.infosUser=user;
    },
    setGroupe(payload, user_id) {
      const path = `http://localhost:5000/api/validation/${user_id}`;
      axios.patch(path, payload)
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitValidationEleve(evt) {
      evt.preventDefault();
      const user = {
        id_groupeutilisateur: this.infosUser.groupe,
      };
      this.setGroupe(user, this.infosUser.id_utilisateur);
    },
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