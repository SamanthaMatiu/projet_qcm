from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from app import db, models
from app.models import Utilisateurs, Groupe

class UtilsateursValidesResource(Resource):
    """
    Get tous les utilisateurs dont le compte a déjà été validé
    ---
    tags:
        - Flask API
    responses:
        200:
            description: JSON représentant tous les utilisateurs
        404:
            description: Il n'y a aucun utilisateur déjà validé
    """
        
    def get(self) -> List:
        result = db.session.query(Utilisateurs).filter(Utilisateurs.valide == True)
        if result.count() == 0:
            return {'status':404, 'message':'Il n\'y a aucun utilisateur déjà validé.'}
        else:
            print(result)
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
            return {'data':users,'status':200, 'message':'Vous avez récupéré les utilisateurs déjà validés'}

class GestionGroupeResource(Resource):

    """
        Créé un nouveau groupe dans la bdd
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON avec un message validant la création du groupe
            404:
                description: S'il y a déjà un groupe avec le même nom dans la bdd
            
        """  
    def post(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('nomgroupe', type=str, required=True, help="Missing the name groupe")
        args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
        try:
            
            if(abort_if_groupe_is_not_unique(args['nomgroupe'])):
                return {'status':404,'message':'Ce nom de groupe existe déjà, veuillez en saisir un différent.'}
            else:
                
                #Crée le groupe
                groupe = Groupe(nom = args['nomgroupe'])
                #L'ajoute à la bdd
                db.session.add(groupe)
                db.session.commit()
                #retourne le status de la requête et un message qui pourra être utilisé par le front
                return {'status':201,'message':'Nouveau groupe créé !'}
        except:
            abort(400)
    """
        Get tous les groupes existants dans la bdd
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON représentant tous les groupes
            404:
                description: S'il n'y a aucun groupe dans la bdd
        """
    def get(self) -> List:
        result = Groupe.query.all()
        if result == []:
            return {'status':404, 'message':'Il n\'y a aucun groupe à récupérer.'}
        else:
            print(result)
            groupes = []
            for row in result:
                groupe = {}
                groupe['id_groupe'] = row.id
                groupe['nom'] = row.nom
                groupes.append(groupe)
            return {'data':groupes,'status':200, 'message':'Vous avez récupéré tous les groupes'}

class GestionGroupeById(Resource):

    """
        PATCH pour modifier le nom d'un groupe
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_groupe
              description: id du groupe à modifier
              required: true
              type: string
        responses:
            200:
                description: JSON avec un message validant la modification du groupe
            404:
                description: Si le groupe n'existe pas
        """
    def patch(self,id_groupe):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('nom_groupe', type=str, required=False, help="Missing the group name")
        args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
        if(not check_group_exists(id_groupe)):
            return {'status':404, 'message': 'Le groupe que vous tentez de modifier n\'existe pas.'}
        try:
            new_name= args['nom_groupe']
            db.session.query(Groupe).filter(Groupe.id == id_groupe).update({Groupe.nom: new_name}, synchronize_session=False)
            db.session.commit()
            return {'status':200, 'message': 'Vous avez bien modifié le nom du groupe !'}

        except:
            abort(400)



    """
        DELETE nom d'un groupe (même dans les utilisateurs de ce groupe)
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_groupe
              description: id du groupe à supprimer
              required: true
              type: string
        responses:
            200:
                description: JSON avec un message validant la suppression du groupe
            404:
                description: Si le groupe n'existe pas
        """
    def delete(self, id_groupe):

        if(not check_group_exists(id_groupe)):
            return {'status':404, 'message': 'Le groupe que vous tentez de supprimer n\'existe pas.'}
        
        else:
            #supprime les groupes des utilisateurs ayant le groupe
            Utilisateurs.query.filter(Utilisateurs.id_groupe == id_groupe).update({Utilisateurs.id_groupe: None}, synchronize_session=False)
            db.session.commit()
            #supprime le groupe
            Groupe.query.filter(Groupe.id == id_groupe).delete()
            db.session.commit()
            return {"status":200, "message": "Vous avez bien supprimé le groupe"}


    """
        Get tous les groupes existants dans la bdd
        ---
        tags:
            - Flask API
        responses:
            200:
                description: JSON représentant tous les groupes
            404:
                description: S'il n'y a aucun groupe dans la bdd
        """
    def get(self,id_groupe) -> List:

        if(not check_group_exists(id_groupe)):
            return {'status':404, 'message': 'Le groupe que vous tentez de récupérer n\'existe pas.'}
    
        else:
            result = Groupe.query.filter(Groupe.id == id_groupe).first()
            groupe = {}
            groupe['nom_groupe'] = result.nom
            return {'data':groupe,'status':200, 'message':'Vous avez récupéré le groupe'}


class GestionGroupeByEleveId(Resource):

    """
        PATCH pour modifier le groupe d'un utilisateur en particulier
        ---
        tags:
            - Flask API
        parameters:
            - in: path
              name: id_user
              description: id de l'utilisateur dont il faut modifier le groupe
              required: true
              type: string
        responses:
            200:
                description: JSON avec un message validant la modification du groupe de l'utilisateur
            404:
                description: Si le groupe n'a pas pu être modifié
        """
    def patch(self,id_eleve):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('groupe_id', type=str, required=False, help="Missing the group name")
        args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
        if(not check_user_exists(id_eleve)):
            return {'status':404, 'message': 'L\'utilisateur que vous tentez de modifier n\'existe pas.'}
        try:
            new_groupe= args['groupe_id']
            db.session.query(Utilisateurs).filter(Utilisateurs.id == id_eleve).update({Utilisateurs.id_groupe: new_groupe}, synchronize_session=False)
            db.session.commit()
            return {'status':200, 'message': 'Vous avez bien modifié le groupe de l\'utilisateur !'}

        except:
            abort(400)


def abort_if_groupe_is_not_unique(nom_groupe: str):
    already_exists = db.session.query(db.exists().where(Groupe.nom == nom_groupe)).scalar()
    return already_exists


def check_group_exists(id_groupe:int):
    groupe_exists = db.session.query(db.exists().where(Groupe.id == id_groupe)).scalar() 
    return groupe_exists


def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists



