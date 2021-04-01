from app import api

from app.resources.Authentification.register import RegisterResource
from app.resources.Admin.validationadmin import ValidationAdminResource, ValidationAdminResourceById
from app.resources.qcm import QCMRessources,QCMRessourcesById
from app.resources.Prof.gestionqcmprof import QCMProf,ListQCMaCorriger,ListQCMaCorrigerById,ListACorriger
from app.resources.Admin.gestiongroupe import GestionGroupeResource,GestionGroupeById, GestionGroupeByEleveId, ElevesValidesResource, ProfesseursValidesResource
from app.resources.Eleve.qcmafaire import QCMaFaireResources, QMCaFaireQuestionsResources
from app.resources.Authentification.login import LoginResource
#tests

# login
api.add_resource(LoginResource, '/api/login')

#qcms
api.add_resource(QCMRessources,'/api/qcm')
api.add_resource(QCMRessourcesById,'/api/qcm/<int:id_qcm>')
api.add_resource(QCMProf,'/api/qcmProf')
api.add_resource(ListQCMaCorriger,'/api/qcmAcorriger')
api.add_resource(ListQCMaCorrigerById,'/api/qcmAcorriger/<int:id_qcm>')
api.add_resource(ListACorriger,'/api/correction')

# Create an account
api.add_resource(RegisterResource,'/api/register')

#Gestion des groupes
api.add_resource(ElevesValidesResource,'/api/elevesvalides')
api.add_resource(ProfesseursValidesResource,'/api/professeursvalides')
api.add_resource(GestionGroupeResource,'/api/groupes')
api.add_resource(GestionGroupeById,'/api/groupes/<int:id_groupe>')
api.add_resource(GestionGroupeByEleveId,'/api/groupesutilisateurs/<int:id_eleve>')

# Validate an account
api.add_resource(ValidationAdminResource,'/api/validation')
api.add_resource(ValidationAdminResourceById,'/api/validation/<int:id_user>')


#qcms élèves
api.add_resource(QCMaFaireResources,'/api/qcmaFaireInfos')
api.add_resource(QMCaFaireQuestionsResources,'/api/qcmaFaire/<int:id_qcm_a_faire>')