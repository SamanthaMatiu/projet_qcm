<template>
    <div>
        <b-card no-body>
            <b-tabs pills card>
                <b-tab title="A VALIDER" active><b-card-text><ValidationUser/></b-card-text></b-tab>
                <b-tab title="Tous les utilisateurs"><b-card-text><Users/></b-card-text></b-tab>
                <b-tab title="Gestion groupes utilisateurs"><b-card-text><Groupes/></b-card-text></b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
import ValidationUser from '@/components/Admin/ValidationUser.vue'
import Users from '@/components/Admin/Users.vue'
import Groupes from '@/components/Admin/Groupes.vue'

export default {
  name: 'DashboardAdmin',
  components: {
    ValidationUser,
    Users,
    Groupes
  }
}
</script>