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
                <!--mdb-input v-if = question.estOuverte v-bind:key = question.choix.id disabled/>
                <br>
                <div v-if = !question.estOuverte >
                    <div v-for="(choix,id_choix) in question.choix" :key="id_choix" class="justify-content-start">
                        <div v-if = "choix.choix === qcm.reponses[id].choix">
                            <b-form-checkbox id="choix" v-model="checkOk" disabled>{{ choix.choix }}</b-form-checkbox>
                        </div>
                        <div v-else>
                            <b-form-checkbox id="choix" disabled>{{ choix.choix }}</b-form-checkbox>
                        </div>
                    </div>
                    <br>
                    
                </div-->
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

export default {
  name: 'CorrigerQcm',
  data() {
    return {
        id_qcm: this.$route.params.id_qcm,
        id_eleve: this.$route.params.id_eleve,
        data: {},
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

