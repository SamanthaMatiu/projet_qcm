from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from datetime import datetime
from app import db,app
from app.models import Qcm,Utilisateurs,Question,Choix,QcmEleve,Groupe, ReponseEleve
from app.resources.Authentification.login import token_verif

class ReponsesQCM(Resource):
    """
        Créé les réponses d'un élève à un qcm
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON avec un message validant la prises en charge des réponses de l'élève
            404: 
                description: JSON avec un message pour dire que l'élève a déjà répondu au qcm
        """  
    @token_verif
    def post(user,self):
        datas=request.get_json()
        try:

            # Récupère l'id de l'élève 
            id=user.id

            # Récupère les réponses de l'élève
            reponses = datas['réponses']

            #Récupère l'id du qcm
            id_qcm = datas['id']
        
            #Récupère le statut du qcm
            qcm = db.session.query(QcmEleve).filter(QcmEleve.id_qcm == id_qcm, QcmEleve.id_eleve == id).first()
            statut_qcm = qcm.statut
        

            if(statut_qcm == "Fait"):
                return {'status':404,'message':'Vous avez déjà répondu à ce QCM !'}
        
            else:
                # On cherche l'élève avec son id pour établir le lien foreign key dans ReponseEleve
                eleve = db.session.query(Utilisateurs).filter_by(id=id).first()
                
                for reponse in reponses:

                    #Récupère l'id de la question à laquelle l'élève répond 
                    id_question = reponse['id_question']
                    # On cherche l'objet question auquel l'élève répond 
                    q = db.session.query(Question).filter_by(id=id_question).first()

                    #Récupère l'id du choix sélectionné par l'élève
                    id_choix = reponse['id_choix']
                    # On cherche l'objet choix que l'élève a choisi
                    choix_eleve = db.session.query(Choix).filter_by(id=id_choix).first()

                    #Récupère la réponse ouverte de l'élève
                    reponseouv = reponse['reponseouverte']

                    reponseEleve = ReponseEleve(reponseouverte=reponseouv,choix=choix_eleve,utilisateurs=eleve,question=q)
                    db.session.add(reponseEleve)
                    db.session.commit()
                
                db.session.query(QcmEleve).filter(QcmEleve.id_eleve == id, QcmEleve.id_qcm == id_qcm ).update({QcmEleve.statut: "Fait"}, synchronize_session=False)
                db.session.commit()

                return {'status':200,'message':'Vos réponses ont été enregistrées !'}
        except:
            abort(400)

#def already_answer_qcm(eleve_id,question_id):
#    return db.session.query(db.exists().where(ReponseEleve.id_eleve == eleve_id and ReponseEleve.id_question == question_id)).scalar()