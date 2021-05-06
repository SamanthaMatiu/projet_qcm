<template>
    <div>
        <b-card no-body>
            <b-tabs pills card>
                <b-tab title="A VALIDER" active><b-card-text>
                  <div class="deconnexion">
                  <b-button variant="outline-primary" @click="logout()">Déconnexion</b-button>
                  </div>
                  <ValidationUser/></b-card-text>
                </b-tab>
                <b-tab title="Tous les utilisateurs"><b-card-text>
                  <div class="deconnexion">
                  <b-button variant="outline-primary" @click="logout()">Déconnexion</b-button>
                  </div>
                  <Users/></b-card-text>
                </b-tab>
                <b-tab title="Gestion groupes utilisateurs"><b-card-text>
                  <div class="deconnexion">
                  <b-button variant="outline-primary" @click="logout()">Déconnexion</b-button>
                  </div>
                  <Groupes/></b-card-text>
                </b-tab>
                
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
import ValidationUser from '@/components/Admin/ValidationUser.vue'
import Users from '@/components/Admin/Users.vue'
import Groupes from '@/components/Admin/Groupes.vue'
import router from '../../router';

export default {
  name: 'DashboardAdmin',
  components: {
    ValidationUser,
    Users,
    Groupes
  },
  data() {
      return {
      };
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('statut');
        router.push({ name: "Connexion", params: {}});
      },
    },
    created() {
      if (!(localStorage.getItem('token'))){
        router.push({ name: "Connexion", params: {}});
      }
      if (!(localStorage.getItem('statut')==="Administrateur")){
        localStorage.removeItem('token');
        localStorage.removeItem('statut');
        router.push({ name: "Connexion", params: {}});
      }
    },
}
</script>

<style scoped>
.deconnexion{
  text-align: right
}
</style>