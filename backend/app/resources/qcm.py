from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe
from app.resources.Authentification.login import token_verif

class QCMRessourcesById(Resource):

    """
        GET pour obtenir un QCM selon son id 
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_qcm
              description: id du QCM
              required: true
              type: int
        responses:
            200:
                description: JSON avec le QCM
            400:
                description: Le qcm n'existe pas
        """
    @token_verif
    def get(user,self,id_qcm):
        try :
            qcm=db.session.query(Qcm).filter_by(id=id_qcm).first()
            return get_qcm(qcm)
        except:
            abort(400)

    """
        DELETE pour qu'un porfesseur supprime un de ses qcms
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_qcm
              description: id du qcm a supprimer
              required: true
              type: int
        responses:
            200:
                description: JSON avec un message qui indique que le qcm a été supprimé
            404:
                description: Si l'utilisateur n'est pas un professeur
            400 :
                description : Le qcm n'existe pas
        """
    @token_verif
    def delete(user,self,id_qcm):
        try :
            ## On récupère le qcm concerné.
            qcm=db.session.query(Qcm).filter_by(id=id_qcm).first()

            ## On delete tout les liens entre ce qcm et les élèves.
            qcmEleve=db.session.query(QcmEleve).filter_by(id_qcm=id_qcm).delete()
            ## Pour chaque questions du QCM
            for question in qcm.questions:
                ## on delete les choix 
                for choi in question.choix :
                    db.session.query(Choix).filter_by(id=choi.id).delete()
                    ## puis on delete la question
                    db.session.query(Question).filter_by(id=question.id).delete()
            ## enfin on delete le QCM
            db.session.query(Qcm).filter_by(id=id_qcm).delete()
            db.session.commit()
            return {'status':200,'message':'Le qcm a bien été supprimé.'}
        except :
            abort (400)

class QCMRessources(Resource): 

    """
        PATCH pour modifier un qcm
        ---
        tags:
            - Flask API
        parameters:
            - in: json
            -parameters : a lot
        responses:
            200:
                description: JSON avec un message validant la modification du qcm
            404:
                description: Si le qcm n'a pas pu être modifié ou si l'utilisateur n'est pas un professeur
        """
    @token_verif  
    def patch(user,self):
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
                qcm.date_debut=datetime.strptime(datas['date_debut'],"%Y-%m-%d %H:%M:%S")
                db.session.commit()
            if datas['date_fin'] != "":
                qcm.date_fin=datetime.strptime(datas['date_fin'],"%Y-%m-%d %H:%M:%S")
                db.session.commit()
                ## changement du groupe 
            if groupe_id != "":
                for groupe in groupe_id:
                    print(groupe)
                    add_groupe_to_qcm(groupe['id'],qcm)

            ## changement de l'élève concerné par le QCM
            if eleve_id != "":
                for eleves in eleve_id:
                    eleve=db.session.query(Utilisateurs).filter_by(id=eleves['id']).first()
                    add_eleve_to_qcm(eleve,qcm)

            ## si on souhaite changer les questions.
            if questions != "":
                for question in questions:
                    ## pour chaque question qu'on souhaite changer on recupere son homologue
                    quest=db.session.query(Question).filter_by(id=question['id']).first()
                    ## on change son titre si désiré
                    if question['titre'] != "":
                        quest.intitule=question['titre']
                    if question['bareme'] != "":
                        quest.bareme=question['bareme']
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
    
    @token_verif
    def post(user,self):
        datas=request.get_json()
        try: 
            titre=datas['titre']
            debut=datetime.strptime(datas['date_debut'],"%Y-%m-%d %H:%M:%S")
            fin=datetime.strptime(datas['date_fin'],"%Y-%m-%d %H:%M:%S")
            id=user.id
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
                for groupe in groupe_id:
                    add_groupe_to_qcm(groupe['id'],QCM)
            else :
                for eleves in eleve_id:
                    eleve=db.session.query(Utilisateurs).filter_by(id=eleves['id']).first()
                    add_eleve_to_qcm(eleve,QCM)
            db.session.add(QCM)
            db.session.commit()
            return {'status':201,'message':'QCM créé avec succès !'}
        except:
            abort(400)

class GestionQuestion(Resource):
    @token_verif
    def post(user,self):
        datas=request.get_json()
        try:
            id_qcm=datas['id_qcm']
            qcm=db.session.query(Qcm).filter_by(id=id_qcm).first()
            creation_quest(datas['question'],qcm)
            return {'status':200,'message':"Question(s) créée(s)."}
        except:
            db.session.rollback()
            db.session.commit()
            abort(400)

