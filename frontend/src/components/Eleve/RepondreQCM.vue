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
                <div v-for="(question,id) in qcm.questions" :key="id">
                <h3> {{question.titre}} </h3>
                <mdb-input v-if = question.ouverte label="Tapez votre réponse ici" v-bind:key = question.choix.id  required/>
                <br>
                <div v-if = !question.ouverte >
                    <div v-for="(choix,id_choix) in question.choix" :key="id_choix" class="justify-content-start">
                    <mdb-input class="" type="checkbox" id="choix" /> <label class="" for="choix">{{ choix.choix }} </label>
                    </div>
                    <br>
                    
                </div>
                <br>
                </div>
            
                <div class="text-center mb-4 mt-5">
                <mdb-btn color="#97adff" type="submit" class="btn-block z-depth-2">Valider vos réponses</mdb-btn>

                <!-- Pop up Utilisateur créé -->
                <mdb-modal :show="modalOk" @close="modalOk = false">
                    <mdb-modal-header>
                    <mdb-modal-title>Vos réponses ont été enregistrées !</mdb-modal-title>
                    </mdb-modal-header>
                    <mdb-modal-body>Votre professeurs corrigera votre QCM dès que possible. En attendant vous pouvez toujours le visualiser dans vos QCM faits</mdb-modal-body>
                    <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modalOk = false">Ok</mdb-btn>
                    </mdb-modal-footer>
                </mdb-modal>

                <!-- Pop up Utilisateur existe déjà -->
                <mdb-modal :show="modalUserExist" @close="modalUserExist = false">
                    <mdb-modal-header>
                    <mdb-modal-title>Oh oh !</mdb-modal-title>
                    </mdb-modal-header>
                    <mdb-modal-body>Un compte à déjà été créé avec cet adresse email</mdb-modal-body>
                    <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modalUserExist = false">Ok</mdb-btn>
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
        radioBtn: '',
        modalOk: false,
        modalUserExist: false,
        mdpEstIncorrecte: false,
        userForm: {
          nomauth: '',
          prenomauth: '',
          mailauth: '',
          mdpauth: '',
          mdpverif: ''
        },
        qcm: {},
        id_qcm: this.$route.params.id,
      };
    },
    methods: {
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
