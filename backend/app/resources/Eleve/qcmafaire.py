from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe
from app.resources.Authentification.login import token_verif

class QCMaFaireResources(Resource):
    @token_verif
    def get(user,self):
        try :
            
            qcm_eleve=db.session.query(QcmEleve).filter_by(id_eleve = user.id).first()
            
            print(qcm_eleve)
            return qcm_eleve.id_eleve
        except:
            abort(400)




def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists


def get_qcm(qcm,id_eleve):
    questions=[]
    for question in qcm.questions:
        Listchoix=[]
        for choix in question.choix:
            Listchoix.append({'id':choix.id,'choix':choix.intitule,'true':choix.estcorrect})
        temp={'id': question.id ,'titre':question.intitule,'ouverte':question.ouverte,'choix':Listchoix}
        questions.append(temp)
    date_debut=qcm.date_debut.strftime('%d/%m/%Y %H:%M')
    date_fin=qcm.date_fin.strftime('%d/%m/%Y %H:%M')
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleve':id_eleve,'id_prof':qcm.id_professeur,'questions':questions}
    return jsonqcm