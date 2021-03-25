from app import api

from app.resources.helloworld import HelloWorldResource, HelloWorldResourceNameToken, HelloWorldResourceNameURL, HelloWorldResourceNames
from app.resources.register import RegisterResource

# Hello World
api.add_resource(HelloWorldResource, '/api/helloworld')
api.add_resource(HelloWorldResourceNameToken, '/api/hello')
api.add_resource(HelloWorldResourceNameURL, '/api/hello/<string:name>')
api.add_resource(HelloWorldResourceNames, '/api/hello/<int:count>')

# Create an account
api.add_resource(RegisterResource,'/api/register')