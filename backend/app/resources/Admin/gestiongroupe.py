from flask import request
from flask_restful import Resource, reqparse, abort
from typing import Dict, List, Any
from sqlalchemy import or_
from app import db, models
from app.models import Utilisateurs, Groupe, Qcm, QcmEleve

class ElevesValidesResource(Resource):
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
        result = db.session.query(Utilisateurs).filter(Utilisateurs.valide == True ,or_(Utilisateurs.droit == "Élève" , Utilisateurs.droit == "élève"))
        if result.count() == 0:
            return {'status':404, 'message':'Il n\'y a aucun utilisateur déjà validé.'}
        else:
            users = []
            for row in result:
                user = {}
                user['nom'] = row.nom
                user['prenom'] = row.prenom
                user['mail'] = row.mail
                user['droit'] = row.droit
                user['groupe'] = row.id_groupe
                user['id_utilisateur'] = row.id
                user['nom_groupe'] = get_nom_groupe(row.id_groupe)
                users.append(user)
            return {'data':users,'status':200, 'message':'Vous avez récupéré les utilisateurs déjà validés'}

class ProfesseursValidesResource(Resource):
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
        result = db.session.query(Utilisateurs).filter(Utilisateurs.valide == True, Utilisateurs.droit == "Professeur")
        if result.count() == 0:
            return {'status':404, 'message':'Il n\'y a aucun utilisateur déjà validé.'}
        else:
            users = []
            for row in result:
                user = {}
                user['nom'] = row.nom
                user['prenom'] = row.prenom
                user['mail'] = row.mail
                user['droit'] = row.droit
                user['groupe'] = row.id_groupe
                user['id_utilisateur'] = row.id
                user['nom_groupe'] = get_nom_groupe(row.id_groupe)
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

        #Je cherche quelqu'un de ce groupe et ensuite je check tous ses qcm et les ajoute à la nouvelle personne du groupe'
    def patch(self,id_eleve):
        body_parser = reqparse.RequestParser()
        body_parser.add_argument('groupe_id', type=str, required=False, help="Missing the group name")
        args = body_parser.parse_args(strict=True) # Accepté seulement si tous les paramètres sont strictement déclarés dans le body sinon lève une exception
        if(not check_user_exists(id_eleve)):
            return {'status':404, 'message': 'L\'utilisateur que vous tentez de modifier n\'existe pas.'}
        try:
            new_groupe= args['groupe_id']
            print(new_groupe)
            if(check_if_group_already_has_eleve_with_qcm(new_groupe) is not None):
                #Créer la/les liaisons qcm_eleve que va impliquer ce changement de groupe
                #Récupère un élève qui est déjà dans le groupe
                eleve_deja_dans_groupe = Utilisateurs.query.filter(Utilisateurs.id_groupe == new_groupe).first()
                #Récupère l'élève dont on veut modifier le groupe
                eleve = db.session.query(Utilisateurs).filter_by(id=id_eleve).first()

                for qcm in eleve_deja_dans_groupe.qcmeleve:
                    qcm_du_groupe = db.session.query(Qcm).filter_by(id=qcm.id_qcm).first()
                    if(eleve_already_has_this_qcm(eleve.id,qcm_du_groupe) is None):
                        add_eleve_to_qcm(eleve,qcm_du_groupe)
                
                db.session.query(Utilisateurs).filter(Utilisateurs.id == id_eleve).update({Utilisateurs.id_groupe: new_groupe}, synchronize_session=False)
                db.session.commit()
            else:
                #On met le nouveau groupe à l'élève
                db.session.query(Utilisateurs).filter(Utilisateurs.id == id_eleve).update({Utilisateurs.id_groupe: new_groupe}, synchronize_session=False)
                db.session.commit()
            
            return {'status':200, 'message': 'Vous avez bien modifié le groupe de l\'utilisateur !'}


        except:
            abort(400)