class GestionQuestionById(Resource):
    @token_verif
    def patch(user,self,id_question):
        datas=request.get_json()
        try:
            question=datas['question']
            choix=datas['choix']
            ## pour chaque question qu'on souhaite changer on recupere son homologue
            quest=db.session.query(Question).filter_by(id=id_question).first()
            ## on change son titre si désiré
            if question['titre'] != "":
                quest.intitule=question['titre']
            if question['bareme'] != "":
                quest.bareme=question['bareme']
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
                    db.session.query(Choix).filter_by(id_question=id_question).delete()
                db.session.commit()
            
            ## si on veut modifier un choix 
            if choix != "":
                ## Pour chaque choix renseigné 
                for choi in choix :
                    ## on recupère le choix concerné en BDD 
                    value=db.session.query(Choix).filter_by(id=choi['id']).first()
                    ## on change ses attributs
                    if choi['choix'] != "" :
                        value.intitule=choi['choix']
                    if choi['true'] != "":
                        value.estcorrect=choi['true']
                    db.session.commit()
            return {'status':200,'message': 'Les changements ont été effectués.'}
        except:
            db.session.rollback()
            db.session.commit()
            abort(400)

    @token_verif
    def delete(user,self,id_question):
        try:
            q=db.session.query(Question).filter(Question.id==id_question).delete()
            db.session.commit()
            return ("Question supprimée")
        except:
            db.session.rollback()
            db.session.commit()
            abort(400)

class RetraitDroitQCM(Resource):
    @token_verif
    def delete(user,self,id_qcm, id_eleve):
        datas=request.get_json()
        try:
            rep=db.session.query(QcmEleve).filter_by(id_eleve=id_eleve,id_qcm=id_qcm).delete()
            db.session.commit()
            return ("Qcm supprimée")
        except:
            abort(400)

def exist_qcm(titre,debut,fin,id_prof):
    exist=db.session.query(Qcm).filter_by(titre=titre,date_debut=debut,date_fin=fin,id_professeur=id_prof).first()
    return exist

def creation_question(data,QCM):
    for questionChoix in data:
        if questionChoix['ouverte']==0:
            ouverte=False
        else :
            ouverte=True
        question=Question(intitule=questionChoix['titre'],ouverte=ouverte,bareme=questionChoix['bareme'],qcm=QCM)
        db.session.add(question)
        db.session.commit()

        if not (ouverte):
            for y in questionChoix['choix']:
                choix=Choix(intitule=y['choix'],estcorrect=y['true'],question=question)
                db.session.add(choix)
                db.session.commit()

def creation_quest(question,QCM):
    if question['ouverte']==0:
        ouverte=False
    else :
        ouverte=True
    question=Question(intitule=question['titre'],ouverte=ouverte,bareme=question['bareme'],qcm=QCM)
    db.session.add(question)
    db.session.commit()
    if not (ouverte):
        for y in question['choix']:
            choix=Choix(intitule=y['choix'],estcorrect=y['true'],question=question)
            db.session.add(choix)
            db.session.commit()

def get_qcm(qcm):
    questions=[]
    for question in qcm.questions:
        Listchoix=[]
        for choix in question.choix:
            Listchoix.append({'id':choix.id,'choix':choix.intitule,'true':choix.estcorrect})
        temp={'id': question.id ,'titre':question.intitule,'ouverte':question.ouverte,'bareme': question.bareme,'choix':Listchoix}
        questions.append(temp)
    date_debut=qcm.date_debut.strftime('%Y-%m-%d %H:%M')
    date_fin=qcm.date_fin.strftime('%Y-%m-%d %H:%M')
    Listusers=[]
    for eleve in qcm.eleve:
        Listusers.append({'id':eleve.utilisateurs.id,'prenom':eleve.utilisateurs.prenom,'nom':eleve.utilisateurs.nom,'groupe':eleve.utilisateurs.groupe.nom,'id_groupe':eleve.utilisateurs.groupe.id})
    jsonqcm={'id':qcm.id,'titre':qcm.titre,'date_debut':date_debut,'date_fin':date_fin,'id_eleves':Listusers,'id_prof':qcm.id_professeur,'questions':questions}
    return jsonqcm

def add_eleve_to_qcm(eleve,QCM):
    if not(db.session.query(QcmEleve).filter_by(id_eleve=eleve.id,id_qcm=QCM.id).first()):
        qcmEleve=QcmEleve(statut='A faire',utilisateurs=eleve,qcm=QCM)
        db.session.add(qcmEleve)
        db.session.commit()

def add_groupe_to_qcm(groupe_id,QCM):
    groupe=db.session.query(Groupe).filter_by(id=groupe_id).first()
    for eleve in groupe.utilisateurs :
        add_eleve_to_qcm(eleve,QCM)
