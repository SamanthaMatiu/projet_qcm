<template>
  <div class="card text-center">
    <div class="card-header">Featured</div>
    <div class="card-body">
      <div class="col-sm table-responsive">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">Titre</th>
              <th scope="col">Date</th>
              <th scope="col">Durée</th>
              <th scope="col">Etat</th>
            </tr>
          </thead>
          <tbody>
            <tr v-on:click="getQcm()">
              <th scope="row">1</th>
              <td>Mark</td>
              <td>Otto</td>
              <td>@mdo</td>
            </tr>
            <tr>
              <th scope="row">2</th>
              <td>Jacob</td>
              <td>Thornton</td>
              <td>@fat</td>
            </tr>
            <tr>
              <th scope="row">3</th>
              <td colspan="2">Larry the Bird</td>
              <td>@twitter</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="card-footer text-muted">2 days ago</div>
  </div>  
</template>

<script>
  import axios from 'axios';

export default {
  name: 'Consultation',
  methods: {
    onSubmit(evt) {
        evt.preventDefault();
        // eslint-disable-next-line no-unused-vars
        const newQcm = {
          /*titre: this.qcmForm.titre,
          date_debut: this.getDateDebut(),
          date_fin: this.getDateFin(),
          groupe: this.qcmForm.groupe,
          utilisateur: this.qcmForm.utilisateur,
          questions: q*/
        };
    },
    getQcm(){
      const path = 'http://localhost:5000/api/qcmProf';
      axios.get(path)
        .then((res) => {
          console.log(res)
        })
        .catch((error) => {
          // eslint-disable-next-line
          console.error(error);
        });
    }
  }
}
</script>

<style scoped lang="scss">
  thead {
    background-color: #d5deff;
  }

  .tableau {
    text-align: center;
    width: 70%;
  }
</style>
