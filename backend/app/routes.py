from app import api
from app.resources.Authentification.login import LoginResource
from app.resources.Authentification.register import RegisterResource
from app.resources.Admin.validationadmin import ValidationAdminResource, ValidationAdminResourceById
from app.resources.Admin.gestiongroupe import GestionGroupeResource,GestionGroupeById, GestionGroupeByEleveId, ElevesValidesResource, ProfesseursValidesResource, GestionGroupeManyEleves
from app.resources.qcm import QCMRessources,QCMRessourcesById,GestionQuestion,GestionQuestionById,RetraitDroitQCM
from app.resources.Prof.gestionqcmprof import QCMProf,ListDesQCMS,CorrectionDunQCM,CorrectionQuestionOuverte,ListQCMFait,ListQCMFaitParExam
from app.resources.Eleve.qcmafaire import QCMaFaireResources, QMCaFaireQuestionsResources
from app.resources.Eleve.qcmfait import QCMFaitResources, QCMFaitQuestionsResources,ListQCMCorrige
from app.resources.Eleve.postqcmeleve import ReponsesQCM
from app.resources.Eleve.noteqcmEleve import NoteQCMEleve
from app.resources.Prof.noteqcmProf import NoteQCMProf, ListQCMCorrigeParExam, ListQCMCorrigeProf

# login
api.add_resource(LoginResource, '/api/login')

#qcms
api.add_resource(QCMRessources,'/api/qcm') ## post/patch un qcm
api.add_resource(QCMRessourcesById,'/api/qcm/<int:id_qcm>') ##get /delete un qcm
api.add_resource(QCMProf,'/api/qcmProf') ## get qcm d'un prof
api.add_resource(ListDesQCMS,'/api/consultation') ##  get tout les qcms crée par l'utilisateur
api.add_resource(ListQCMFait,'/api/listQCM') ## get qcmEleve de l'utilisateur 
api.add_resource(ListQCMFaitParExam,'/api/listQCM/<int:id_qcm>') ## get qcmEleve du QCM concerné
api.add_resource(NoteQCMProf,'/api/NoteQcmFait/<int:id_qcm>/<int:id_eleve>') ## get detail + corrigé du qcmEleve de l'eleve

##Correcion qcms prof 
api.add_resource(CorrectionDunQCM,'/api/correction/<int:id_qcm>/<int:id_eleve>') ##post = correction auto / ## get pas utils mais retourne note  + question ouvertes / patch change statut a corrigé 
api.add_resource(CorrectionQuestionOuverte,'/api/correctionQuestionOuverte/<int:id_eleve>/<int:id_question>') ## post change note d'une question ouverte

#Consultation QCM Corrigé Prof
api.add_resource(ListQCMCorrigeProf,'/api/qcmCorriges')
api.add_resource(ListQCMCorrigeParExam,'/api/qcmCorriges/<int:id_qcm>')

##modif questions qcms 
api.add_resource(GestionQuestion,'/api/creationQuestions') ## post creer un question pour le qcm x 
api.add_resource(GestionQuestionById,'/api/ModifQuestions/<int:id_question>') ## patch modifie les question du qcm x / delete supprime la question
api.add_resource(RetraitDroitQCM,'/api/retraitDroits/<int:id_qcm>/<int:id_eleve>')
# Create an account
api.add_resource(RegisterResource,'/api/register')

#Gestion des groupes
api.add_resource(ElevesValidesResource,'/api/elevesvalides')
api.add_resource(ProfesseursValidesResource,'/api/professeursvalides')
api.add_resource(GestionGroupeResource,'/api/groupes')
api.add_resource(GestionGroupeById,'/api/groupes/<int:id_groupe>')
api.add_resource(GestionGroupeByEleveId,'/api/groupesutilisateurs/<int:id_eleve>')
api.add_resource(GestionGroupeManyEleves,'/api/groupesmanyusers')

# Validate an account
api.add_resource(ValidationAdminResource,'/api/validation')
api.add_resource(ValidationAdminResourceById,'/api/validation/<int:id_user>')


#qcms à faire élèves
api.add_resource(QCMaFaireResources,'/api/qcmaFaireInfos')
api.add_resource(QMCaFaireQuestionsResources,'/api/qcmaFaire/<int:id_qcm_a_faire>')

#réponses à un qcm
api.add_resource(ReponsesQCM,'/api/qcmReponses')

#qcms fait élèves
api.add_resource(QCMFaitResources,'/api/qcmFaitInfos')
api.add_resource(QCMFaitQuestionsResources,'/api/qcmFait/<int:id_qcm_fait>')
api.add_resource(NoteQCMEleve,'/api/NoteQcmFait/<int:id_qcm>')## retourne la note + detail du qcmEleve de l'elebe
api.add_resource(ListQCMCorrige,'/api/qcmCorrigeInfos')