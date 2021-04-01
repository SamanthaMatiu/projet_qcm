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
                Listeqcm.append({'id':qcm.id,'titre':qcm.titre,'date_debut':qcm.date_debut.strftime('%d/%m/%Y %H:%M')})
            return Listeqcm
        except:
            abort(400)

class ListACorriger(Resource):
    @token_verif
    def get(user,self):
        try:
            ListeQcmEleve=[]
            for qcm in user.qcm:
                for qcmeEleve in qcm.eleve :
                    ListeQcmEleve.append({'id':qcm.id,'titre':qcm.titre,'date_debut':qcm.date_debut.strftime('%d/%m/%Y %H:%M'),'statut':qcmeEleve.statut})
            return ListeQcmEleve
        except :
            abort(400)

class ListACorrigerDetails(Resource):
    @token_verif
    def get(user,self,id_qcm,id_eleve):
        try:
            qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).first()
            return get_qcm_eleve(qcmeEleve)
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

