from app import db


class Groupe(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    nom = db.Column("nom", db.String(100))
    utilisateurs = db.relationship('Utilisateurs', backref='groupe', lazy=True)


class Utilisateurs(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    nom = db.Column("nom", db.String(100))
    prenom = db.Column("prenom", db.String(100))
    mail = db.Column("mail", db.String(100))
    mdp = db.Column("mdp", db.String(100))
    droit = db.Column("type", db.String(100))
    valide = db.Column("valide",db.Boolean)
    qcm = db.relationship('Qcm', backref='utilisateurs', lazy=True)
    reponseleve = db.relationship('ReponseEleve', backref='utilisateurs', lazy=True)
    qcmeleve = db.relationship('QcmEleve', backref='utilisateurs', lazy=True)
    id_groupe = db.Column("id_groupe",db.Integer,db.ForeignKey('groupe.id'),nullable=True)
    

class Qcm(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    titre = db.Column("titre",db.String(200))
    date_debut = db.Column("date_debut", db.DateTime)
    date_fin = db.Column("date_fin", db.DateTime)
    questions = db.relationship('Question', backref='qcm', lazy=True)
    eleve = db.relationship('QcmEleve', backref='qcm', lazy=True)
    id_professeur = db.Column("id_professeur",db.Integer,db.ForeignKey('utilisateurs.id'),nullable=False)


class Question(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    intitule = db.Column("intitule",db.String(200))
    ouverte = db.Column("ouverte", db.Boolean)
    bareme = db.Column("bareme",db.Integer,nullable=True)
    choix = db.relationship('Choix', backref='question', lazy=True)
    reponseleve = db.relationship('ReponseEleve', backref='question', lazy=True)
    id_qcm = db.Column("qcm", db.Integer,db.ForeignKey('qcm.id'),nullable=False)

class Choix(db.Model):
    id = db.Column("id", db.Integer,primary_key=True)
    intitule = db.Column("intitule",db.String(200))
    estcorrect = db.Column("estcorrect", db.Boolean)
    reponseleve = db.relationship('ReponseEleve', backref='choix', lazy=True)
    id_question = db.Column("id_question", db.Integer,db.ForeignKey('question.id'),nullable=False)

class ReponseEleve(db.Model):
    id = db.Column("id", db.Integer,primary_key=True)
    reponseouverte = db.Column("reponseouverte", db.String(200),nullable=True)
    note = db.Column("note", db.Integer,nullable=True)
    id_choix = db.Column("id_choix", db.Integer,db.ForeignKey('choix.id'),nullable=True)
    id_eleve = db.Column("id_eleve", db.Integer,db.ForeignKey('utilisateurs.id'),nullable=False)
    id_question = db.Column("id_question", db.Integer,db.ForeignKey('question.id'),nullable=False)

class QcmEleve(db.Model):
    id = db.Column("id", db.Integer,primary_key=True)
    statut = db.Column("statut",db.String(50))
    id_eleve = db.Column("id_eleve", db.Integer,db.ForeignKey('utilisateurs.id'),nullable=False)
    id_qcm = db.Column("id_qcm", db.Integer,db.ForeignKey('qcm.id'),nullable=False)








