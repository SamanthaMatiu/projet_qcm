from app import api

from app.resources.login import LoginResource
from app.resources.helloworld import HelloWorldResource
from app.resources.register import RegisterResource
from app.resources.validationadmin import ValidationAdminResource, ValidationAdminResourceById
from app.resources.gestiongroupe import GestionGroupeResource

# login
api.add_resource(LoginResource, '/api/login')

#tests
api.add_resource(HelloWorldResource,'/test')

# Create an account
api.add_resource(RegisterResource,'/api/register')

#Gestion des groupes
api.add_resource(GestionGroupeResource,'/api/groupes')

# Validate an account
api.add_resource(ValidationAdminResource,'/api/validation')
api.add_resource(ValidationAdminResourceById,'/api/validation/<int:id_user>')

