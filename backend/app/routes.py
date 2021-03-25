from app import api

from app.resources.login import LoginResource
from app.resources.helloworld import HelloWorldResource

# login
api.add_resource(LoginResource, '/login')

#tests
api.add_resource(HelloWorldResource,'/test')

