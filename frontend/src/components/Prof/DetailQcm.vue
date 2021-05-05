<template>
  <div class="row">
    <div class="col-1">
      <router-link :to="{ name: 'Consultation'}">
        <i class="retour fas fa-arrow-circle-left fa-2x"></i>
      </router-link>
    </div>
    <div class="col-11">
      <div class="card text-center">
        <div class="card-header">{{affichage.titre}}</div>
        <div class="card-body">
          
          <mdb-row class="time">
            <mdb-col col="4">
              <p>Date : {{this.affichage.date}}</p> 
            </mdb-col>
            <mdb-col col="8">
              à faire de {{this.affichage.time.debut}} jusqu'à {{this.affichage.time.fin}}  
            </mdb-col>
          </mdb-row>

          <div>
            <b-tabs content-class="mt-3">
              <b-tab title="Questions ouverte" active>
                <div>
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th scope="col">Barème</th>
                        <th scope="col">Question</th>
                        <th width="70px" scope="col">#</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="question in data.questions" :key="question.id">
                        <template v-if="question.ouverte">
                        <td>{{ question.bareme }}</td>
                        <td>{{ question.titre }}</td>
                        <td>
                          <i v-on:click="prepModifierOuverte(question)" class="fas fa-pen"></i>
                          <i v-on:click="prepSupprimer(question.id)" class="fas fa-trash"></i>
                        </td>
                        </template>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </b-tab>

              <b-tab title="Questions à choix multiples">
                <div>
                  <table class="table table-hover">
                    <thead>
                      <tr>
                        <th scope="col">Barème</th>
                        <th scope="col">Question</th>
                        <th scope="col">Réponse</th>
                        <th width="70px" scope="col">#</th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="question in data.questions" :key="question.id">
                        <template v-if="!question.ouverte">
                          <td>{{ question.bareme }}</td>
                          <td>{{ question.titre }}</td>
                          <td>
                            <template v-for="choix in question.choix">
                              - {{ choix.choix }} 
                            </template>
                          </td>                          
                          <td>
                            <i class="fas fa-pen"></i>
                            <i v-on:click="prepSupprimer(question.id)" class="fas fa-trash"></i>
                          </td>
                        </template>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </b-tab>
            </b-tabs>
          </div>

        </div>
        <div class="card-footer text-muted">
          <button type="button" class="btn btn-primary btn-sm" @click="$bvModal.show('modal-modif-qcm')">Modifier</button>
          <button type="button" class="btn btn-danger btn-sm" @click="$bvModal.show('bv-modal-example')">Supprimer</button>
        
        <!-- Pop up supprimer qcm -->
          <b-modal id="bv-modal-example" hide-footer>
            <template #modal-title>
              Suppression d'un qcm
            </template>
            <div class="text-center-modal">
              Etes-vous sur de vouloir supprimer ce qcm ?
            </div>
            <div class="suppr">
              <b-button variant="danger" @click="supprimerQcm()">Oui</b-button>
              <b-button variant="primary" @click="$bvModal.hide('bv-modal-example')">Non</b-button>
            </div>
          </b-modal>

          <!-- Pop up supprimer question -->
          <b-modal id="modal-suppr-quest" hide-footer>
            <template #modal-title>
              Suppression question
            </template>
            <div class="text-center-modal">
              Etes-vous sur de vouloir supprimer cette question ?
            </div>
            <div class="suppr">
              <b-button variant="danger" @click="supprimerQuestion()">Oui</b-button>
              <b-button variant="primary" @click="initSupprQuest()">Non</b-button>
            </div>
          </b-modal>

          <!-- Pop up modifier une question ouverte -->
          <b-modal id="modal-modif-ouverte" hide-footer>
            <template #modal-title>
              Modification d'une question ouverte
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="titreQO">Question</label>
                </div>
                <div class="row">
                  <textarea id="titreQO" v-model="modifOuverte.question" cols="48"/>
                </div>
              </div>

              <div class="form-label">
                <label for="typeNumber">Barème</label>
                <input label="Barème" type="number" id="typeNumber" class="form-control" v-model="modifOuverte.bareme" min="1" required/>
              </div>
            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="modifierOuverte()">Modifier</b-button>
              <b-button variant="secondary" @click="initModifOuverte()">Annuler</b-button>
            </div>
          </b-modal>

          <!-- Pop up modifier un qcm -->
          <b-modal id="modal-modif-qcm" hide-footer>
            <template #modal-title>
              Modification information qcm
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="titre-qcm">Titre</label>
                </div>
                <div class="row">
                  <input id="titre-qcm" type="text" v-model="affichage.titre" rows="60"/>
                </div>
              </div>
              
              <div class="row date">
                <div classe="col-6">
                  <input label="" type="date" v-model="affichage.date" required/>
                </div>
                <div class="col6">

                  <div class="row time">
                    <div class="col-6 col-lg-8">
                        <vue-timepicker placeholder="Heure deb" :minute-interval="5" hide-disabled-hours :hour-range="[[8, 19]]" input-width="102px" v-model="affichage.time.debut"></vue-timepicker>
                    </div>
                    <div class="col-6 col-lg-4">
                      <vue-timepicker placeholder="Heure fin" :minute-interval="5" hide-disabled-hours :hour-range="[[8, 20]]" input-width="102px" v-model="affichage.time.fin"></vue-timepicker>
                    </div>
                  </div>
                </div>
              </div>

            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="modifierQcm()">Modifier</b-button>
              <b-button variant="secondary" @click="initModifQcm()">Annuler</b-button>
            </div>
          </b-modal>
        </div>
      </div>  
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { mdbRow, mdbCol } from 'mdbvue';
  import VueTimepicker from 'vue2-timepicker/dist/VueTimepicker.common.js'

