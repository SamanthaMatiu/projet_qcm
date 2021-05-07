<template>
  <div class="container">
    <br><br>
    <div class="row">
      <div class="col-sm-10">
        <h2>Tous les groupes</h2>
        <hr><br><br>
        <table class="table table-hover">
          <tbody>
            <tr v-for="(groupe, index) in groupes" :key="index">
              <td>{{ groupe.nom }}</td>
              <td>
                <div class="btn-group" role="group">
                  <button type="button" class="btn btn-warning btn-sm" v-b-modal.modif-groupe-modal @click="getInfosGroupe(groupe)">Modifier</button>
                  <button type="button" class="btn btn-danger btn-sm" @click="onDeleteGroup(groupe)">Supprimer</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
        <br><br>
        <button type="button" class="btn btn-success btn-sm" v-b-modal.ajout-groupe-modal>Ajouter un groupe</button>
      </div>
    </div>
    <b-modal ref="ajoutGroupeModal"
            id="ajout-groupe-modal"
            title="Créer un groupe"
            hide-footer>
      <b-form @submit="onSubmit" class="w-100">
      <b-form-group id="form-name-group"
                    label="Nom du groupe :"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="ajoutGroupeForm.nomgroupe"
                        required>
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Ajouter</b-button>
        </b-button-group>
      </b-form>
    </b-modal>

    <b-modal ref="modifGroupeModal"
            id="modif-groupe-modal"
            title="Modifier groupe"
            hide-footer>
      <b-form @submit="onSubmitModifGroupe" class="w-100">
      <b-form-group id="form-name-group"
                    label="Nom du groupe :"
                    label-for="form-name-input">
          <b-form-input id="form-name-input"
                        type="text"
                        v-model="infosGroupe.nom"
                        required>
          </b-form-input>
        </b-form-group>
        <b-button-group>
          <b-button type="submit" variant="primary">Modifier</b-button>
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
      groupes: [],
      ajoutGroupeForm: {
        nomgroupe: '',
      },
      infosGroupe : {}
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
    onSubmit(evt) {
      evt.preventDefault();
      this.$refs.ajoutGroupeModal.hide();
      const payload = {
        nomgroupe: this.ajoutGroupeForm.nomgroupe,
      };
      this.ajoutGroupe(payload);
      this.ajoutGroupeForm.nomgroupe = '';
    },
    ajoutGroupe(payload) {
      const path = 'http://localhost:5000/api/groupes';
      axios.post(path, payload)
        .then(() => {
          this.getGroups();
        })
        .catch((error) => {
          console.log(error);
        });
    },
    removeGroup(group_id) {
      const path = `http://localhost:5000/api/groupes/${group_id}`;
      axios.delete(path)
        .then(() => {
          this.getGroups();
        })
        .catch((error) => {
          console.error(error);
          this.getGroups();
        });
    },
    onDeleteGroup(groupe) {
      this.removeGroup(groupe.id_groupe);
    },
    getInfosGroupe(group){
      this.infosGroupe=group;
    },
    setNomGroupe(payload, group_id) {
      const path = `http://localhost:5000/api/groupes/${group_id}`;
      axios.patch(path, payload)
        .then(() => {
          this.getGroups();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitModifGroupe(evt) {
      evt.preventDefault();
      this.$refs.modifGroupeModal.hide();
      const groupe = {
        nom_groupe: this.infosGroupe.nom,
      };
      this.setNomGroupe(groupe, this.infosGroupe.id_groupe);
      window.location.reload();
    }
  },
  created() {
    this.getGroups();
  },
};
</script>