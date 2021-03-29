<template>
    <div>
        <b-card no-body>
            <b-tabs pills card>
                <b-tab title="A VALIDER" active><b-card-text><ValidationUser/></b-card-text></b-tab>
                <b-tab title="Tous les utilisateurs"><b-card-text>Tab contents 2</b-card-text></b-tab>
            </b-tabs>
        </b-card>
    </div>
</template>

<script>
import ValidationUser from '@/components/Admin/ValidationUser.vue'

export default {
  name: 'Validation',
  components: {
    ValidationUser
  }
}
</script>