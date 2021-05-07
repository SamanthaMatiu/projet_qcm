<template>
  <section class="creer-qcm form-simple">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">Création de Qcm</h3>
            </mdb-row>
          </div>
          <mdb-card-body class="mx-4 mt-4">
            <form v-on:submit.prevent="onSubmit">
              <mdb-input label="Titre" type="text" v-model="qcmForm.titre" required/>

              <mdb-row>
                <mdb-col col="6">
                  <mdb-input label="" type="date" v-model="qcmForm.date" required/>
                </mdb-col>
                <mdb-col col="6">

                  <!-- Timepicker -->
                  <mdb-row class="time">
                    <mdb-col col="6 lg-8">
                        <vue-timepicker @click.native="verification.time = false" placeholder="Heure deb" :minute-interval="5" hide-disabled-hours :hour-range="[[8, 19]]" input-width="102px" v-model="qcmForm.time.debut" required></vue-timepicker>
                    </mdb-col>
                    <mdb-col col="6 lg-4">
                      <vue-timepicker @click.native="verification.time = false" placeholder="Heure fin" :minute-interval="5" hide-disabled-hours :hour-range="[[8, 20]]" input-width="102px" v-model="qcmForm.time.fin" required></vue-timepicker>
                    </mdb-col>
                  </mdb-row>
                </mdb-col>
              </mdb-row>
              
              <!-- Dropdown -->
              <label class="grey-text margetop">Pour qui est ce qcm ?</label> 
              <mdb-row class="dropdown"> 
                <mdb-col>
                  <multiselect v-model="droit.valueGroupe" :options="droit.groupes" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="groupe(s)" label="nom" track-by="nom" :preselect-first="true">
                    <template slot="selection" slot-scope="{ values, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} groupe(s) selectionné</span></template>
                  </multiselect>
                </mdb-col>
                <mdb-col>
                  <multiselect v-model="droit.valueUser" :options="droit.utilisateur" :multiple="true" :close-on-select="false" :clear-on-select="false" :preserve-search="true" placeholder="élève(s)" label="nom" track-by="nom" :preselect-first="true">
                    <template slot="selection" slot-scope="{ values, isOpen }"><span class="multiselect__single" v-if="values.length &amp;&amp; !isOpen">{{ values.length }} élève(s) selectionné</span></template>
                  </multiselect>
                </mdb-col>
              </mdb-row>

              <!-- Questions -->
              <label class="grey-text">Ajouter des questions</label> 
              <i class="fas fa-plus-circle" v-on:click="modal.question = true"></i>
              <div v-if="qcmForm.questions.length">
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Question</th>
                      <th scope="col">Type</th>
                      <th scope="col">#</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="question in qcmForm.questions" :key="question.id">
                      <td>{{ question.titre }}</td>
                      <td v-if="question.ouverte === 0">Choix multiples</td>
                      <td v-if="question.ouverte === 1">Ouverte</td>
                      <td v-if="question.ouverte === 2"> / </td>
                      <td>
                        <i v-if="question.ouverte === 0" class="fas fa-eye" v-on:click="getQuestChoixMult(question)"></i>
                        <i class="fas fa-trash" v-on:click="prepSupprQuest(question.id)"></i>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
              <div v-if="verification.question">
                <p class="unequest"> Un Qcm est composé d'au moins une question </p><br>
              </div>
              <div v-if="verification.droit">
                <p class="unequest"> Veuillez selectionner au moins un groupe ou un élève qui effectuera ce qcm </p><br>
              </div>
              <div v-if="verification.time">
                <p class="unequest"> Veuillez remplir l'heure pendant laquelle s'effectuera ce qcm </p><br>
              </div>

              <div class="text-center mb-4 mt-5">
                <mdb-btn color="#97adff" type="submit" v-on:click="submit = true" class="btn-block z-depth-2">Valider</mdb-btn>
              </div>

                <!-- Pop up créer question -->
                <mdb-modal :show="modal.question" @close="annulerAjout">
                  <mdb-modal-header>
                    <mdb-modal-title>Ajout d'une question</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>
                    <mdb-input type="textarea" label="Ecrire votre question" outline :rows="3" v-model="questForm.titre" />
                  
                    <div class="form-label">
                      <label for="typeNumber">Barème</label>
                      <input label="Barème" type="number" id="typeNumber" class="form-control" v-model="questForm.bareme" min="1" required/>
                    </div>
                    
                    <div class="radio-btn">
                      <div>
                        Question : 
                      </div>
                      <div>
                        <mdb-input type="radio" id="option-1" name="groupOfMaterialRadios" radioValue="1" v-model="questForm.radioBtn" label="ouverte"/>
                      </div>
                      <div>
                        <mdb-input type="radio" id="option-2" name="groupOfMaterialRadios" radioValue="0" v-model="questForm.radioBtn" label="à choix multiples"/>
                      </div>
                    </div>
                    <div v-if="questForm.radioBtn === '3'">
                      <br><p> Choisissez le type de votre question </p>
                    </div>

                    <!-- si c'est une question à choix multiple -->
                    <div class="btn-ajout-choix" v-if="questForm.radioBtn === '0'">
                      <label class="grey-text">Ajouter un choix</label> 
                      <i class="fas fa-plus-circle" v-on:click="prepAjoutChoix"></i>
                    
                      <div v-if="questForm.choix.length">
                        <table class="table table-hover">
                          <thead>
                            <tr>
                              <th scope="col">Choix</th>
                              <th scope="col">Bonne réponse ?</th>
                              <th scope="col">#</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="choix in questForm.choix" :key="choix.id">
                              <td>
                                {{ choix.choix }}
                              </td>
                              <td v-if="choix.true == 1">
                                Oui
                              </td>
                              <td v-if="choix.true == 0">
                                Non
                              </td>
                              <td>
                                <i class="fas fa-trash" v-on:click="supprimerChoix(choix.id)"></i>
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                      <div v-if="verification.choix">
                        <p> Une question à choix multiple est composé d'au moins deux réponses </p><br>
                      </div>
                    </div>

                  </mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="success" @click.native="addQuestion">Ajouter</mdb-btn>
                    <mdb-btn color="blue-grey" @click.native="annulerAjout">Annuler</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

                <!-- Pop up créer choix -->
                <mdb-modal :show="modal.choix" @close="annulerAjoutChoix">
                  <mdb-modal-header>
                    <mdb-modal-title>Ajout d'un choix</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>
                    <mdb-input type="textarea" label="Ecrire votre choix" outline :rows="3" v-model="choixForm.choix" />
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        value="oui"
                        id="form2Example3"
                        v-model="choixForm.estBonneReponse"
                      />
                      <label class="form-check-label" for="form2Example3">Est-ce une bonne réponse ?</label>
                     
                    </div>
                  </mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="success" @click.native="addChoix">Ajouter</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

                <!-- Pop up supprimer question -->
                <mdb-modal :show="modal.supprQuestion" @close="modal.supprQuestion = false">
                  <mdb-modal-body>Voulez-vous vraiment supprimer cette question ?</mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="success" @click.native="supprimerQuestion">Oui</mdb-btn>
                    <mdb-btn color="blue-grey" @click.native="modal.supprQuestion = false">Non</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

                 <!-- Pop up visualisation choix multiples -->
                <mdb-modal :show="modal.visuChoixMult" @close="modal.visuChoixMult = false">
                  <mdb-modal-header>
                    <mdb-modal-title>{{question.titre}}</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>                 
                    <div v-if="question.choix.length">
                      <table class="table table-hover">
                        <thead>
                          <tr>
                            <th scope="col">Choix</th>
                            <th scope="col">Bonne réponse ?</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="choix in question.choix" :key="choix.id">
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
                  </mdb-modal-body>
                </mdb-modal>


            </form>
          </mdb-card-body>
        </mdb-card>
  </section>
