<template>
  <div class="center-tab card text-center">
    <div class="card-header"><h3>Mes QCMs</h3></div>
    <div class="card-body">
      <div class="col-sm table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col">Date</th>
              <th scope="col">Satut</th>
              <th scope="col">#</th>
            </tr>
          </thead>
          <tbody>
            
              <tr v-for="qcm in data" :key="qcm.id">
                <td>{{ qcm.titre }}</td>
                <td>{{ qcm.date_debut }}</td>
                <template v-if="qcm.statut == 'A faire'">
                  <td>A faire</td>
                  <td>
                    <router-link :to="{ name: 'DetailQcm', params: { id: qcm.id }}">
                      <i class="fas fa-pen"></i>
                    </router-link>
                  </td>
                </template>
                <template v-if="qcm.statut != 'A faire'">
                  <td>Fait</td>
                  <td>
                    <i class="dis fas fa-pen"></i>
                  </td>
                </template>
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
        data: []
      }
    },
  methods: {
    getQcms(){
      const path = `http://localhost:5000/api/qcmProf`;
      axios.get(path)
        .then((res) => {
          this.data = res.data
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  },
  created() {
    this.getQcms()
  }
}
</script>

<style scoped lang="scss">

  .dis {
    color: #cacaca;
  }

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
