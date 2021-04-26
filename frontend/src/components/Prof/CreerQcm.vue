<template>
  <section class="form-simple">
    <mdb-row>
      <mdb-col md="5 mx-auto">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">Création de Qcm</h3>
            </mdb-row>
          </div>
          <mdb-card-body class="mx-4 mt-4">
            <form v-on:submit.prevent="onSubmit">
              
              <mdb-input label="Titre" type="text" v-model="qcmForm.titre" required/>
              <mdb-input label="" type="date" v-model="qcmForm.date" required/>
              <!--<label class="grey-text">hh:mm AM/PM</label>-->
              <mdb-row>
                <mdb-col col="6 lg-8">
                  <label class="grey-text heure">Heure de début</label>
                  <mdb-input label="" type="time" class="time" v-model="qcmForm.time.debut" required/>
                </mdb-col>
                <mdb-col col="6 lg-4">
                  <label class="grey-text heure">Heure de fin</label>
                  <mdb-input label="" type="time" class="time" v-model="qcmForm.time.fin" required/>
                </mdb-col>
              </mdb-row>
              
              <!-- Dropdown : TODO v-for sur groupe/user -->
              <mdb-input basic class="mb-3" ariaLabel="Example text with button addon" ariaDescribedBy="button-addon1">
                <mdb-dropdown slot="prepend">
                  <mdb-dropdown-toggle color="#97adff" size="md" slot="toggle" class="z-depth-0">Droits</mdb-dropdown-toggle>
                  <mdb-dropdown-menu>
                    <mdb-dropdown-item>Action</mdb-dropdown-item>
                    <mdb-dropdown-item>Another action</mdb-dropdown-item>
                    <mdb-dropdown-item>Something else here</mdb-dropdown-item>
                    <div class="dropdown-divider"></div>
                    <mdb-dropdown-item>Separated link</mdb-dropdown-item>
                  </mdb-dropdown-menu>
                </mdb-dropdown>
              </mdb-input>

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
                <p> Un Qcm est composé d'au moins une question </p><br>
              </div>

              <div class="text-center mb-4 mt-5">
                <mdb-btn color="#97adff" type="submit" class="btn-block z-depth-2">Submit</mdb-btn>
              </div>

                <!-- Pop up Utilisateur créé -->
                <mdb-modal :show="modal.ok" @close="modal.ok = false">
                  <mdb-modal-header>
                    <mdb-modal-title>Utilisateur créer !</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>Vous devez attendre que votre compte soit validé.</mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modal.ok = false">Ok</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

                <!-- Pop up créer question -->
                <mdb-modal :show="modal.question" @close="annulerAjout">
                  <mdb-modal-header>
                    <mdb-modal-title>Ajout d'une question</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>
                    <mdb-input type="textarea" label="Ecrire votre question" outline :rows="3" v-model="questForm.titre" />
                    
                    <div class="radio-btn">
                      <div>
                        Question : 
                      </div>
                      <div>
                        <mdb-input type="radio" id="option-1" name="groupOfMaterialRadios" v-on:click="verification.typeQuestion = false" radioValue="1" v-model="questForm.radioBtn" label="ouverte"/>
                      </div>
                      <div>
                        <mdb-input type="radio" id="option-2" name="groupOfMaterialRadios" v-on:click="verification.typeQuestion = false" radioValue="0" v-model="questForm.radioBtn" label="à choix multiples"/>
                      </div>
                    </div>
                    <div v-if="verification.typeQuestion">
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
                              <th scope="col">#</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="choix in questForm.choix" :key="choix.id">
                              <td>
                                {{ choix.choix }}
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
                    <mdb-input type="textarea" label="Ecrire votre choix" outline :rows="3" v-model="choix" />
                    <div class="form-check">
                      <input
                        class="form-check-input"
                        type="checkbox"
                        value=""
                        id="form2Example3"
                        checked
                      />
                      <label class="form-check-label" for="form2Example3">Est-ce la bonne réponse ?</label>
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
                            <th scope="col">Réponse</th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="choix in question.choix" :key="choix.id">
                            <td>
                              {{ choix.choix }}
                            </td>
                            <td>
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
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
  import axios from 'axios';
  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn, mdbModal,
      mdbModalHeader, mdbModalTitle, mdbModalBody, mdbModalFooter,
      mdbDropdown, mdbDropdownToggle, mdbDropdownMenu, mdbDropdownItem } from 'mdbvue';

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
      mdbDropdown,
      mdbDropdownToggle,
      mdbDropdownMenu,
      mdbDropdownItem
    },
    data() {
      return {
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
          time: {
            debut:'',
            fin:''
          },
          groupe: '', //{"id":6}
          utilisateur: '', //{"id":6}
          questions: []
        },
        questForm: {
          titre: '',
          choix: [],
          radioBtn: ''
        },
        idChoix: 0,
        idQuestion: 0,
        choix:'',
        verification : {
          question: false,
          choix: false,
          typeQuestion: false
        },
        question: {
          titre: '',
          choix: [],
          radioBtn: ''
        }
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
          estOuverte = 2
        }

        if ((estOuverte == 0) && (this.questForm.choix.length < 2)){
          this.verification.choix = true
        }  else if (estOuverte == 2) {
          this.verification.typeQuestion = true
        } else {
          const q = {
            id: this.idQuestion,
            titre: this.questForm.titre,
            ouverte: estOuverte,
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
        const c = 
        {
          id: this.idChoix,
          choix: this.choix,
          true:0
        }

        this.questForm.choix.push(c)
        this.idChoix++
        this.modal.choix = false
        this.choix = ''

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
        this.qcmForm.questions = ''
      },
      initQuestForm() {
        this.questForm.titre = '',
        this.questForm.choix = [],
        this.questForm.radioBtn = ''
      },
      onSubmit(evt) {
        evt.preventDefault();
        const q = JSON.parse(JSON.stringify(this.qcmForm.questions))
        const newQcm = {
          titre: this.qcmForm.titre,
          date_debut: this.getDateDebut(),
          date_fin: this.getDateFin(),
          groupe: this.qcmForm.groupe,
          utilisateur: this.qcmForm.utilisateur,
          questions: q
        };

        if (this.qcmForm.questions.length < 1) {
          this.verification.question = true
        } else {
          this.verification.question = false
          console.log(newQcm)
          this.addQcm(newQcm);
        }

      },
      getDateDebut(){
        let date = this.qcmForm.date + " " + this.qcmForm.time.debut
        return date
      },
      getDateFin(){
        let date = this.qcmForm.date + " " + this.qcmForm.time.fin
        return date
      },
      getQuestChoixMult(question){
        this.question.titre = question.titre
        this.question.choix = question.choix
        this.question.radioBtn = question.radioBtn
        this.modal.visuChoixMult = true
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
        if(this.verification.typeQuestion){
          this.verification.typeQuestion = false
        }
        this.initQuestForm()
        this.modal.question = false
        this.modal.modifQuestion = false
      },
      annulerAjoutChoix() {
        this.modal.indexChoix = ''
        this.choix = ''
        this.modal.choix = false
      }
    }
  }
</script>

<style>

  p {
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
    width: 100px
  }

  .heure {
    position: absolute;
    left: 15px;
  }

  .dropdown {
    background-color: #d5deff;
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