</template>

<script>
  import axios from 'axios';
  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn, mdbModal,
      mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter } from 'mdbvue';
  import Multiselect from 'vue-multiselect'
  import VueTimepicker from 'vue2-timepicker/dist/VueTimepicker.common.js'


  export default { 
    name: 'CreationQcm',
    components: {
      mdbModal,
      mdbModalHeader,
      mdbModalTitle,
      mdbModalBody,
      mdbModalFooter,
      mdbRow,
      mdbCol,
      mdbCard,
      mdbCardBody,
      mdbInput,
      mdbBtn,
      Multiselect,
      VueTimepicker
    },
    data() {
      return {
        droit: {
          groupes: [],
          utilisateur: [],
          valueGroupe: [],
          valueUser: []
        },
        modal: {
          question: false,
          ok: false,
          choix: false,
          supprQuestion: false,
          visuChoixMult: false,
          index: '',
          indexChoix: ''
        },
        qcmForm: { 
          titre: '',
          date:'',
          droit:{
            groupe: [], 
            utilisateur: [] 
          },
          time: {
            debut:'',
            fin:''
          },
          questions: []
        },
        questForm: {
          titre: '',
          bareme: '',
          choix: [],
          radioBtn: ''
        },
        idChoix: 0,
        idQuestion: 0,
        choixForm:{
          choix: '',
          estBonneReponse: ''
        },
        verification : {
          question: false,
          choix: false,
          droit: false,
          time: false
        },
        question: {
          titre: '',
          choix: [],
          radioBtn: ''
        },
        submit: false
      };
    },
    methods: {
      addQcm(data) {
        const path = `http://localhost:5000/api/qcm`;
        axios.post(path, data)
          // eslint-disable-next-line no-unused-vars
          .then((res) => {
            this.initForm()
          })
          .catch((error) => {
            console.log(error);
          });
      },
      addQuestion() {
        let estOuverte = -1;
        if (this.questForm.radioBtn == "0") {
          estOuverte = 0
        } else if (this.questForm.radioBtn == "1"){
          estOuverte = 1
        } else {
          estOuverte = 3
        }

        if ((estOuverte == 0) && (this.questForm.choix.length < 2)){
          this.verification.choix = true
        }  else if (estOuverte == 3) {
          this.questForm.radioBtn = "3"
        } else if (this.questForm.bareme > 0){
          const q = {
            id: this.idQuestion,
            titre: this.questForm.titre,
            ouverte: estOuverte,
            bareme: this.questForm.bareme,
            choix: this.questForm.choix,
          }

          this.qcmForm.questions.push(q)
          this.idQuestion++
          this.modal.question = false
          this.initQuestForm()

          if(this.verification.question){
            this.verification.question = false
          }
        }
      },
      addChoix() {
        let estBonneReponse
        if(this.choixForm.estBonneReponse) {
          estBonneReponse = 1
        } else {
          estBonneReponse = 0
        }

        const c = 
        {
          id: this.idChoix,
          choix: this.choixForm.choix,
          true: estBonneReponse
        }
        
        this.questForm.choix.push(c)
        this.idChoix++
        this.modal.choix = false
        this.initChoixForm()

        if (this.questForm.choix.length >= 2){
          this.verification.choix = false
        }
      },
      initForm() {
        this.qcmForm.titre = '',
        this.qcmForm.date = '',
        this.qcmForm.time.debut = '',
        this.qcmForm.time.fin = '',
        this.qcmForm.groupe = '',
        this.qcmForm.utilisateur = '',
        this.qcmForm.questions = '',
        this.submit = false
        this.droit.valueUser = []
        this.droit.valueGroupe = []
      },
      initQuestForm() {
        this.questForm.titre = '',
        this.questForm.bareme = '',
        this.questForm.choix = [],
        this.questForm.radioBtn = ''
      },
      initChoixForm() {
        this.choixForm.choix = '',
        this.choixForm.estBonneReponse = ''
      },
      choixQuestForm() {
        this.questForm.titre = '',
        this.questForm.choix = [],
        this.questForm.radioBtn = ''
      },
      onSubmit(evt) {
        if (this.submit) {
          evt.preventDefault();

          if (this.qcmForm.questions.length < 1) {
            this.verification.question = true
            this.submit = false
          } else if ((this.droit.valueGroupe.length == 0) && (this.droit.valueUser.length == 0)) {
            this.verification.droit = true
            this.submit = false
          } else if (!(this.qcmForm.time.debut && this.qcmForm.time.fin)) {
            this.verification.time = true
            this.submit = false
          } else {
            this.verification.question = false
            this.verification.droit = false

            this.qcmForm.droit.groupe = this.getDroit(this.droit.valueGroupe)
            this.qcmForm.droit.utilisateur = this.getDroit(this.droit.valueUser)

            const q = JSON.parse(JSON.stringify(this.qcmForm.questions))
            const d = JSON.parse(JSON.stringify(this.qcmForm.droit))

            const newQcm = {
              titre: this.qcmForm.titre,
              droit: d,
              date_debut: this.getDateDebut(),
              date_fin: this.getDateFin(),
              questions: q
            };

            this.addQcm(newQcm);
          }
        }
        

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
      getDateDebut(){
        let date = this.qcmForm.date + " " + this.qcmForm.time.debut + ":00"
        return date
      },
      getDateFin(){
        let date = this.qcmForm.date + " " + this.qcmForm.time.fin + ":00"
        return date
      },
      getQuestChoixMult(question){
        this.question.titre = question.titre
        this.question.choix = question.choix
        this.question.radioBtn = question.radioBtn
        this.modal.visuChoixMult = true
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
      prepSupprQuest(id) {
        this.modal.supprQuestion = true
        this.modal.index = id
      },
      prepAjoutChoix(id) {
        this.modal.choix = true
        this.modal.indexChoix = id
      },
      supprimerQuestion() {
        const index = this.qcmForm.questions.findIndex((element) => element.id == this.modal.index)

        this.qcmForm.questions.splice(index, 1)
        this.modal.index = ''
        this.modal.supprQuestion = false
      },
      supprimerChoix(id) {
        const index = this.questForm.choix.findIndex((element) => element.id == id)
        this.questForm.choix.splice(index, 1)
      },
      annulerAjout() {
        this.initQuestForm()
        this.modal.question = false
        this.modal.modifQuestion = false
      },
      annulerAjoutChoix() {
        this.modal.indexChoix = ''
        this.initChoixForm()
        this.modal.choix = false
      }
    },
    created(){
      this.getGroupe()
      this.getUser()
    }
  }
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style src="vue2-timepicker/dist/VueTimepicker.css"></style>

<style>

  .margetop {
    margin-top: 25px;
  }

  .form-label {
    text-align: left;
    margin-bottom: 25px;
  }

  .dropdown {
    margin-bottom: 30px;
  }

  .unequest {
    margin-top: 50px;
  } 

  .mb-3.input-group {
    margin-bottom: 2rem !important;
    margin-top: 1rem;
  }

  .card {
    max-width: 50%;
    left: 25%;
  }

  .card .md-form label {
    font-weight: 300;
    left: 0;
  }

  .creer-qcm > p {
    color: red;
  }

  .btn-ajout-choix {
    margin-top: 20px;
  }

  .btn-choix {
    margin-top: 20px;
    background-color: #f5f5f5;
  }
  
  .radio-btn {
      text-align: left;
  }

  thead {
    background-color: #f5f5f5;
  }
  
  .form-check-label {
    margin-left: 10px;
  }
  
  i {
    margin-left: 10px;
    cursor: pointer;
  }

  .time {
    top: 30px;
    position: relative;
  }

  .heure {
    position: absolute;
    left: 15px;
  }

  .btn-questions {
    background-color: #fff4d5;
  }

  .btn-block {
    background-color: #d5deff;
  }

  .form-simple {
    margin-top: 50px; }

  .form-simple .font-small {
    font-size: 0.8rem; }

  .form-simple .header {
    border-top-left-radius: .3rem;
    border-top-right-radius: .3rem; }

  .form-simple input[type=text]:focus:not([readonly]) {
    border-bottom: 1px solid #ff3547;
    -webkit-box-shadow: 0 1px 0 0 #ff3547;
    box-shadow: 0 1px 0 0 #ff3547; }

  .form-simple input[type=text]:focus:not([readonly]) + label {
    color: #4f4f4f; }

  .form-simple input[type=password]:focus:not([readonly]) {
    border-bottom: 1px solid #ff3547;
    -webkit-box-shadow: 0 1px 0 0 #ff3547;
    box-shadow: 0 1px 0 0 #ff3547; }

  .form-simple input[type=password]:focus:not([readonly]) + label {
    color: #4f4f4f; }

  section.preview {
      border: 1px solid #e0e0e0;
      padding: 15px;
  }

</style>
