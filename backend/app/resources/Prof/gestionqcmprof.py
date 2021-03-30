from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe

class QCMProfRessources(Resource):
    def get(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id_prof',type=int,required=True,help="Pas d'identifiants renseigné.")
        args=body_parser.parse_args(strict=True)
        try :
            Listeqcm=[]
            qcms=db.session.query(Qcm).filter_by(id_professeur=args['id_prof'])
            for qcm in qcms:
                Listeqcm.append(get_qcm(qcm))
            return Listeqcm
        except:
            abort(400)

class ListQCMaCorrigerRessources(Resource):
    def get(self):

        try:
            return 1
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