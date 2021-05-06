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
                qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=user.id,id_qcm=id_qcm_fait).first()
                res = get_qcm_fait(qcmeEleve)
    
                return res
            else:
                return {"message":"L\'id du qcm à faire est incorrect"}

        except:
            abort(400)

class ListQCMCorrige(Resource):
    @token_verif
    def get(user,self):
        try:
            ListeQcmEleve=[]
            qcm_eleve = QcmEleve.query.filter(QcmEleve.id_eleve == user.id).all()
       
            for qcm in qcm_eleve:
                if(qcm.statut == "Corrigé"):
                    qcm_corrige=Qcm.query.filter_by(id=qcm.id_qcm).first()
                    res = get_qcm_fait_titre(qcm_corrige,user.id)
                    ListeQcmEleve.append(res)

            return ListeQcmEleve
        except :
            db.session.rollback()
            db.session.commit()
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

def get_qcm_fait(Qcmeleve):
    qcm=Qcmeleve.qcm
    questions=qcm.questions
    id_eleve=Qcmeleve.utilisateurs.id
    listequestion=[]
    for question in questions:
        Listchoix={}
        if not(question.ouverte):
            for choix in question.choix:
                Listchoix[choix.id]={'intitule':choix.intitule,'estCorrect':choix.estcorrect,'estChoisi':False}
                reponsEleve=db.session.query(ReponseEleve).filter_by(id_question=question.id,id_eleve=id_eleve)
                for repons in reponsEleve:
                    ch=repons.choix
                    Listchoix[ch.id]={'intitule':ch.intitule,'estCorrect':ch.estcorrect,'estChoisi':True}
            listequestion.append({'intitule':question.intitule,'bareme':question.bareme,'estOuverte':False,'reponseOuverte':"",'choix':Listchoix})
        else :
            rep=db.session.query(ReponseEleve).filter_by(id_question=question.id,id_eleve=id_eleve).first()
            listequestion.append({'intitule':question.intitule,'bareme':question.bareme,'estOuverte':True,'reponseOuverte':rep.reponseouverte,'choix':""})    
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M')
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur,'questions':listequestion}
    return jsonqcm