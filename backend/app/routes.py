from app import api

from app.resources.login import LoginResource
from app.resources.helloworld import HelloWorldResource
from app.resources.register import RegisterResource
from app.resources.qcm import QCMRessources

#tests
api.add_resource(HelloWorldResource,'/test')

# login
api.add_resource(LoginResource, '/api/login')

#qcms
api.add_resource(QCMRessources,'/api/qcm')

# Create an account
api.add_resource(RegisterResource,'/api/register')