<template>
  <div class="row">
    <div class="col-1">
      <router-link :to="{ name: 'Consultation'}">
        <i class="retour fas fa-arrow-circle-left fa-2x"></i>
      </router-link>
    </div>
    <div class="col-11">
      <div class="card text-center">
        <div class="card-header">{{data.titre}}</div>
        <div class="card-body">
          
          <mdb-row class="time">
            <mdb-col col="4">
              <p>Date : {{this.affichage.date}}</p> 
            </mdb-col>
            <mdb-col col="8">
              à faire de {{this.affichage.time.debut}} jusqu'à {{this.affichage.time.fin}}  
            </mdb-col>
          </mdb-row>

          <div>
                <table class="table table-hover">
                  <thead>
                    <tr>
                      <th scope="col">Question</th>
                      <th scope="col">Type</th>
                      <th scope="col">Barème</th>
                      <th scope="col">#</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="question in data.questions" :key="question.id">
                      <td>{{ question.titre }}</td>
                      <td v-if="!question.ouverte">Choix multiples</td>
                      <td v-if="question.ouverte">Ouverte</td>
                      <td>{{ question.bareme }}</td>
                      <td>{{ question.bareme }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

        </div>
        <div class="card-footer text-muted">
          <button type="button" class="btn btn-primary btn-sm" @click="modifierQcm()">Modifier</button>
          <button type="button" class="btn btn-danger btn-sm" @click="$bvModal.show('bv-modal-example')">Supprimer</button>
        
          <b-modal id="modal-1" title="Suppression d'une question">
            <p class="my-4">Etes-vous sur de vouloir supprimer cette question ?</p>
          </b-modal>
          <b-modal id="bv-modal-example" hide-footer>
            <template #modal-title>
              Suppression d'une question
            </template>
            <div class="text-center-modal">
              Etes-vous sur de vouloir supprimer cette question ?
            </div>
            <div class="suppr">
              <b-button variant="danger" @click="supprimerQcm()">Oui</b-button>
              <b-button variant="primary" @click="$bvModal.hide('bv-modal-example')">Non</b-button>
            </div>
          </b-modal>

        </div>
      </div>  
    </div>
  </div>
</template>

<script>
  import axios from 'axios';
  import { mdbRow, mdbCol } from 'mdbvue';

export default {
  name: 'DetailQcm',
  components: {
    mdbRow,
    mdbCol
  },
  data() {
    return {
      data: {},
      modal: {
        delete: false,
        modify: false
      },
      affichage: {
        date: "",
        time: {
          debut: "",
          fin: ""
        }
      }
    }
  },
  methods: {
    getQcm(){
      const path = `http://localhost:5000/api/qcm/${this.$route.params.id}`;
      axios.get(path)
        .then((res) => {
          this.data = res.data
          this.affichage.date = res.data.date_debut.slice(0,10)
          this.affichage.time.debut = res.data.date_debut.slice(11,16)
          this.affichage.time.fin = res.data.date_fin.slice(11,16)
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    },
    getDate(){
      this.data.date_debut
    },
    modifierQcm(){
    },
    supprimerQcm(){
      const path = `http://localhost:5000/api/qcm/${this.data.id}`;
      axios.delete(path)
        .then((res) => {
          this.$router.go(-1)
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getQcm()
  }
}
</script>

<style scoped lang="scss">

  .suppr {
    position: relative;
    left: 250px;
  }

  .text-center-modal{
    margin-bottom: 20px;
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