export default {
  name: 'DetailQcm',
  components: {
    mdbRow,
    mdbCol,
    VueTimepicker
  },
  data() {
    return {
      data: {},
      modal: {
        delete: false,
        modify: false
      },
      affichage: {
        titre: "",
        date: "",
        time: {
          debut: "",
          fin: ""
        }
      },
      modifQcm: {
        titre: "",
        date: "",
        time: {
          debut: "",
          fin: ""
        }
      },
      modifOuverte: {
        id: "",
        question: "",
        bareme: ""
      },
      idQuestion: ""
    }
  },
  methods: {
    getQcm(){
      const path = `http://localhost:5000/api/qcm/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.data = res.data
          this.affichage.titre = res.data.titre
          this.affichage.date = res.data.date_debut.slice(0,10)
          this.affichage.time.debut = res.data.date_debut.slice(11,16)
          this.affichage.time.fin = res.data.date_fin.slice(11,16)
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    modifierQcm(){
      const q = {
        id: this.data.id,
        titre: this.modifQcm.titre,
        date_debut: "",
        date_fin: "",
        droit: {
          groupe: "",
          utilisateur: ""
        },
        questions: "",
        choix: ""
      }

      const path = `http://localhost:5000/api/qcm`;
      axios.patch(path, q)
        .then((res) => {
          console.log(res)

          this.affichage.time = this.modifQcm.titre,
          this.affichage.date = this.modifQcm.date,
          this.affichage.time.debut = this.modifQcm.time.debut,
          this.affichage.time.fin = this.modifQcm.time.fin

          this.initModifQcm()
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    modifierQuestion(data){
      const path = `http://localhost:5000/api/ModifQuestions/${this.modifOuverte.id}`;
      axios.patch(path, data)
        .then((res) => {
          console.log(res)
          this.initModifOuverte()
          this.$router.go(0);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    modifierOuverte(){
      const q = {
        question: {
          titre: this.modifOuverte.question,
          ouverte: true,
          bareme: this.modifOuverte.bareme,
        },
        choix: ""
      }

      this.modifierQuestion(q)
    },
    supprimerQcm(){
      const path = `http://localhost:5000/api/qcm/${this.data.id}`;
      axios.delete(path)
        .then((res) => {
          this.$router.go(-1)
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    supprimerQuestion(){
      const path = `http://localhost:5000/api/ModifQuestions/${this.idQuestion}`;
      axios.delete(path)
        .then((res) => {
          this.initSupprQuest()
          this.$router.go(0);
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    initSupprQuest(){
      this.idQuestion = ""
      this.$bvModal.hide('modal-suppr-quest')
    },
    initModifQcm(){
      this.modifQcm.titre = "",
      this.modifQcm.date = "",
      this.modifQcm.time.debut = "",
      this.modifQcm.time.fin = "",

      this.$bvModal.hide('modal-modif-qcm')
    },
    initModifOuverte(){
      this.modifOuverte.id = "",
      this.modifOuverte.question = "",
      this.modifOuverte.bareme = ""
      this.$bvModal.hide('modal-modif-ouverte')
    },
    prepSupprimer(id){
      this.idQuestion = id
      this.$bvModal.show('modal-suppr-quest')
    },
    prepModifierQcm(){
      this.modifQcm.titre = this.affichage.titre,
      this.modifQcm.date = this.affichage.date,
      this.modifQcm.time.debut = this.affichage.time.debut,
      this.modifQcm.time.fin = this.affichage.time.fin,

      this.$bvModal.show('modal-modif-qcm')
    },
    prepModifierOuverte(question){
      this.modifOuverte.id = question.id,
      this.modifOuverte.question = question.titre,
      this.modifOuverte.bareme = question.bareme

      this.$bvModal.show('modal-modif-ouverte')
    }
  },
  created() {
    this.getQcm()
  }
}
</script>

<style src="vue2-timepicker/dist/VueTimepicker.css"></style>

<style scoped lang="scss">

  .row.time {
    margin-left: 15px;
  }

  .date {
    margin-left: 1px;
  }

  #titre-qcm {
    width: 450px;
  }

  .modif-ouv-titre {
    margin-left: 15px;
    margin-bottom: 15px;
  }

  .modifOuverte {
    position: relative;
    left: 180px;
  }

  .fas.fa-pen {
    margin-right: 8px;
  }

  .suppr {
    position: relative;
    left: 250px;
  }

  .text-center-modal{
    margin-bottom: 20px;
  }

  .text-center {
    max-width: 70%;
    left: 12%;
  }

  .card-footer {
    text-align: right;  
  }

  .retour {
    color: #3f51b5;
  }

  thead {
    background-color: #d5deff;
  }

  .tableau {
    text-align: center;
    width: 70%;
  }
</style>
