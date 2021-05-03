<template>
  <div class="row">
    <div class="col-1">
      <router-link :to="{ name: 'Correction'}">
        <i class="retour fas fa-arrow-circle-left fa-2x"></i>
      </router-link>
    </div>
    <div class="col-11">
      <div class="card text-center">
        <div class="card-header">{{data.titre}}</div>
        <div class="card-body">
          <p>
            A faire
          </p>
        </div>
        <div class="card-footer text-muted">
          <button type="button" class="btn btn-primary btn-sm">Modifier</button>
          <button type="button" class="btn btn-danger btn-sm" data-mdb-toggle="modal" data-mdb-target="#exampleModal">Supprimer</button>
        </div>
      </div>  
    </div>

                <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
                  <div class="modal-dialog">
                    <div class="modal-content">
                      <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Modal title</h5>
                        <button
                          type="button"
                          class="btn-close"
                          data-mdb-dismiss="modal"
                          aria-label="Close"
                        ></button>
                      </div>
                      <div class="modal-body">...</div>
                      <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">
                          Close
                        </button>
                        <button type="button" class="btn btn-primary">Save changes</button>
                      </div>
                    </div>
                  </div>
                </div>
  </div>
</template>

<script>
//import axios from 'axios';

export default {
  name: 'CorrigerQcm',
  data() {
    return {
      data: {},
      modal: {
        delete: false,
        modify: false
      }
    }
  },
  methods: {

  },
  created() {
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

