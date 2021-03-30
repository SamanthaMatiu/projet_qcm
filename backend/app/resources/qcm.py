from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe

class QCMRessources(Resource):
    def get(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id',type=int,required=True,help="Pas d'identifiants renseigné.")
        args=body_parser.parse_args(strict=True)
        try :
            qcm=db.session.query(Qcm).filter_by(id=args['id']).first()
            return get_qcm(qcm)
        except:
            abort(400)
    
    def delete(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id',type=int,required=True,help="Pas d'identifiants renseigné.")
        args=body_parser.parse_args(strict=True)
        try :
            ## On récupère le qcm concerné.
            qcm=db.session.query(Qcm).filter_by(id=args['id']).first()

            ## On delete tout les liens entre ce qcm et les élèves.
            qcmEleve=db.session.query(QcmEleve).filter_by(id_qcm=args['id']).delete()
            ## Pour chaque questions du QCM
            for question in qcm.questions:
                ## on delete les choix 
                for choi in question.choix :
                    db.session.query(Choix).filter_by(id=choi.id).delete()
                ## puis on delete la question
                db.session.query(Question).filter_by(id=question.id).delete()
            ## enfin on delete le QCM
            db.session.query(Qcm).filter_by(id=args['id']).delete()
            db.session.commit()
            return {'status':200,'message':'Le qcm a bien été supprimé.'}

        except :
            abort (400)
    
    def patch(self):
        datas=request.get_json()
        try:
            id_qcm=datas['id']
            titre=datas['titre']
            groupe_id=datas['droit']['groupe']
            eleve_id=datas['droit']['utilisateur']
            questions=datas['questions']
            choix=datas['choix']
            qcm=db.session.query(Qcm).filter_by(id=id_qcm).first()
            
            ## changement du titre
            if titre != "":
                qcm.titre=titre
                db.session.commit()
            ## changement des horraires/dates
            if datas['date_debut'] != "":
                qcm.date_debut=datetime.strptime(datas['date_debut'],"%d/%m/%Y %H:%M")
                db.session.commit()

            if datas['date_fin'] != "":
                qcm.date_fin=datetime.strptime(datas['date_fin'],"%d/%m/%Y %H:%M")
                db.session.commit()

            ## changement du groupe 
            if groupe_id != "":
                db.session.query(QcmEleve).filter_by(id_qcm=qcm.id).delete()
                add_groupe_to_qcm(groupe_id,qcm)

            ## changement de l'élève concerné par le QCM
            if eleve_id != "":
                db.session.query(QcmEleve).filter_by(id_qcm=qcm.id).delete()
                eleve=db.session.query(Utilisateurs).filter_by(id=eleve_id).first()
                add_eleve_to_qcm(eleve,qcm)

            ## si on souhaite changer les questions.
            if questions != "":
                for question in questions:
                    ## pour chaque question qu'on souhaite changer on recupere son homologue
                    quest=db.session.query(Question).filter_by(id=question['id']).first()
                    ## on change son titre si désiré
                    if question['titre'] != "":
                        quest.intitule=question['titre']
                    ## si on souhaite changer le type de question.
                    if question['ouverte'] != "":
                        ## si on passe d'une question ouverte a fermé
                        if question['ouverte'] == 0:
                            if quest.ouverte !=0:
                                quest.ouverte=0
                                ## On ajoute les choix a la question
                                for choose in question['choix']: 
                                    choixQuestion=Choix(intitule=choose['titre'],estcorrect=choose['estcorrect'],question=quest)
                                    db.session.add(choixQuestion)
                                    db.session.commit()
                                db.session.commit()
                        else:
                            ## si on passe d'une question fermée a une question ouverte
                            quest.ouverte=1
                            ## on supprime les choix liées
                            db.session.query(Choix).filter_by(id_question=question['id']).delete()
                        db.session.commit()
            
            ## si on veut modifier un choix 
            if choix != "":
                ## Pour chaque choix renseigné 
                for choi in choix :
                    ## on recupère le choix concerné en BDD 
                    value=db.session.query(Choix).filter_by(id=choi['id']).first()
                    ## on change ses attributs
                    if choi['intitule'] != "" :
                        value.intitule=choi['intitule']
                    if choi['estcorrect'] != "":
                        value.estcorrect=choi['estcorrect']
                    db.session.commit()
            return {'status':200,'message': 'Les changements ont été effectués.'}
        except:
            abort(400)

    def post(self):
        datas=request.get_json()
        try:
            titre=datas['titre']
            debut=datetime.strptime(datas['date_debut'],"%d/%m/%Y %H:%M")
            fin=datetime.strptime(datas['date_fin'],"%d/%m/%Y %H:%M")
            id=datas['id_prof']
            groupe_id=datas['droit']['groupe']
            eleve_id=datas['droit']['utilisateur']
            ## Si le qcm existe déjà on ne le recréer pas.
            if(exist_qcm(titre,debut,fin,id)):
                return {'status':404,'message':'Le QCM existe déjà.'}

            ## On cherche le prof pour établir le lien foreign key
            prof=db.session.query(Utilisateurs).filter_by(id=id).first()
            ##création du QCM
            QCM=Qcm(titre=titre,date_debut=debut,date_fin=fin,utilisateurs=prof)
            creation_question(datas['questions'],QCM)
            ## On ajoute les élèves d'un groupe ou un élève seulement
            if groupe_id != "":
                add_groupe_to_qcm(groupe_id,QCM)
            else :
                eleve=db.session.query(Utilisateurs).filter_by(id=eleve_id).first()
                add_eleve_to_qcm(eleve,QCM)
            
            db.session.add(QCM)
            db.session.commit()
            return {'status':201,'message':'QCM créé avec succès !'}
        except:
            abort(400)

def exist_qcm(titre,debut,fin,id_prof):
    exist=db.session.query(Qcm).filter_by(titre=titre,date_debut=debut,date_fin=fin,id_professeur=id_prof).first()
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

def add_eleve_to_qcm(eleve,QCM):
    qcmEleve=QcmEleve(statut='A faire',utilisateurs=eleve,qcm=QCM)
    db.session.add(qcmEleve)
    db.session.commit()

def add_groupe_to_qcm(groupe_id,QCM):
    groupe=db.session.query(Groupe).filter_by(id=groupe_id).first()
    for eleve in groupe.utilisateurs :
        add_eleve_to_qcm(eleve,QCM)

