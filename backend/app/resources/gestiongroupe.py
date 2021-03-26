from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any

from app import db, models
from app.models import Utilisateurs, Groupe

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


def abort_if_groupe_is_not_unique(nom_groupe: str):
    already_exists = db.session.query(db.exists().where(Groupe.nom == nom_groupe)).scalar()
    return already_exists