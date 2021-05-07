from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, models
from app.models import Utilisateurs

class RegisterResource(Resource):
    def post(self):
            body_parser = reqparse.RequestParser()
            body_parser.add_argument('nomauth', type=str, required=True, help="Missing the login of the user")
            body_parser.add_argument('prenomauth', type=str, required=True, help="Missing the login of the user")
            body_parser.add_argument('mailauth', type=str, required=True, help="Missing the login of the user")            
            body_parser.add_argument('mdpauth', type=str, required=True, help="Missing the password associated to the user login")
            body_parser.add_argument('droitauth', type=str, required=True, help="Missing the login of the user")
            #Valide à mettre à false dès le départ, pour l'instant à true le temps de valider les comptes côté front
            #Groupe à renseigner plus tard par l'admin
            args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
            try:
                if(abort_if_mail_is_not_unique(args['mailauth'])):
                    return {'status':404,'message':'Adresse mail déjà utilisée, merci d\'en saisir une autre.'}
                else:
                    #Hash le mot de passe
                    hashed_mdp = generate_password_hash(args['mdpauth'], method='sha256')
                    #Crée l'utilisateur
                    user = Utilisateurs(nom = args['nomauth'], prenom = args['prenomauth'], mail = args['mailauth'], mdp = hashed_mdp, droit = args['droitauth'], valide = False, id_groupe = None)
                    #L'ajoute à la bdd
                    db.session.add(user)
                    db.session.commit()
                    #retourne le status de la requête et un message qui pourra être utilisé par le front
                    return {'status':201,'message':'Nouvelle utilisateur créé !'}
            except:
                abort(400)


def abort_if_mail_is_not_unique(mail_saisi: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.mail == mail_saisi)).scalar()
    return already_exists