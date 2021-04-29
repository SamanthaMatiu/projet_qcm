<template>
  <section class="form-simple">
    <mdb-row>
      <mdb-col md="5 mx-auto">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">{{ qcm.titre}}</h3>
            </mdb-row>
          </div>
          <mdb-card-body class="mx-4 mt-4">
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">Dates</h5>
                    <mdb-row class="d-flex justify-content-center">
                        <p>Début de l'examen:  {{ qcm.date_debut }}</p> 
                    </mdb-row>
                    <mdb-row class="d-flex justify-content-center">
                        <p>Fin de l'examen:  {{ qcm.date_fin }}</p>
                    </mdb-row>
                </div>
            </div>
           
           <br>
            <form v-on:submit.prevent="onSubmit">
                <div v-for="(question,index) in qcm.questions" :key="index">
                <h3> {{question.titre}} </h3>
                <mdb-input v-model="reponseOuverteForm.id[question.id]" v-if = question.ouverte label="Tapez votre réponse ici" />
               
                <br>
                <div v-if = !question.ouverte >
                    <div v-for="(c,index) in question.choix" :key="index" class="justify-content-start">
                    <b-form-checkbox  :value="c.id" :id="'choix_'+c.id" v-model="selected" > <!-- @change="addChoix.push({reponseouverte:'',id_question:question.id,id_choix:c.id})" -->
                    {{ c.choix}} </b-form-checkbox>
                    </div>
                </div>
                <br>
                </div>
                <!--span>cases cochées: {{ selected }} {{ selected.id }}</span-->
            
                <div class="text-center mb-4 mt-5">
                <mdb-btn color="#97adff" type="submit" class="btn-block z-depth-2">Valider vos réponses</mdb-btn>

                <!-- Pop up Utilisateur existe déjà -->
                <mdb-modal :show="modalQCM" @close="modalQCM = false">
                    <mdb-modal-header>
                    <mdb-modal-title>Oh oh !</mdb-modal-title>
                    </mdb-modal-header>
                    <mdb-modal-body>Vous avez déjà répondu au QCM !</mdb-modal-body>
                    <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modalQCM = false">Ok</mdb-btn>
                    </mdb-modal-footer>
                </mdb-modal>

                </div>
            </form>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
  import axios from 'axios';
  import router from '../../router';

  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn, mdbModal,
      mdbModalHeader,
      mdbModalTitle,
      mdbModalBody,
      mdbModalFooter,
     } from 'mdbvue';

  export default { 
    name: 'RepondreQcm',
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
    },
    props: [
        'question'
    ],
    data() {
      return {
        selected: [],
        addChoix: [],
        modalQCM: false,
      
        qcm: {},
        id_qcm: this.$route.params.id,
        qcmForm: {
          id_question: '',
          titre: '',
          reponses: []
        },
        reponsesForm: {
          reponseouverte:'',
          id_choix:'',
          id_eleve:'',
          id_question:''
        },
        reponseOuverteForm: {
          id: []
        },
        submit : false
      };
    },
    methods: {
      addQcmReponses(data) {
        const path = `http://localhost:5000/api/qcmReponses`;
        axios.post(path, data).
        then((res) => {
          if(res.data.status == 404) {
            console.log("erreur 404")
            this.modalQCM = true
          } else {
            router.push({ name: "Eleve", params: {}});
          }
        });
      },
      
      initQcmForm() {
        this.qcmForm = {
          id_question: '',
          titre: '',
          reponses: []
        }
      },

      initReponseOuverteForm() {
        this.reponseOuverteForm = {id:[]}
      },

      initReponsesForm() {
        this.reponsesForm = {
              reponseouverte:'',
              id_choix:'',
              id_eleve:'',
              id_question:''
            }
      },

      addReponseOuverte() {
        for (let i = 0; i < this.qcm.questions.length; i++) {
          this.initReponsesForm()
          console.log('coucou')
          console.log(this.qcm.questions[i].ouverte)
          if(this.qcm.questions[i].ouverte == true) {
            console.log('lardon')
            if(this.reponseOuverteForm.id[this.qcm.questions[i].id] != undefined) {
              this.reponsesForm.reponseouverte = this.reponseOuverteForm.id[this.qcm.questions[i].id]
            }else {
              this.reponsesForm.reponseouverte = ""
            }
            this.reponsesForm.id_choix = null
            this.reponsesForm.id_eleve = this.qcm.id_eleve
            this.reponsesForm.id_question= this.qcm.questions[i].id
            this.qcmForm.reponses.push(this.reponsesForm)
          }

        }
      },

     
      onSubmit(e) {
        
          e.preventDefault();
        
          this.addReponseOuverte()
        
          console.log('selected')

          for (let i = 0; i < this.qcm.questions.length; i++) {
            
            if(this.qcm.questions[i].ouverte == false) {

              for (let j = 0; j < this.qcm.questions[i].choix.length; j ++){
                this.initReponsesForm()
                for(let k = 0; k < this.selected.length; k ++) {

                  if(this.selected[k] == this.qcm.questions[i].choix[j].id) {
                    const r = {
                      reponseouverte : "",
                      id_choix : this.selected[k],
                      id_eleve : this.qcm.id_eleve,
                      id_question : this.qcm.questions[i].id
                    }
            
                    this.qcmForm.reponses.push(r)
                  }
                }
              }
            }
          }
          const newQcmReponses = {
            id: this.qcm.id,
            titre: this.qcm.titre,
            réponses: this.qcmForm.reponses
          };
          console.log(newQcmReponses)
       

          console.log(this.selected)
          console.log('toutes les réponses')
          console.log(this.qcmForm.reponses)
          this.addQcmReponses(newQcmReponses)
          this.initReponseOuverteForm()
          this.initReponsesForm()
          this.initQcmForm()
        
        }
      
    },
    async created(){
        console.log(this.id);
        axios.get('http://localhost:5000/api/qcmaFaire/'+this.id_qcm)
        .then((res) => {this.qcm = res.data;console.log('toto');
        console.log(res.data)}) //this.todos = res.data
        .catch(err => console.log(err));
    },
 
  }
</script>

<style>
 

  .btn-block {
    background-color: #d5deff;
  }

  .checkbox-btn {
    text-align: left;
    color: #757575;
  }

  label {
  display: block;
  padding-left: 15px;
  text-indent: -15px;
    }


  .form-simple {
    margin-top: 50px; }

  .form-simple .font-small {
    font-size: 0.8rem; }

  .form-simple .header {
    border-top-left-radius: .3rem;
    border-top-right-radius: .3rem; }

  section.preview {
      border: 1px solid #e0e0e0;
      padding: 15px;
  }

</style>
