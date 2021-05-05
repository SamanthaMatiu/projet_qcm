from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe
from app.resources.Authentification.login import token_verif

class QCMaFaireResources(Resource):
    """
        Get tous les qcm à faire de l'utilisateur connecté
        ---
        tags:
            - Flask API
        responses:
            200:
                description: retourne un tableau contenant les infos qcm à faire sous format json
            404:
                description: 
        """
    @token_verif
    def get(user,self):
        try :
            list_qcm_a_faire =  []
            qcm_eleve=QcmEleve.query.filter(QcmEleve.id_eleve == user.id).all()
            
            for qcm in qcm_eleve:

                if(qcm.statut == "A faire"):
                    
                    qcm_a_faire=Qcm.query.filter_by(id=qcm.id_qcm).first()

                    now = datetime.now()

                    if((qcm_a_faire.date_debut < now) and (now < qcm_a_faire.date_fin)):
                        res = get_qcm_a_faire_titre(qcm_a_faire,user.id)
                        list_qcm_a_faire.append(res)

            return list_qcm_a_faire
            
        except:
            abort(400)

class QMCaFaireQuestionsResources(Resource):
    """
        Get tous les qcm à faire de l'utilisateur connecté
        ---
        tags:
            - Flask API
        responses:
            200:
                description: retourne un tableau contenant les qcm (infos+questions) à faire sous format json
            404:
                description: 
        """
    @token_verif
    def get(user,self,id_qcm_a_faire):
        try:
            if(check_qcm_a_faire_exists(id_qcm_a_faire)):
                qcm_a_faire=Qcm.query.filter(Qcm.id == id_qcm_a_faire).first()
                res = get_qcm_a_faire(qcm_a_faire,user.id)
    
                return res
            else:
                return {"message":"L\'id du qcm à faire est incorrect"}

        except:
            abort(400)







def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists

def check_qcm_a_faire_exists(id_qcm:int):
    qcm_a_faire_already_exists = db.session.query(db.exists().where(QcmEleve.id_qcm== id_qcm and QcmEleve.statut ==" A faire")).scalar()
    return qcm_a_faire_already_exists

def get_qcm_a_faire_titre(qcm,id_eleve):
  
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M:%S')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M:%S')
    jsonqcm_a_faire = {'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur}
    return jsonqcm_a_faire

def get_qcm_a_faire(qcm,id_eleve):
    questions=[]
    for question in qcm.questions:
        Listchoix=[]
        for choix in question.choix:
            Listchoix.append({'id':choix.id,'choix':choix.intitule,'true':choix.estcorrect})
        temp={'id': question.id ,'titre':question.intitule,'ouverte':question.ouverte,'choix':Listchoix}
        questions.append(temp)
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M:%S')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M:%S')
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur,'questions':questions}
    return jsonqcm