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
          
          <mdb-row class="">
            <mdb-col col="4">
              <p>Date : {{this.affichage.date}}</p> 
            </mdb-col>
            <mdb-col col="8">
              à faire de {{this.affichage.time.debut}} jusqu'à {{this.affichage.time.fin}}  
            </mdb-col>
          </mdb-row>

          <div>
            <b-tabs content-class="mt-3">
              <!-- Question ouverte -->
              <b-tab title="Questions ouverte" active>
                <div>
                  <label class="grey-text ajout-quest">Ajouter une question</label> 
                  <i class="fas fa-plus-circle" v-on:click="$bvModal.show('modal-creer-ouverte')"></i>

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

              <!-- Question à choix multiple -->
              <b-tab title="Questions à choix multiples">
                <div>
                  <label class="grey-text ajout-quest">Ajouter une question</label> 
                  <i class="fas fa-plus-circle" v-on:click="$bvModal.show('modal-creer-mult')"></i>

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
                            <i v-on:click="prepModifierMult(question)" class="fas fa-pen"></i>
                            <i v-on:click="prepSupprimer(question.id)" class="fas fa-trash"></i>
                          </td>
                        </template>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </b-tab>

              <!-- Droit -->
              <b-tab title="Droit">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Elève</th>
                      <th scope="col">Groupe</th>
                      <th width="35px" scope="col">#</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="eleve in data.id_eleves" :key="eleve.id">
                      <template>
                        <td>{{ eleve.nom }} {{ eleve.prenom }}</td>                       
                        <td>{{ eleve.groupe }}</td>  
                        <td>
                          <i class="fas fa-trash" @click="prepSuprDroit(eleve.id)"></i>
                        </td>
                      </template>
                    </tr>
                  </tbody>
                </table>
              </b-tab>
            </b-tabs>
          </div>

        </div>
        <div class="card-footer text-muted">
          <button type="button" class="btn btn-primary btn-sm" @click="prepModifQcm()">Modifier</button>
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

          <!-- Pop up modifier une question à choix multiple -->
          <b-modal id="modal-modif-mult" hide-footer>
            <template #modal-title>
              Modification d'une question à choix multiples
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="titreQO">Question</label>
                </div>
                <div class="row">
                  <textarea id="titreQO" v-model="modifMult.question" cols="48"/>
                </div>
              </div>

              <div class="form-label">
                <label for="typeNumber">Barème</label>
                <input label="Barème" type="number" id="typeNumber" class="form-control" v-model="modifMult.bareme" min="1" required/>
              </div>

              <!-- Réponse -->
              <div class="text-reponse">
                <div class="row">
                  <label for="titre-reponse">Réponse</label>
                </div>
                <div class="row">
                  <div id="titre-reponse">
                    <div v-for="choix in modifMult.choix" :key="choix.id">
                      <div class="form-check">
                        <input
                          class="form-check-input"
                          type="checkbox"
                          value="oui"
                          id="form2Example3"
                          v-model="choix.true"
                        />
                        <label class="form-check-label" for="form2Example3">Est-ce une bonne réponse ?</label>
                      </div>
                      <textarea v-model="choix.choix" cols="48"/>
                    </div>
                  </div>
                </div>
              </div>
              
              
            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="modifierMult()">Modifier</b-button>
              <b-button variant="secondary" @click="initModifMult()">Annuler</b-button>
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
              

              <label for="date-time">Date et Horaire</label>
              <div id="date-time" class="row date">
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

              <label class="label-drop" for="dropdown">Ajouter un groupe ou un élève ?</label> 
              <div id="dropdown" class="row dropdown"> 
                <div class="col">
                  <multiselect v-model="droit.valueGroupe" :options="droit.groupes" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="groupe(s)" label="nom" track-by="nom" :preselect-first="false">
                    <template slot="selection" slot-scope="{ values, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} groupe(s) selectionné</span></template>
                  </multiselect>
                </div>
                <div class="col">
                  <multiselect v-model="droit.valueUser" :options="droit.utilisateur" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="élève(s)" label="nom" track-by="nom" :preselect-first="false">
                    <template slot="selection" slot-scope="{ values, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} élève(s) selectionné</span></template>
                  </multiselect>
                </div>
              </div>

            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="modifierQcm()">Modifier</b-button>
              <b-button variant="secondary" @click="annuleModifQcm()">Annuler</b-button>
            </div>
          </b-modal>

          <!-- Pop up creer une question ouverte -->
          <b-modal id="modal-creer-ouverte" hide-footer>
            <template #modal-title>
              Création d'une question ouverte
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="titreQO">Question</label>
                </div>
                <div class="row">
                  <textarea id="titreQO" v-model="creerOuverte.question" cols="48"/>
                </div>
              </div>

              <div class="form-label">
                <label for="typeNumber">Barème</label>
                <input label="Barème" type="number" id="typeNumber" class="form-control" v-model="creerOuverte.bareme" min="1" required/>
              </div>
            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="creerQuestOuverte()">Ajouter</b-button>
              <b-button variant="secondary" @click="initOuvert()">Annuler</b-button>
            </div>
          </b-modal>

          <!-- Pop up creer une question mult -->
          <b-modal id="modal-creer-mult" hide-footer>
            <template #modal-title>
              Création d'une question à choix multiples
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="titreQO">Question</label>
                </div>
                <div class="row">
                  <textarea id="titreQO" v-model="creerMult.question" cols="48"/>
                </div>
              </div>

              <div class="form-label">
                <label for="typeNumber">Barème</label>
                <input label="Barème" type="number" id="typeNumber" class="form-control" v-model="creerMult.bareme" min="1" required/>
              </div>
              
              <div class="ajout-choix">
                <label class="grey-text">Ajouter un choix</label> 
                <i class="fas fa-plus-circle" v-on:click="$bvModal.show('modal-creer-choix')"></i>
              </div>

              <div v-if="creerMult.choix.length > 0">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Choix</th>
                      <th width="150px" scope="col">Bonne réponse ?</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="choix in creerMult.choix" :key="choix.id">
                      <td>
                        {{ choix.choix }}
                      </td>
                      <td v-if="choix.true == 1">
                        Oui
                      </td>
                      <td v-if="choix.true == 0">
                        Non
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="creerQuestMult()">Ajouter</b-button>
              <b-button variant="secondary" @click="initMult()">Annuler</b-button>
            </div>
          </b-modal>

          <!-- Pop up creer un choix -->
          <b-modal id="modal-creer-choix" hide-footer>
            <template #modal-title>
              Création d'un choix
            </template>
            <div class="text-center-modal">
              <div class="modif-ouv-titre">
                <div class="row">
                  <label for="choix">Choix</label>
                </div>
                <div class="row">
                  <textarea id="choix" v-model="creerChoix.choix" cols="48"/>
                </div>
              </div>

              <div class="form-check">
                <input
                  class="form-check-input"
                  type="checkbox"
                  value="oui"
                  id="form2Example3"
                  v-model="creerChoix.estBonneReponse"
                />
                <label class="form-check-label" for="form2Example3">Est-ce une bonne réponse ?</label>

              </div>
            </div>
            <div class="modifOuverte">
              <b-button variant="primary" @click="creeChoix()">Ajouter</b-button>
              <b-button variant="secondary" @click="initChoix()">Annuler</b-button>
            </div>
          </b-modal>

          <!-- Pop up supprimer droit -->
          <b-modal id="modal-suppr-droit" hide-footer>
            <template #modal-title>
              Suppression d'un élève pour ce QCM
            </template>
            <div class="text-center-modal">
              Une fois supprimé, cet élève n'aurra plus accès à ce QCM.
            </div>
            <div class="supprDroit">
              <b-button variant="danger" @click="supprimerDroit()">Supprimer</b-button>
              <b-button variant="primary" @click="initSupprDroit()">Annuler</b-button>
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
  import Multiselect from 'vue-multiselect'
  import VueTimepicker from 'vue2-timepicker/dist/VueTimepicker.common.js'

