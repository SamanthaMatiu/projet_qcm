<template>
  <section class="form-simple">
    <mdb-row>
      <mdb-col md="5 mx-auto">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">{{ qcm.titre}} </h3>
            </mdb-row>
             <h5> Note: {{qcm.conversionSur20}}/20 </h5>
          </div>
          <mdb-card-body class="mx-4 mt-4">
           
           <br>
            <form v-on:submit.prevent="onSubmit">
                <div v-for="(question,index) in qcm.questions" :key="index">
                <h3> {{question.intitule}} </h3> <h5> {{question.note}}/{{question.bareme}} </h5>
                <mdb-input v-if = question.estOuverte v-model="question.reponseOuverte" disabled/>
                <br>
                <div v-if = !question.ouverte >
                    <div v-for="(choix,index) in question.choix" :key="index" class="justify-content-start">
                        <div v-if = choix.estChoisi>
                          <div v-if = choix.estCorrect  v-bind:class="{'checkCorrect': checkCorrect}">
                            <b-form-checkbox id="choix" v-model="checkCorrect" disabled> {{ choix.intitule }} <span><i style="color: #66CC33;" class=" ml-5 fas fa-check-circle"></i></span></b-form-checkbox>
                          </div>
                          <div v-else >
                            <b-form-checkbox id="choix" v-model="checkIncorrect" disabled> {{ choix.intitule }} <span><i  style=" color: Tomato;" class="ml-5 fas fa-times-circle"></i></span></b-form-checkbox>
                          </div>
                        </div>
                        <div v-else>
                          <div v-if = choix.estCorrect>
                            <b-form-checkbox id="choix" disabled> {{ choix.intitule }} <span><i style="color: Blue;" class="ml-5 fas fa-check-double"></i></span></b-form-checkbox>
                          </div>
                          <div v-else>
                            <b-form-checkbox id="choix" disabled> {{ choix.intitule }} <span><i style="color: White;" class=" ml-5 fas fa-arrow-alt-left"></i></span></b-form-checkbox>
                          </div>

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
    name: 'RepondreQcm',
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
        axios.get('http://localhost:5000/api/NoteQcmFait/'+this.id_qcm)
        .then((res) => {this.qcm = res.data;console.log('toto');
        console.log(res.data)}) //this.todos = res.data
        .catch(err => console.log(err));
    },
  }
</script>

<style>


 
 .checkCorrect{
  border: 1px;
  border-color: green;
}
  .checkIncorrect{
  background-color:red;

} 
  .btn-block {
    background-color: #d5deff;
  }

  .checkbox-btn {
    text-align: left;
    color: #757575;
  }

  /* When the checkbox is checked, add a blue background */
  input:checked{
  background-color: #2196F3;
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