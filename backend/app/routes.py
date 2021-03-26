from app import api

from app.resources.login import LoginResource
from app.resources.helloworld import HelloWorldResource
from app.resources.register import RegisterResource

# login
api.add_resource(LoginResource, '/api/login')

#tests
api.add_resource(HelloWorldResource,'/test')

# Create an account
api.add_resource(RegisterResource,'/api/register')