from app import api

from app.resources.helloworld import HelloWorldResource, HelloWorldResourceNameToken, HelloWorldResourceNameURL, HelloWorldResourceNames
from app.resources.register import RegisterResource
from app.resources.validationadmin import ValidationAdminResource, ValidationAdminResourceById
from app.resources.gestiongroupe import GestionGroupeResource

# Hello World
api.add_resource(HelloWorldResource, '/api/helloworld')
api.add_resource(HelloWorldResourceNameToken, '/api/hello')
api.add_resource(HelloWorldResourceNameURL, '/api/hello/<string:name>')
api.add_resource(HelloWorldResourceNames, '/api/hello/<int:count>')

# Create an account
api.add_resource(RegisterResource,'/api/register')

#Gestion des groupes
api.add_resource(GestionGroupeResource,'/api/groupes')

# Validate an account
api.add_resource(ValidationAdminResource,'/api/validation')
api.add_resource(ValidationAdminResourceById,'/api/validation/<int:id_user>')

