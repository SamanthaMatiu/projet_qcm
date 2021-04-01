from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe
from app.resources.Authentification.login import token_verif


class QCMProf(Resource):

    @token_verif
    def get(user,self):
        try :
            Listeqcm=[]
            qcms=db.session.query(Qcm).filter_by(id_professeur=user.id)
            for qcm in qcms:
                Listeqcm.append(get_qcm(qcm))
            return Listeqcm
        except:
            abort(400)

class ListQCMaCorriger(Resource):
    @token_verif
    def get(user,self):
        try:
            ListeQcm=[]
            for qcm in user.qcm:
                resteAcorrige=False
                for qcmeEleve in qcm.eleve :
                    if qcmeEleve.statut=='A faire':
                        resteAcorrige=True
                if(resteAcorrige):
                    ListeQcm.append({'id':qcm.id,'titre':qcm.titre,'date_debut':qcm.date_debut.strftime('%d/%m/%Y %H:%M')})
            return ListeQcm
        except :
            abort(400)

class ListQCMaCorrigerById(Resource):
    @token_verif
    def get(user,self,id_qcm):
        try:
            ListeQcmEleve=[]
            for qcm in user.qcm:
                for qcmeEleve in qcm.eleve :
                    if qcmeEleve.statut=='A faire':
                        ListeQcmEleve.append({'id':qcm.id,'titre':qcm.titre,'eleve':qcmeEleve.utilisateurs})
            return ListeQcmEleve
        except :
            abort(400)

class ListACorriger(Resource):
    @token_verif
    def get(user,self):
        try:
            ListeQcmEleve=[]
            for qcm in user.qcm:
                for qcmeEleve in qcm.eleve :
                    if qcmeEleve.statut=='A faire':
                        ListeQcmEleve.append(get_qcm_eleve(qcmeEleve))

            return ListeQcmEleve
        except :
            abort(400)

def get_qcm(qcm):
    questions=[]
    for question in qcm.questions:
        Listchoix=[]
        for choix in question.choix:
            Listchoix.append({'id':choix.id,'choix':choix.intitule,'true':choix.estcorrect})
        temp={'id': question.id ,'titre':question.intitule,'ouverte':question.ouverte,'choix':Listchoix}
        questions.append(temp)
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M')
    Listusers=[]
    for eleve in qcm.eleve:
        Listusers.append({'id':eleve.utilisateurs.id})
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleves':Listusers,'id_prof':qcm.id_professeur,'questions':questions}
    return jsonqcm

def get_qcm_eleve(Qcmeleve):
    id_qcm=QcmEleve.id_qcm
    id_eleve=Qcmeleve.utilisateurs
    questionreponse=[]
    for reponse in id_eleve.reponseleve:
        if reponse.question.id_qcm==id_qcm :
            if reponse.reponseouverte != none :
                questionreponse={'question':reponse.question.intitule,'reponse':reponse.reponseouverte}
            else :
                questionreponse={'question':reponse.question.intitule,'reponse':reponse.id_choix,'estCorrect':reponse.choix.estcorrect}
            qcmEleve.append(questionreponse)
    return questionreponse

