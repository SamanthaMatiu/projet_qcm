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
        body_parser.add_argument('utilisateurs', type=str, required=True, help="Pas de login.")
        body_parser.add_argument('mdp', type=str, required=True, help="Pas de mot de passe.")
        args = body_parser.parse_args(strict=True)
        try:
            utilisateurs = args['utilisateurs']
            mdp = args['mdp']
            return login(utilisateurs, mdp)
        except:
            abort(400)

def login(login, mdp):
    util=models.Utilisateurs.query.filter_by(mail=login).first()
    if util and check_password_hash(util.mdp,mdp):
        heure=datetime.datetime.utcnow()+datetime.timedelta(hours=2)
        token=jwt.encode({'utilisateur':util.mail,'exp':heure},app.config['SECRET_KEY'])
        return {'message':'Bienvenue '+util.prenom+' '+util.nom+' !','token':token.decode('UTF-8')},200
    return {'message':'Identifiant et/ou mot de passe incorrect.'},400

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
            user=models.Utilisateurs.query.filter_by(mail=data['utilisateur'])
            if (user):
              valid=1
        except :
            return {'message': 'Token invalide.'},400

        return f(*args,**kwargs)
    return decorated

