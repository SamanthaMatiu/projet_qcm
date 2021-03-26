from flask import request,jsonify
from flask_restful import Resource, reqparse, abort
from app import db,app,models

class QCMRessources(Resource):
    def get(self):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('id',type=int,required=True,help="Pas d'identifiants renseigné.")
        args=body_parser.parse_args(strict=True)
        try :
            qcm=find_a_qcm(args['id'])
            return qcm
        except:
            abort(400)

def find_a_qcm(id):
    return True