from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from app import db, models
from app.models import Utilisateurs

class ValidationAdminResource(Resource):
    """
        Get tous les utilisateurs dont il faut valider le compte
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON représentant tous les utilisateurs
            404:
                description: Il n'y a aucun utilisateurs à valider
        """
    def get(self) -> List:
        result = db.session.query(Utilisateurs).filter(Utilisateurs.valide == False)
        if result.count() == 0:
            return {'status':404, 'message':'Il n\'y a aucun compte à valider.'}
        else:
            #print(result)
            users = []
            for row in result:
                user = {}
                user['nom'] = row.nom
                user['prenom'] = row.prenom
                user['mail'] = row.mail
                user['droit'] = row.droit
                user['groupe'] = row.id_groupe
                user['id_utilisateur'] = row.id
                users.append(user)
            return {'data':users,'status':200, 'message':'Vous avez récupéré les utilisateurs à valider'}

class ValidationAdminResourceById(Resource):
    """
        Delete un utilisateur dont on ne veut pas valider le compte
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_user
              description: id de l'utilisateur à supprimer
              required: true
              type: string
        responses:
            200:
                description: Si l'élève a bien été supprimé
            404:
                description: Si l'élève à supprimer n'existe pas en BDD
        """
    def delete(self,id_user):
        if(not check_user_exists(id_user)):
            return {'status':404,'message':'Cet utilisateur n\'existe pas'}
        else:
            db.session.query(Utilisateurs).filter(Utilisateurs.id == id_user).delete()
            db.session.commit()
        #Retourne un status 200 OK, successful HTTP request avec un message de confirmation de suppression de l'utilisateur. 
        #Côté front, si retour status = 200, afficher message et rediriger vers get de tous les utilisateurs à valider, pour mettre à jour la liste. 
        return {'status':200, 'message': 'Vous avez bien supprimé l\'utilisateur !'}

    """
        PATCH pour valider un compte utlisateur en lui attribuant son groupe
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_user
              description: id de l'utilisateur à valider
              required: true
              type: string
        responses:
            200:
                description: JSON avec un message validant la validation du compte utilisateur
            404:
                description: Si le compte n'a pas pu être validé
        """
    def patch(self,id_user):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id_groupeutilisateur', type=str, required=False, help="Missing the user group")
        args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
        print(args['id_groupeutilisateur'])
        #récupère le user 
        user = Utilisateurs.query.filter(Utilisateurs.id == id_user).first()
        print(user.nom)

        try:
            if(user.droit == "Professeur"):
                db.session.query(Utilisateurs).filter(Utilisateurs.id == id_user).update({Utilisateurs.valide : True}, synchronize_session=False)
                db.session.commit()
            else:
                id_groupe = args['id_groupeutilisateur']
                db.session.query(Utilisateurs).filter(Utilisateurs.id == id_user).update({Utilisateurs.id_groupe: id_groupe, Utilisateurs.valide : True}, synchronize_session=False)
                db.session.commit()
            return {'status':200, 'message': 'Vous avez bien validé l\'utilisateur !'}

        except:
            abort(400)


def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists

