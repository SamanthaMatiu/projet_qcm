from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from werkzeug.security import check_password_hash, generate_password_hash
from functools import wraps
import datetime
import jwt
from app import db,app,models


class LoginResource(Resource):
    def post(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('utilisateur', type=str, required=True, help="Pas de login.")
        body_parser.add_argument('mdp', type=str, required=True, help="Pas de mot de passe.")
        args = body_parser.parse_args(strict=True)
        try:
            utilisateurs = args['utilisateur']
            mdp = args['mdp']
            return login(utilisateurs, mdp)
        except:
            abort(400)

def login(login, mdp):
    util=db.session.query(models.Utilisateurs).filter_by(mail=login).first()
    if util and check_password_hash(util.mdp,mdp) and util.valide==1:
        heure=datetime.datetime.utcnow()+datetime.timedelta(weeks=1)
        token=jwt.encode({'utilisateur':util.mail,'exp':heure},app.config['SECRET_KEY'])
        return {'statut':util.droit,'message':'Bienvenue '+util.prenom+' '+util.nom+' !','token':token.decode('UTF-8')},200
    return {'message':'Identifiant et/ou mot de passe incorrect. Ou compte non valide'},400

def token_verif(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token=None
        if 'x-access-token' in request.headers :
            token=request.headers['x-access-token']
        if not token:
            return{'message':'Aucun token trouvé.'},400
        
        try:
            data=jwt.decode(token,app.config['SECRET_KEY'])
            user=db.session.query(models.Utilisateurs).filter_by(mail=data['utilisateur']).first()
             
        except :
            return {'message': 'Token invalide.'},400

        return f(user,*args,**kwargs)
        
    return decorated