class GestionGroupeManyEleves(Resource):

    """
        PATCH pour modifier le groupe de plusieurs élèves en même temps
        ---
        tags:
            - Flask API
        parameters:
            - in: body
              name: eleves qui est un tableau 
              description: id des utilisateurs dont il faut modifier le groupe
              required: true
              type: string
        responses:
            200:
                description: JSON avec un message validant la modification 
            404:
                description: Si le groupe n'a pas pu être modifié
        """

        #Je cherche quelqu'un de ce groupe et ensuite je check tous ses qcm et les ajoute à la nouvelle personne du groupe'
    def patch(self):
        datas = request.get_json()
        try:
            eleves = datas['eleves']
            new_groupe= datas['groupe_id']

            #Vérifie qu'un élève n'appartient pas déjà à ce groupe
            for eleve in eleves:
                eleve_a_check = db.session.query(Utilisateurs).filter(Utilisateurs.id == eleve['id']).first()
                if(user_already_in_the_group(new_groupe,eleve['id']) is not None):
                    return {"status":404,"message": "L\'utilisateur "+eleve_a_check.prenom+" "+eleve_a_check.nom+" est déjà dans le groupe que vous venez de choisir"}
        
            #Si le groupe contient déjà des élèves avec des qcm
            if(check_if_group_already_has_eleve_with_qcm(new_groupe) is not None):

                #Récupère un élève qui est déjà dans le groupe
                eleve_deja_dans_groupe = Utilisateurs.query.filter(Utilisateurs.id_groupe == new_groupe).first()
                for eleve in eleves:
                    #Récupère l'élève dont on veut modifier le groupe
                    eleve_a_modifier = db.session.query(Utilisateurs).filter(Utilisateurs.id == eleve['id']).first()
                    #On met les qcm du groupe à ce nouvelle élève
                    for qcm in eleve_deja_dans_groupe.qcmeleve:
                        qcm_du_groupe = db.session.query(Qcm).filter_by(id=qcm.id_qcm).first()
                        if(eleve_already_has_this_qcm(eleve['id'],qcm_du_groupe) is None):
                            add_eleve_to_qcm(eleve_a_modifier,qcm_du_groupe)
                    #On met le nouveau groupe à l'élève
                    db.session.query(Utilisateurs).filter(Utilisateurs.id == eleve['id']).update({Utilisateurs.id_groupe: new_groupe}, synchronize_session=False)
                    db.session.commit()

            else:
                for eleve in eleves:
                    #On met le nouveau groupe à l'élève
                    db.session.query(Utilisateurs).filter(Utilisateurs.id == eleve['id']).update({Utilisateurs.id_groupe: new_groupe}, synchronize_session=False)
                    db.session.commit()

           
            return {'status':200, 'message': 'Vous avez bien modifié le groupe des utilisateurs !'}

        except:
            abort(400)


def abort_if_groupe_is_not_unique(nom_groupe: str):
    already_exists = db.session.query(db.exists().where(Groupe.nom == nom_groupe)).scalar()
    return already_exists

def check_if_group_already_has_eleve_with_qcm(id_groupe:int):
    q = db.session.query(Utilisateurs,QcmEleve).filter(QcmEleve.id_eleve == Utilisateurs.id).filter(Utilisateurs.id_groupe == id_groupe).first()
    res = db.session.query(db.exists().where(Utilisateurs.id_groupe == id_groupe )).scalar()
    return q

def user_already_in_the_group(groupe_id,eleve_id):
    res = db.session.query(Utilisateurs).filter(Utilisateurs.id_groupe == groupe_id, Utilisateurs.id == eleve_id).first()
    return res


def check_if_group_already_has_user(id_groupe:int):
    res = db.session.query(db.exists().where(Utilisateurs.id_groupe == id_groupe)).scalar()
    return res

def check_group_exists(id_groupe:int):
    groupe_exists = db.session.query(db.exists().where(Groupe.id == id_groupe)).scalar() 
    return groupe_exists


def check_user_exists(id_user: str):
    already_exists = db.session.query(db.exists().where(Utilisateurs.id == id_user)).scalar()
    return already_exists

def eleve_already_has_this_qcm(eleve_id,QCM):
    q = db.session.query(QcmEleve).filter(QcmEleve.id_eleve == eleve_id, QcmEleve.id_qcm == QCM.id).first()
    return q

def add_eleve_to_qcm(eleve,QCM):    
    qcmEleve=QcmEleve(statut='A faire',utilisateurs=eleve,qcm=QCM)
    db.session.add(qcmEleve)
    db.session.commit()


def get_nom_groupe(id_groupe):
    groupe = ""
    if(id_groupe is not None):
        groupe = Groupe.query.filter(Groupe.id == id_groupe).first().nom
    return groupe

