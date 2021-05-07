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
        <form v-on:submit.prevent="onSubmit">
        <div class="card-body">
       
                <div v-for="(question,id) in data.questions" :key="id">
                <h4> {{question.intitule}} </h4>
                <div v-if = question.estOuverte>
                <mdb-input v-model="question.reponseOuverte" disabled/> 
                <div v-if="(!(question.note===null))&&(question.note>0)"><i>Correction enregistrée : <b>Correct</b>
                  <br> Mais vous pouvez encore modifier votre correction :</i></div>
                <div v-if="(!(question.note===null))&&(question.note===0)"><i>Correction enregistrée : <b>Incorrect</b>
                  <br> Mais vous pouvez encore modifier votre correction :</i></div>               
                <button type="button" class="btn btn-success btn-sm" @click="onSubmitReponseTrue(question.id_question)">Correct</button>
                <button type="button" class="btn btn-danger btn-sm" @click="onSubmitReponseFalse(question.id_question)">Incorrect</button>
                </div>
                <br>
                <div v-if = !question.estOuverte >
                    <div v-for="(choix,id_choix) in question.choix" :key="id_choix" class="justify-content-start">
                        <div v-if = choix.estChoisi>
                          <div v-if = choix.estCorrect  v-bind:class="{'checkCorrect': checkCorrect}">
                            <b-form-checkbox id="choix" v-model="checkCorrect" disabled> {{ choix.intitule }} <span><i style="color: #66CC33;" class=" ml-5 fas fa-check-circle"></i></span></b-form-checkbox>
                          </div>
                          <div v-else >
                            <b-form-checkbox id="choix" v-model="checkIncorrect" disabled>{{ choix.intitule }} <span><i  style=" color: Tomato;" class="ml-5 fas fa-times-circle"></i></span></b-form-checkbox>
                          </div>
                        </div>
                        <div v-else>
                          <div v-if = choix.estCorrect>
                            <b-form-checkbox id="choix" disabled>{{ choix.intitule }} <span><i style="color: Blue;" class="ml-5 fas fa-check-double"></i></span></b-form-checkbox>
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
        </div>
          <div class="card-footer text-muted">
          <button type="submit" class="btn btn-primary btn-sm">Correction terminée</button>
        </div>
        </form>
      </div>  
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../../router';
import {mdbInput} from 'mdbvue';

export default {
  name: 'CorrigerQcm',
  components: {
      mdbInput
    },
  data() {
    return {
        id_qcm: this.$route.params.id_qcm,
        id_eleve: this.$route.params.id_eleve,
        data: {},
        checkOk: true,
        checkCorrect: true,
        checkIncorrect: true, 
    }
  },
  methods: {
    getData() {
      const path = 'http://localhost:5000/api/NoteQcmFait/'+this.id_qcm+'/'+this.id_eleve;
      axios.get(path)
        .then((res) => {
          this.data = res.data;
        })
        .catch((error) => {
          console.error(error);
        });
    },

    setReponse(payload, id_question) {
      const path = `http://localhost:5000/api/correctionQuestionOuverte/`+this.id_eleve+`/${id_question}`;
      axios.post(path, payload)
        .then(() => {
          this.$bvModal.msgBoxOk('Correction enregistrée !', {
          size: 'sm',
          buttonSize: 'sm',
          okVariant: 'success',
          headerClass: 'p-2 border-bottom-0',
          footerClass: 'p-2 border-top-0',
          centered: true
        })
          this.getData();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitReponseTrue(question) {
      const infos = {
        correction: true,
      };
      this.setReponse(infos, question);
    },

    onSubmitReponseFalse(question) {
      const infos = {
        correction: false,
      };
      this.setReponse(infos, question);
    },

    onSubmit(evt){
      evt.preventDefault();
      this.setQcmCorrige();
    },

    setQcmCorrige() {
      const path = 'http://localhost:5000/api/correction/'+this.id_qcm+'/'+this.id_eleve;
      axios.patch(path)
        .then(() => {
          router.push({ name: "Correction", params: {}});
        })
        .catch((error) => {
          console.error(error);
        });
    },

  },
  created() {
      this.getData();
  }
}
</script>

<style scoped lang="scss">
 .checkCorrect{
  border: 1px;
  border-color: green;
}
  .checkIncorrect{
  background-color:red;

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

