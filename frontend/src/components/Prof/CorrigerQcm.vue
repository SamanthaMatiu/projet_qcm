<template>
  <div class="row">
    <div class="col-1">
      <router-link :to="{ name: 'Correction'}">
        <i class="retour fas fa-arrow-circle-left fa-2x"></i>
      </router-link>
    </div>
    <div class="col-11">
      <div class="card text-center">
        <div class="card-header"><h3>{{data.titre}}</h3></div>
        <div class="card-body">
       
            <form v-on:submit.prevent="onSubmit">
                <div v-for="(question,id) in data.questions" :key="id">
                <h4> {{question.intitule}} </h4>
                <div v-if = question.estOuverte>
                <mdb-input v-model="question.reponseOuverte" disabled/>                
                <button type="button" class="btn btn-success btn-sm" @click="onSubmitReponseTrue(question)">Ok</button>
                <button type="button" class="btn btn-danger btn-sm" @click="onDeleteUser(question.id)">Non</button>
                </div>
                <br>
                <div v-if = !question.estOuverte >
                    <div v-for="(choix,id_choix) in question.choix" :key="id_choix" class="justify-content-start">
                        <div v-if = choix.estChoisi>
                            <b-form-checkbox id="choix" v-model="checkOk" disabled>{{ choix.intitule }}</b-form-checkbox>
                        </div>
                        <div v-else>
                            <b-form-checkbox id="choix" disabled>{{ choix.intitule }}</b-form-checkbox>
                        </div>
                    </div>
                    <br>
                    
                </div>
                <br>
                </div>
            
            </form>
       
        </div>
      </div>  
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {mdbInput} from 'mdbvue';

export default {
  name: 'CorrigerQcm',
  components: {
      mdbInput,
    },
  data() {
    return {
        id_qcm: this.$route.params.id_qcm,
        id_eleve: this.$route.params.id_eleve,
        data: {},
        checkOk: true,
        reponse : {
            isTrue:'false',
            id_question: ''
        }
    }
  },
  methods: {
    getData() {
      const path = 'http://localhost:5000/api/NoteQcmFait/'+this.id_qcm+'/'+this.id_eleve;
      axios.get(path)
        .then((res) => {
          this.data = res.data;
          console.log(this.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },

    setReponseTrue(payload, id_question) {
      const path = `http://localhost:5000/api/correctionQuestionOuverte/`+this.id_eleve+`/${id_question}`;
      //axios.post(path, payload)
       // .then(() => {
        //  console.log('ok')
        //})
        //.catch((error) => {
        //  console.error(error);
        //});
        console.log(path);
        console.log(payload);
    },
    onSubmitReponseTrue(question) {
      const infos = {
        correction: true,
      };
      console.log(question);
      this.setReponseTrue(infos, question.id);
    },

  },
  created() {
      this.getData();
  }
}
</script>

<style scoped lang="scss">

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

