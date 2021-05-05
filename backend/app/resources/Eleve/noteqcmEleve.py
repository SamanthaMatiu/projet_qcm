from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe, ReponseEleve
from app.resources.Authentification.login import token_verif

class NoteQCMEleve(Resource):
    @token_verif
    def get(user,self,id_qcm):
        try:
            id_eleve=user.id
            qcmeEleve=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).first()
            noteglobale=get_Note(qcmeEleve)
            baremeTotal=get_Bareme(id_qcm)
            questions=get_qcm_choix_eleve(qcmeEleve)
            conversion=round((20/baremeTotal)*noteglobale,2)
            jsonqcm={'titre':qcmeEleve.qcm.titre,'note':noteglobale,'baremeTotal':baremeTotal,'conversionSur20':conversion,'questions':questions}
            return(jsonqcm)
        except :
            db.session.commit()
            abort(400)

def get_Note(Qcmeleve):
    id_qcm=Qcmeleve.qcm.id
    id_eleve=Qcmeleve.utilisateurs
    contenairetempo={}
    for reponse in id_eleve.reponseleve:
        if reponse.question.id_qcm == id_qcm :
            idq=reponse.question.id
            if( not (idq in contenairetempo)):
                contenairetempo[idq]=True
            if (reponse.note==0 or reponse.note==None) :
                contenairetempo[idq]=False    
    note=0
    for answer in contenairetempo:
        if (contenairetempo[answer]==True):
            question=db.session.query(Question).filter_by(id=answer).first()
            note+=question.bareme
    return (note)

def get_Bareme(id_qcm):
    qcm=db.session.query(Qcm).filter_by(id=id_qcm).first()
    bareme=0
    for question in qcm.questions:
        bareme+=question.bareme
    return (bareme)

## renvoie tout le qcm 
def get_qcm_choix_eleve(Qcmeleve):
    qcm=Qcmeleve.qcm
    questions=qcm.questions
    id_eleve=Qcmeleve.utilisateurs.id
    listequestion=[]
    for question in questions:
        Listchoix={}
        note=question.bareme
        if not(question.ouverte):
            for choix in question.choix:
                Listchoix[choix.id]={'intitule':choix.intitule,'estCorrect':choix.estcorrect,'estChoisi':False}
                reponsEleve=db.session.query(ReponseEleve).filter_by(id_question=question.id,id_eleve=id_eleve)
                for repons in reponsEleve:
                    ch=repons.choix
                    Listchoix[ch.id]={'intitule':ch.intitule,'estCorrect':ch.estcorrect,'estChoisi':True}
                    if(ch.estcorrect==0):
                        note=0
            listequestion.append({'intitule':question.intitule,'bareme':question.bareme,'note':note,'estOuverte':False,'reponseOuverte':"",'choix':Listchoix})
        else :
            rep=db.session.query(ReponseEleve).filter_by(id_question=question.id,id_eleve=id_eleve).first()
            listequestion.append({'intitule':question.intitule,'bareme':question.bareme,'note':rep.note,'estOuverte':True,'reponseOuverte':rep.reponseouverte,'choix':""})
    return(listequestion)
