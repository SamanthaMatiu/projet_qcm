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
          <strong>Création d'un qcm</strong>
        </h3>
        <p class="dark-grey-text">Tu peux créer plein de super QCM - blablabla - youpii</p>
        <mdb-btn color="primary" size="md" @click="goToCreation()">Je veux créer un qcm</mdb-btn>
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
          <strong>Gestion de mes qcm</strong>
        </h3>
        <p class="dark-grey-text">Tu peux voir touuuut les petis qcms que tu as créé ici - blablabla - N'hésites pas à les modifier ou en supprimer si tu as fait une connerie</p>
        <mdb-btn color="primary" size="md" @click="goToConsultation()">Je veux voir mes qcms</mdb-btn>
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
          <strong>Correction des qcm</strong>
        </h3>
        <p class="dark-grey-text">Penses à venir ici de temps en temps pour corriger les qcm de tes élèves - blablabla - Tes élèves sont impatients</p>
        <mdb-btn color="primary" size="md" @click="goToCorrection()">Je veux faire une correction</mdb-btn>
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
        this.$router.push({ name: 'CreationQcm' });
      },
      goToConsultation(){
        this.$router.push({ name: 'Consultation' });
      },
      goToCorrection(){
        this.$router.push({ name: 'Correction' });
      }
    }
}
</script>
