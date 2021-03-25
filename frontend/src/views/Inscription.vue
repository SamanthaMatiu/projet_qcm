<template>
  <section class="form-simple">
    <mdb-row>
      <mdb-col md="5 mx-auto">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">Inscription</h3>
            </mdb-row>
          </div>
          <mdb-card-body class="mx-4 mt-4">
            <mdb-input label="Nom" type="text"/>
            <mdb-input label="Prénom" type="text"/>
            <mdb-input label="Mail" type="text"/>
            <mdb-input label="Mot de passe" type="password"/>
            <mdb-input label="Confirmez mot de passe" type="password"/>
            <div class="radio-btn">
                <mdb-input type="radio" id="option4-1" name="groupOfMaterialRadios" radioValue="Professeur" v-model="radio4" label="Professeur" />
                <mdb-input type="radio" id="option4-2" name="groupOfMaterialRadios" radioValue="Élève" v-model="radio4" label="Élève" />
            </div>
            <div class="text-center mb-4 mt-5">
              <mdb-btn color="danger" type="button" class="btn-block z-depth-2">S'inscrire</mdb-btn>
            </div>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn, mdbIcon } from 'mdbvue';
  export default { 
    name: 'FormsPage',
    components: {
      mdbRow,
      mdbCol,
      mdbCard,
      mdbCardBody,
      mdbInput,
      mdbBtn,
      // eslint-disable-next-line vue/no-unused-components
      mdbIcon
    },
    data() {
      return {
        radio4: "" 
      };
    }
  }
</script>

<style>
  .radio-btn {
    text-align: left;
    color: #757575;
  }

  .form-simple {
    margin-top: 50px; }

  .form-simple .font-small {
    font-size: 0.8rem; }

  .form-simple .header {
    border-top-left-radius: .3rem;
    border-top-right-radius: .3rem; }

  .form-simple input[type=text]:focus:not([readonly]) {
    border-bottom: 1px solid #ff3547;
    -webkit-box-shadow: 0 1px 0 0 #ff3547;
    box-shadow: 0 1px 0 0 #ff3547; }

  .form-simple input[type=text]:focus:not([readonly]) + label {
    color: #4f4f4f; }

  .form-simple input[type=password]:focus:not([readonly]) {
    border-bottom: 1px solid #ff3547;
    -webkit-box-shadow: 0 1px 0 0 #ff3547;
    box-shadow: 0 1px 0 0 #ff3547; }

  .form-simple input[type=password]:focus:not([readonly]) + label {
    color: #4f4f4f; }
</style>
