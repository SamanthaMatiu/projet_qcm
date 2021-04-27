from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe,ReponseEleve
from app.resources.Authentification.login import token_verif

class QCMFaitResources(Resource):
    """
        Get tous les qcm fait de l'utilisateur connecté
        ---
        tags:
            - Flask API
        responses:
            200:
                description: retourne un tableau contenant les infos des qcm fait sous format json
            404:
                description: 
        """
    @token_verif
    def get(user,self):
        try :
            list_qcm_fait =  []
            qcm_eleve=QcmEleve.query.filter(QcmEleve.id_eleve == user.id).all()
            
            for qcm in qcm_eleve:

                if(qcm.statut == "Fait"):

                    qcm_fait=Qcm.query.filter_by(id=qcm.id_qcm).first()
                    res = get_qcm_fait_titre(qcm_fait,user.id)
                    list_qcm_fait.append(res)

            return list_qcm_fait
            
        except:
            abort(400)

class QCMFaitQuestionsResources(Resource):
    """
        Get tous les qcm fait de l'utilisateur connecté
        ---
        tags:
            - Flask API
        responses:
            200:
                description: retourne un tableau contenant les qcm (infos+questions) fait sous format json
            404:
                description: 
        """
    @token_verif
    def get(user,self,id_qcm_fait):
        try:
            if(check_qcm_fait_exists(id_qcm_fait)):
        
                qcm_fait=Qcm.query.filter(Qcm.id == id_qcm_fait).first()
                print(qcm_fait)
                res = get_qcm_fait(qcm_fait,user.id)
    
                return res
            else:
                return {"message":"L\'id du qcm à faire est incorrect"}

        except:
            abort(400)







def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists

def check_qcm_fait_exists(id_qcm:int):
    qcm_fait_already_exists = db.session.query(db.exists().where(QcmEleve.id_qcm == id_qcm and QcmEleve.statut == "Fait")).scalar()
    return qcm_fait_already_exists

def get_qcm_fait_titre(qcm,id_eleve):
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M')
    jsonqcm_fait = {'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur}
    return jsonqcm_fait

def get_qcm_fait(qcm,id_eleve):
    questions=[]
    Listreponse=[]
    for question in qcm.questions:
        Listchoix=[]
        for choix in question.choix:
            Listchoix.append({'id':choix.id,'choix':choix.intitule,'true':choix.estcorrect})
        temp={'id': question.id ,'titre':question.intitule,'ouverte':question.ouverte,'choix':Listchoix}
        questions.append(temp)

        reponse = db.session.query(ReponseEleve).filter(ReponseEleve.id_question == question.id, ReponseEleve.id_eleve == id_eleve).first()
        if (reponse.id_choix != None):
            choix_reponse = db.session.query(Choix).filter(Choix.id == reponse.id_choix).first()
            choix = choix_reponse.intitule
        else:
            choix = ""
        r = {'id':reponse.id,'id_choix':reponse.id_choix,'choix':choix,'reponseouverte':reponse.reponseouverte,'question':reponse.id_question}
        Listreponse.append(r)
    
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M')
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur,'questions':questions,'reponses':Listreponse}
    return jsonqcm