export default {
  name: 'DetailQcm',
  components: {
    mdbRow,
    mdbCol,
    VueTimepicker,
    Multiselect
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
        },
        droit: {
          groupe: "",
          utilisateur: ""
        }
      },
      modifOuverte: {
        question: "",
        bareme: ""
      },
      modifMult: {
        question: "",
        bareme: "",
        choix: []
      },
      creerOuverte: {
        question: "",
        bareme: ""
      },
      creerMult: {
        question: "",
        bareme: "",
        choix:[]
      },
      creerChoix: {
        choix: "",
        estBonneReponse: ""
      },
      idQuestion: "",
      idDroit: -1,
      droit: {
          groupes: [],
          utilisateur: [],
          valueGroupe: [],
          valueUser: []
        },
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
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getGroupe(){
      const path = `http://localhost:5000/api/groupes`;
      axios.get(path)
        // eslint-disable-next-line no-unused-vars
        .then((res) => {
          this.droit.groupes = res.data.data
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getUser(){
      const path = `http://localhost:5000/api/elevesvalides`;
      axios.get(path)
        // eslint-disable-next-line no-unused-vars
        .then((res) => {
          this.droit.utilisateur = res.data.data
        })
        .catch((error) => {
          console.log(error);
        });
    },
    getDroit(list){
        let droit
        
        if (list.length <= 0){
          droit = ""
        } else {
          droit = []
          for(let i=0 ; i<=list.length-1 ; i++){

            if(list[i].id_utilisateur){
              const item = {
                id: list[i].id_utilisateur
              }
              droit.push(item)
            }

            if(list[i].id_groupe){
              const item = {
                id: list[i].id_groupe
              }
              droit.push(item)
            }
            
          }
        }
        
        return droit
      },
    modifierQcm(){
      if(this.affichage.titre != this.modifQcm.titre){
        this.modifQcm.titre = this.affichage.titre
      } else {
        this.modifQcm.titre = ""
      }

      if(this.affichage.date != this.modifQcm.date){
        this.modifQcm.date = this.affichage.date
      }

      if(this.affichage.time.debut != this.modifQcm.time.debut){
        this.modifQcm.time.debut = this.affichage.time.debut
      }

      if(this.affichage.time.fin != this.modifQcm.time.fin){
        this.modifQcm.time.fin = this.affichage.time.fin
      }

      this.modifQcm.droit.groupe = this.getDroit(this.droit.valueGroupe)
      this.modifQcm.droit.utilisateur = this.getDroit(this.droit.valueUser)
     // const d = JSON.parse(JSON.stringify(this.modifQcm.droit))

      const q = {
        id: this.data.id,
        titre: this.modifQcm.titre,
        date_debut: this.getDateDebut(),
        date_fin: this.getDateFin(),
        droit: JSON.parse(JSON.stringify(this.modifQcm.droit)),
        questions: "",
        choix: ""
      }

      const path = `http://localhost:5000/api/qcm`;
      axios.patch(path, q)
        .then((res) => {
          console.log(res)
          this.$bvModal.hide('modal-modif-qcm')
          this.$router.go(0);
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    modifierQuestion(data){
      const path = `http://localhost:5000/api/ModifQuestions/${this.idQuestion}`;
      axios.patch(path, data)
        .then((res) => {
          console.log(res)
          this.initModifOuverte()
          this.initModifMult()
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
    modifierMult(){
      const q = {
        question: {
          titre: this.modifMult.question,
          ouverte: false,
          bareme: this.modifMult.bareme,
        },
        choix: this.modifMult.choix
      }

     this.modifierQuestion(q)
    },
    creerQuestion(data) {
      const path = `http://localhost:5000/api/creationQuestions`;
        axios.post(path, data)
          // eslint-disable-next-line no-unused-vars
          .then((res) => {
            this.$router.go(0);
            this.initOuvert()
            this.initMult()
          })
          .catch((error) => {
            console.log(error);
          });
    },
    creerQuestOuverte(){
      const q = {
        id_qcm: this.data.id,
        question: {
          titre: this.creerOuverte.question,
          ouverte: 1,
          bareme: this.creerOuverte.bareme,
          choix: "",
        }
      }

      this.creerQuestion(q)
    },
    creerQuestMult(){
      const q = {
        id_qcm: this.data.id,
        question: {
          titre: this.creerMult.question,
          ouverte: 0,
          bareme: this.creerMult.bareme,
          choix: JSON.parse(JSON.stringify(this.creerMult.choix)),
        }
      }

console.log(q)
      this.creerQuestion(q)
    },
    creeChoix(){
      let estBonneReponse
      if(this.creerChoix.estBonneReponse) {
        estBonneReponse = 1
      } else {
        estBonneReponse = 0
      }
      
      const c = 
      {
        choix: this.creerChoix.choix,
        true: estBonneReponse
      }

      this.creerMult.choix.push(c)
      this.initChoix()
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
    supprimerDroit(){
      const path = `http://localhost:5000/api/retraitDroits/${this.data.id}/${this.idDroit}`;
      axios.delete(path)
        .then((res) => {
          this.initSupprDroit()
          this.$router.go(0)
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
      this.modifQcm.titre = ""
      this.modifQcm.date = ""
      this.modifQcm.time.debut = ""
      this.modifQcm.time.fin = ""

      this.droit.valueGroupe = []
      this.droit.valueUser = []

      this.$bvModal.hide('modal-modif-qcm')
    },
    initModifOuverte(){
      this.idQuestion = "",
      this.modifOuverte.question = "",
      this.modifOuverte.bareme = ""
      this.$bvModal.hide('modal-modif-ouverte')
    },
    initModifMult(){
      this.idQuestion = "",
      this.modifMult.question = "",
      this.modifMult.bareme = ""
      this.$bvModal.hide('modal-modif-mult')
    },
    initOuvert(){
      this.creerOuverte.question = ""
      this.creerOuverte.bareme = ""

      this.$bvModal.hide('modal-creer-ouverte')
    },
    initMult(){
      this.creerMult.question = ""
      this.creerMult.bareme = ""
      this.creerMult.choix = []

      this.$bvModal.hide('modal-creer-mult')
    },
    initChoix(){
      this.creerChoix.choix = ""
      this.creerChoix.estBonneReponse = ""

      this.$bvModal.hide('modal-creer-choix')
    },
    initSupprDroit(){
      this.idDroit = -1
      this.$bvModal.hide('modal-suppr-droit')
    },
    annuleModifQcm(){
      this.affichage.titre = this.modifQcm.titre 
      this.affichage.date = this.modifQcm.date
      this.affichage.time.debut = this.modifQcm.time.debut 
      this.affichage.time.fin = this.modifQcm.time.fin 
      this.initModifQcm()
    }, 
    prepSupprimer(id){
      this.idQuestion = id
      this.$bvModal.show('modal-suppr-quest')
    },
    prepModifQcm(){
      this.modifQcm.titre = this.affichage.titre
      this.modifQcm.date = this.affichage.date
      this.modifQcm.time.debut = this.affichage.time.debut
      this.modifQcm.time.fin = this.affichage.time.fin

      this.$bvModal.show('modal-modif-qcm')
    },
    prepModifierOuverte(question){
      this.idQuestion = question.id,
      this.modifOuverte.question = question.titre,
      this.modifOuverte.bareme = question.bareme

      this.$bvModal.show('modal-modif-ouverte')
    },
    prepModifierMult(question){
      this.idQuestion = question.id,
      this.modifMult.question = question.titre,
      this.modifMult.bareme = question.bareme,
      this.modifMult.choix = question.choix

      this.$bvModal.show('modal-modif-mult')
    },
    prepSuprDroit(id){
      this.idDroit = id
      this.$bvModal.show('modal-suppr-droit')
    },
    getDateDebut(){
      let date = this.modifQcm.date + " " + this.modifQcm.time.debut + ":00"
      return date
    },
    getDateFin(){
      let date = this.modifQcm.date + " " + this.modifQcm.time.fin + ":00"
      return date
    },
  },
  created() {
    this.getQcm()
    this.getGroupe()
    this.getUser()
  }
}
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style src="vue2-timepicker/dist/VueTimepicker.css"></style>

<style scoped lang="scss">

  .label-drop {
    margin-top: 20px;
  }

  .ajout-choix {
    text-align: center;
    margin-top: 25px;
  }

  .ajout-quest {
    margin-bottom: 20px;
  }

  .fa-plus-circle {
    margin-left: 10px;
  }

  .text-reponse {
    margin-top: 20px;
    margin-left: 15px;
  }

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

  .supprDroit {
    position: relative;
    left: 180px;
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
