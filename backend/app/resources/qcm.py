from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix

class QCMRessources(Resource):
    def get(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id',type=int,required=True,help="Pas d'identifiants renseigné.")
        args=body_parser.parse_args(strict=True)
        try :
            qcm=Qcm.query.filter_by(id=args['id']).first()
            get_qcm(qcm)
            return 1
        except:
            abort(400)

    def post(self):
        datas=request.get_json()
        try:
            titre=datas['titre']
            debut=datetime.strptime(datas['date_debut'],"%d/%m/%Y %H:%M")
            fin=datetime.strptime(datas['date_fin'],"%d/%m/%Y %H:%M")
            id=datas['id_prof']
            
            ## Si le qcm existe déjà on ne le recréer pas.
            if(exist_qcm(titre,debut,fin,id)):
                return {'status':404,'message':'Le QCM existe déjà.'}

            ## On cherche le prof pour établir le lien foreign key
            prof=Utilisateurs.query.filter_by(id=id).first()

            ##création du QCM
            QCM=Qcm(titre=titre,date_debut=debut,date_fin=fin,utilisateurs=prof)
            creation_question(datas['questions'],QCM)

            db.session.add(QCM)
            db.session.commit()
            return {'status':201,'message':'QCM créé avec succès !'}
        except:
            abort(400)

def exist_qcm(titre,debut,fin,id_prof):
    exist=Qcm.query.filter_by(titre=titre,date_debut=debut,date_fin=fin,id_professeur=id_prof).first()
    return exist

def creation_question(data,QCM):
    for questionChoix in data:
        for x in questionChoix:
            if questionChoix[x]['ouverte']==0:
                ouverte=False
            else :
                ouverte=True
            question=Question(intitule=questionChoix[x]['titre'],ouverte=ouverte,qcm=QCM)
            db.session.add(question)
            db.session.commit()
            if not (ouverte):
                for y in questionChoix[x]['choix']:
                    choix=Choix(intitule=y['choix'],estcorrect=y['true'],question=question)
                    db.session.add(choix)
                    db.session.commit()
    
def get_qcm(qcm):
    
    for question in qcm.questions:
        print(question)