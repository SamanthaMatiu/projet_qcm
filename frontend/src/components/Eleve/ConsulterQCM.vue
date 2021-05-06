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
                <h3> {{question.intitule}} </h3><h5> {{question.note}}/{{question.bareme}} </h5>
                <mdb-input v-if = question.estOuverte v-model="question.reponseOuverte" disabled/>
                <br>
                <div v-if = !question.ouverte >
                    <div v-for="(choix,id_choix) in question.choix" :key="id_choix" class="justify-content-start">
                      <div v-if = choix.estChoisi>
                        <b-form-checkbox  id="choix" v-model="checkCorrect" disabled>{{ choix.intitule }}</b-form-checkbox>
                      </div>
                      <div v-else>
                        <b-form-checkbox type="checkbox" id="choix" disabled>{{ choix.intitule }}</b-form-checkbox>
                      </div>
                    </div>
                    <br>
                    
                </div>
                <br>
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
  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput,
     } from 'mdbvue';

  export default { 
    name: 'ConsulterQcm',
    components: {
      mdbRow,
      mdbCol,
      mdbCard,
      mdbCardBody,
      mdbInput,
    },
    props: [
        'question'
    ],
    data() {
      return {
        checkOk: true,
        checkCorrect: true,
        checkIncorrect: true, 
        qcm: {},
        id_qcm: this.$route.params.id,
      };
    },
    methods: {
    },
    async created(){
        console.log(this.id);
        axios.get('http://localhost:5000/api/qcmFait/'+this.id_qcm)
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