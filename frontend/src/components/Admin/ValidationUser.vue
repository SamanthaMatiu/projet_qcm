<template>
  <div class="container">
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
                  <button type="button" class="btn btn-success btn-sm" v-b-modal.validation-modal @click="validerEleve(user)">Valider</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteUser(user)">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div> 
  <b-modal ref="validationModal" id="validation-modal" title="Validation compte" hide-footer>
    <p class="my-4"><b>Nom :</b> {{ infosUser.nom}} </p>
    <p class="my-4"><b>Prénom :</b> {{ infosUser.prenom}} </p>
    <p class="my-4"><b>Mail :</b> {{ infosUser.mail}} </p>
    <p class="my-4"><b>Statut :</b> {{ infosUser.droit}} </p>
    <b-form @submit="onSubmitValidationEleve" class="w-100">
    <b-form-select v-if="infosUser.droit === 'Élève'" v-model="infosUser.groupe" class="mb-2">
      <b-form-select-option :value="null">Choisir un groupe</b-form-select-option>
      <b-form-select-option v-for="(option, index) in groupes" :key="index" v-bind:value="option.id_groupe">{{option.nom}}</b-form-select-option>
    </b-form-select>
    <b-button-group>
        <b-button type="submit" variant="primary">Valider</b-button>
    </b-button-group>
    </b-form>
  </b-modal>
  </div>
 
</template>

<script>
import axios from 'axios';

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
    validerEleve(user){
        this.infosUser=user;
    },
    setGroupe(payload, user_id) {
      const path = `http://localhost:5000/api/validation/${user_id}`;
      axios.patch(path, payload)
        .then(() => {
          this.getUsers();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitValidationEleve(evt) {
      evt.preventDefault();
      this.$refs.validationModal.hide();
      const user = {
        id_groupeutilisateur: this.infosUser.groupe,
      };
      this.setGroupe(user, this.infosUser.id_utilisateur);
      window.location.reload();
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
    this.getUsers();
    this.getGroups();
  },
};
</script>