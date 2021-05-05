<template>
  <section class="form-simple">
    <mdb-row>
      <mdb-col md="5 mx-auto">
        <mdb-card>
          <div class="header pt-3 grey lighten-2">
            <mdb-row class="d-flex justify-content-start">
              <h3 class="deep-grey-text mt-3 mb-4 pb-1 mx-5">Connexion</h3>
            </mdb-row>
          </div>
          <mdb-card-body class="mx-4 mt-4">
            <mdb-alert v-if = error color="danger">
              Mail et/ou mot de passe incorrect
            </mdb-alert>
            <br>
          <form v-on:submit.prevent="onSubmit">
            <mdb-input v-model="loginForm.mail" label="Mail" type="text" required/>
            <mdb-input v-model="loginForm.mdp" label="Mot de passe" type="password" containerClass="mb-0" required/>
            <div class="text-center mb-4 mt-5">
              <mdb-btn color="danger" type="submit" class="btn-block z-depth-2">Se connecter</mdb-btn>
            </div>
          </form>
            <p class="font-small grey-text d-flex justify-content-center">Tu n'as pas de compte ? <router-link to="/inscription"><a class="dark-grey-text font-weight-bold ml-1"> S'inscrire</a></router-link></p>
          </mdb-card-body>
        </mdb-card>
      </mdb-col>
    </mdb-row>
  </section>
</template>

<script>
  import axios from 'axios';
  import router from '../router';

  import { mdbRow, mdbCol, mdbCard, mdbCardBody, mdbInput, mdbBtn,mdbAlert} from 'mdbvue';
  export default { 
    name: 'FormsPage',
    components: {
      mdbRow,
      mdbCol,
      mdbCard,
      mdbCardBody,
      mdbInput,
      mdbBtn,
      mdbAlert
    },
    data() {
      return {
        loginForm: {
          mail: '',
          mdp: '',
        },
        error:false,
      };
    },
    methods: {
      checkUser(user) {
        const path = `http://localhost:5000/api/login`;
        axios.post(path, user)
          .then((res) => {
            console.log(res.data.message);
            if (res.data.token){
              localStorage.setItem('token', res.data.token);
              localStorage.setItem('statut', res.data.statut);
              this.initForm();
              if(res.data.statut==='Administrateur'){
                router.push({ name: "Admin", params: {}});
              } else if(res.data.statut==='Professeur'){
                router.push({ name: "Prof", params: {}});
              } else {
                router.push({ name: "Eleve", params: {}});
              }
            }
          })
          .catch((error) => {
            console.log(error);
            this.error=true;
          });
      },
      initForm() {
        this.loginForm.mail = '';
        this.loginForm.mdp = '';
      },
      onSubmit(evt) {
        evt.preventDefault();
        const user = {
          utilisateur: this.loginForm.mail,
          mdp: this.loginForm.mdp,
        };
        this.checkUser(user);
      },
    },
  }
</script>

<style>
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
