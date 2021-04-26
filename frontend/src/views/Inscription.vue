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
            <form v-on:submit.prevent="onSubmit">
              <mdb-input label="Nom" type="text" v-model="userForm.nomauth" required/>
              <mdb-input label="Prénom" type="text" v-model="userForm.prenomauth" required/>
              <mdb-input label="Mail" type="email" v-model="userForm.mailauth" required/>
              <mdb-input label="Mot de passe" type="password" v-model="userForm.mdpauth" required/>
              <mdb-input label="Confirmez mot de passe" type="password" v-model="userForm.mdpverif" required/>
              <div v-if="mdpEstIncorrecte">
                <p> Les deux mots de passe ne sont pas identiques</p><br>
              </div>
              <div class="radio-btn">
                  <mdb-input type="radio" id="option-1" name="groupOfMaterialRadios" radioValue="Professeur" v-model="radioBtn" label="Professeur" required/>
                  <mdb-input type="radio" id="option-2" name="groupOfMaterialRadios" radioValue="Élève" v-model="radioBtn" label="Élève" required/>
              </div>
              <div class="text-center mb-4 mt-5">
                <mdb-btn color="#97adff" type="submit" class="btn-block z-depth-2">S'inscrire</mdb-btn>

                <!-- Pop up Utilisateur créé -->
                <mdb-modal :show="modalOk" @close="modalOk = false">
                  <mdb-modal-header>
                    <mdb-modal-title>Utilisateur créé !</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>Vous devez attendre que votre compte soit validé.</mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modalOk = false">Ok</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

                <!-- Pop up Utilisateur existe déjà -->
                <mdb-modal :show="modalUserExist" @close="modalUserExist = false">
                  <mdb-modal-header>
                    <mdb-modal-title>Oh oh !</mdb-modal-title>
                  </mdb-modal-header>
                  <mdb-modal-body>Un compte à déjà été créé avec cet adresse email</mdb-modal-body>
                  <mdb-modal-footer>
                    <mdb-btn color="secondary" @click.native="modalUserExist = false">Ok</mdb-btn>
                  </mdb-modal-footer>
                </mdb-modal>

              </div>
            </form>
            <p class="font-small grey-text d-flex justify-content-center">Tu as un compte ? <router-link to="/connexion"><a class="dark-grey-text font-weight-bold ml-1"> Connexion</a></router-link></p>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
  import axios from 'axios';
  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn, mdbIcon, mdbModal,
      mdbModalHeader,
      mdbModalTitle,
      mdbModalBody,
      mdbModalFooter } from 'mdbvue';

  export default { 
    name: 'FormsPage',
    components: {
      mdbModal,
      mdbModalHeader,
      mdbModalTitle,
      mdbModalBody,
      mdbModalFooter,
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
        radioBtn: '',
        modalOk: false,
        modalUserExist: false,
        mdpEstIncorrecte: false,
        userForm: {
          nomauth: '',
          prenomauth: '',
          mailauth: '',
          mdpauth: '',
          mdpverif: ''
        } 
      };
    },
    methods: {
      addUser(data) {
        const path = `http://localhost:5000/api/register`;
        axios.post(path, data)
        .then((res) => {
          if (res.data.status == 404){
            this.modalUserExist = true
          } else {
            this.modalOk = true
            this.initForm();
          }
        })
        .catch((error) => {
          console.log(error);
        });
      },
      initForm() {
        this.mdpEstIncorrecte = false,
        this.radioBtn = '',
        this.userForm.nomauth = '',
        this.userForm.prenomauth = '',
        this.userForm.mailauth = '',
        this.userForm.mdpauth = '',
        this.userForm.mdpverif = '',
        this.userForm.droitauth = ''
      },
      onSubmit(evt) {
        evt.preventDefault();
        if (this.userForm.mdpauth == this.userForm.mdpverif) {
          const newUser = {
            nomauth: this.userForm.nomauth,
            prenomauth: this.userForm.prenomauth,
            mailauth: this.userForm.mailauth,
            mdpauth: this.userForm.mdpauth,
            droitauth: this.radioBtn,
          };
          this.addUser(newUser);
        } else {
          this.mdpEstIncorrecte = true
        }
        
      }
    }
  }
</script>

<style>

  .card .md-form label {
    font-weight: 300;
    left: 0;
  }

  p {
    color: red;
  }

  .btn-block {
    background-color: #d5deff;
  }

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
