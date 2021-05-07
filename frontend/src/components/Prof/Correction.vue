<template>
  <div class="center-tab card text-center">
    <div class="card-header"><h3>QCMs à corriger</h3></div>
    <div class="card-body">
      <div class="col-sm table-responsive">
        <div>
        <b-form class="w-100">
          <b-form-select v-model="exam" class="mb-2">
            <b-form-select-option :value="null" disabled>Choisir un QCM</b-form-select-option>
            <b-form-select-option v-for="(option, index) in exams" :key="index" v-bind:value="option.id">{{option.titre}}</b-form-select-option>
          </b-form-select>
          <b-button-group>
            <button type="button" class="btn btn-primary btn-sm" @click="onSubmitFiltre()">Filtrer</button>
            <button type="button" class="btn btn-dark btn-sm" @click="reset()">Supprimer filtre</button>
          </b-button-group>
          </b-form>
        </div>
        <br>
        <br>
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col">Eleve</th>
              <th scope="col">#</th>
            </tr>
          </thead>
          <tbody>
            
              <tr v-for="qcm in data" :key="qcm.id">
                <td>{{ qcm.titre }}</td>
                <td>{{ qcm.Nom }} {{ qcm.Prenom }}</td>
                <td>
                  <router-link :to="{ name: 'CorrigerQCM', params: { id_qcm: qcm.id_qcm, id_eleve:qcm.id_eleve }}">
                    <i class="fas fa-pen"></i>
                  </router-link>
                </td>
              </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>  
</template>

<script>
  import axios from 'axios';
export default {
  name: 'Consultation',
  data() {
      return {
        data: [],
        exams:[],
        exam:null,
      }
    },
  methods: {
    getQcms(){
      const path = `http://localhost:5000/api/listQCM`;
      axios.get(path)
        .then((res) => {
          this.data = res.data
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getExams(){
      const path = `http://localhost:5000/api/qcmProf`;
      axios.get(path)
        .then((res) => {
          this.exams = res.data
        })
        .catch((error) => {
          console.error(error);
        });
    },
    setFiltrer() {
      const path = `http://localhost:5000/api/listQCM/`+this.exam;
      axios.get(path)
        .then((res) => {
          this.data = res.data
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSubmitFiltre() {
      this.setFiltrer();
    },
    reset() {
      this.exam = null;
      this.getQcms();
    }
  },
  created() {
    this.getQcms();
    this.getExams();
  }
}
</script>

<style scoped lang="scss">

  .center-tab {
    max-width: 70%;
    left: 15%;
  }

  thead {
    background-color: #d5deff;
  }

  .tableau {
    text-align: center;
    width: 70%;
  }
</style>