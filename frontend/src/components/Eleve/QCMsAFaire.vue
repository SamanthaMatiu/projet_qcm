<template>
  <div class="container">
    <br><br>
    <div class="row">
      <div class="col-sm-10">
        <h2>QCMs à faire</h2>
        <hr><br><br>
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col"><b>Nom</b></th>
              <th scope="col"><b>Début</b></th>
              <th scope="col"><b>Fin</b></th>
              <th></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(qcm, index) in qcmsAFaire" :key="index">
              <td>{{ qcm.titre }}</td>
              <td>{{ qcm.date_debut }}</td>
              <td>{{ qcm.date_fin }}</td>
              <td>
                <div class="btn-group" role="group">
                    <router-link :to="{ name: 'RepondreQCM', params: { id: qcm.id }}">
                        <button type="button" class="btn btn-success btn-sm">Faire le QCM</button>
                    </router-link>
                </div>
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
//import router from '../router';

export default {
  data() {
    return {
      qcmsAFaire: []
    };
  },
  methods: {
    getQcms() {
      const path = `http://localhost:5000/api/qcmaFaireInfos`;
      axios.get(path)
        .then((res) => {
          this.qcmsAFaire = res.data;
          console.log(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    //if (!(localStorage.getItem('token'))){
    //  router.push({ name: "Connexion", params: {}});
    //}
    this.getQcms();
  },
};
</script>