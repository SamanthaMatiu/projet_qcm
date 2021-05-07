<template>
  <mdb-container>
    <mdb-row>
      <mdb-col sm="5" xl="4">
        <mdb-view hover class="rounded z-depth-1-half mb-lg-0 mb-4">
          <img class="img-fluid" src="https://us.123rf.com/450wm/sabelskaya/sabelskaya1707/sabelskaya170700971/82924635-ensemble-de-crayons-%C3%A0-dessins-anim%C3%A9s-vectoriels-avec-des-bras-et-des-%C3%A9motions-face-en-gardant-le-livre-dan.jpg?ver=6" alt="Sample image" />
            <a @click="goToCreation()">
              <mdb-mask overlay="white-slight" waves/>
            </a>
        </mdb-view>
      </mdb-col>
      <mdb-col sm="7" xl="8">
        <h3 class="font-weight-bold mb-3 p-0">
          <strong>Mes QCMs à faire</strong>
        </h3>
        <p class="dark-grey-text">Viens voir si des QCMs t'attendent !</p>
        <mdb-btn color="primary" size="md" @click="goToCreation()">Je veux voir les QCMs a faire</mdb-btn>
      </mdb-col>
    </mdb-row>
    <hr class="my-5" />
    <mdb-row>
      <mdb-col sm="5" xl="4">
        <mdb-view hover class="rounded z-depth-1-half mb-lg-0 mb-4">
          <img class="img-fluid" src="https://image.freepik.com/vecteurs-libre/crayon-dessin-anime_1262-14787.jpg" alt="Sample image" />
          <a @click="goToConsultation()">
            <mdb-mask overlay="white-slight" waves/>
          </a>
        </mdb-view>
      </mdb-col>
      <mdb-col sm="7" xl="8">
        <h3 class="font-weight-bold mb-3 p-0">
          <strong>Mes QCMs en cours de correction</strong>
        </h3>
        <p class="dark-grey-text">Tu peux voir tous les QCMs que tu as fait et qui ne sont malheureusement pas encore corrigés mais tu peux revenir revoir tes réponses !</p>
        <mdb-btn color="primary" size="md" @click="goToConsultation()">Je veux voir les QCMs en cours de correction</mdb-btn>
      </mdb-col>
    </mdb-row>
    <hr class="my-5" />
    <mdb-row>
      <mdb-col sm="5" xl="4">
        <mdb-view hover class="rounded z-depth-1-half mb-lg-0 mb-4">
          <img class="img-fluid" src="https://image.freepik.com/vecteurs-libre/personnages-crayon-mignons-qui-ont-idees-confusion_161751-270.jpg" alt="Sample image" />
          <a @click="goToCorrection()">
            <mdb-mask overlay="white-slight" waves/>
          </a>
        </mdb-view>
      </mdb-col>
      <mdb-col sm="7" xl="8">
        <h3 class="font-weight-bold mb-3 p-0">
          <strong>Mes QCMs corrigés</strong>
        </h3>
        <p class="dark-grey-text">Pense à venir ici de temps en temps pour voir les résultats de tes QCMs qui ont été corrigés !</p>
        <mdb-btn color="primary" size="md" @click="goToCorrection()">Je veux voir les QCMs corrigés</mdb-btn>
      </mdb-col>
    </mdb-row>
  </mdb-container>
</template>

<script>
/* eslint-disable vue/no-unused-components */

import Navbar from '@/components/Prof/NavBar.vue'
import { mdbContainer, mdbRow, mdbCol, mdbCard, mdbCardBody, mdbMask, mdbIcon, mdbView, mdbBtn } from 'mdbvue';

export default {
  name: 'Home',
  components: {
    Navbar,
    mdbContainer,
    mdbRow,
    mdbCol,
    mdbCard,
    mdbCardBody,
    mdbMask,
    mdbIcon,
    mdbView,
    mdbBtn
  },
    methods: {
      goToCreation(){
        this.$router.push({ name: 'QcmsAFaire' });
      },
      goToConsultation(){
        this.$router.push({ name: 'QcmsFait' });
      },
      goToCorrection(){
        this.$router.push({ name: 'QcmsCorriges' });
      }
    }
}
</script>

<style scoped>
.view img, .view video {
    max-height: 250px;
}
</style>