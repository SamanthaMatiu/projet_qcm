from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe, ReponseEleve
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
            db.session.rollback()
            db.session.commit()
            abort(400)

class ListACorriger(Resource):
    @token_verif
    def get(user,self):
        try:
            ListeQcmEleve=[]
            for qcm in user.qcm:
                for qcmeEleve in qcm.eleve :
                    ListeQcmEleve.append({'id qcm':qcm.id,'id eleve':qcmeEleve.id_eleve,'titre':qcm.titre,'date_debut':qcm.date_debut.strftime('%d/%m/%Y %H:%M'),'statut':qcmeEleve.statut})
            return ListeQcmEleve
        except :
            db.session.commit()
            abort(400)

class ListACorrigerDetails(Resource):
    @token_verif
    def get(user,self,id_qcm,id_eleve):
        try:
            qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).first()
            return get_qcm_eleve(qcmeEleve)
        except :
            abort(400)

class CorrectionDunQCM(Resource):
    @token_verif
    def post(user,self,id_qcm,id_eleve):
        try:
            qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).first()
            return correction(qcmeEleve)
        except :
            db.session.rollback()
            db.session.commit()
            abort(400)

    @token_verif
    def get(user,self,id_qcm,id_eleve):
        try:
            qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).first()
            return get_Corrige(qcmeEleve)
        except :
            db.session.commit()
            abort(400)

class CorrectionQuestionOuverte(Resource):
    @token_verif
    def post(user,self,id_eleve,id_question):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('correction', type=str, required=True, help="La correction svp")
        args = body_parser.parse_args(strict=True)
        try:
            correction=args['correction']
            Reponse=db.session.query(ReponseEleve).filter_by(id_question=id_question,id_eleve=id_eleve).first()
            if(correction):
                Reponse.note=Reponse.question.bareme
            else:
                Reponse.note=0
            return("Question corrigée")
        except :
            db.session.rollback()
            db.session.commit()
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
    id_qcm=Qcmeleve.qcm.id
    id_eleve=Qcmeleve.utilisateurs
    questionreponses=[]
    for reponse in id_eleve.reponseleve:
        if reponse.question.id_qcm == id_qcm :
            if (reponse.reponseouverte == None) :
                questionreponse={'question':reponse.question.intitule,'reponse':reponse.choix.intitule,'estCorrect':reponse.choix.estcorrect,'bareme':reponse.question.bareme,'id_question':reponse.question.id}
            else :
                questionreponse={'question':reponse.question.intitule,'reponse':reponse.reponseouverte,'bareme':reponse.question.bareme,'id_question':reponse.question.id}
            questionreponses.append(questionreponse)
    return questionreponses

def correction(Qcmeleve):
    id_qcm=Qcmeleve.qcm.id
    id_eleve=Qcmeleve.utilisateurs
    for reponse in id_eleve.reponseleve:
        if reponse.question.id_qcm == id_qcm :
            if (reponse.reponseouverte == None) :
                if (reponse.choix.estcorrect == 1 and reponse.note != 0):
                    reponse.note=1
                else : 
                    reponse.note=0
    db.session.commit()
    return ("QCM corrigé")

def get_Corrige(Qcmeleve):
    id_qcm=Qcmeleve.qcm.id
    id_eleve=Qcmeleve.utilisateurs
    corrige={}
    corrige[0]=0
    contenairetempo={}
    i=1
    for reponse in id_eleve.reponseleve:
        if reponse.question.id_qcm == id_qcm :
            idq=reponse.question.id
            if (reponse.reponseouverte == None) :
                if( not (idq in contenairetempo)):
                    contenairetempo[idq]=True
                if (reponse.choix.estcorrect == 0) :
                    contenairetempo[idq]=False                
            else :
                corrige[i]=({'question':reponse.question.intitule,'reponse':reponse.reponseouverte,'bareme':reponse.question.bareme,'id_question':reponse.question.id})
                i+=1
    note=0
    for answer in contenairetempo:
        if (contenairetempo[answer]==True):
            corrige[0]+=1
    return (corrige)