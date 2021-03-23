from app import api

from app.resources.helloworld import HelloWorldResource, HelloWorldResourceNameToken, HelloWorldResourceNameURL, HelloWorldResourceNames
from app.resources.login import LoginResource
from app.resources.todos import TodoManagementResource, TodoManagementResourceByID

# Hello World
api.add_resource(HelloWorldResource, '/api/helloworld')
api.add_resource(HelloWorldResourceNameToken, '/api/hello')
api.add_resource(HelloWorldResourceNameURL, '/api/hello/<string:name>')
api.add_resource(HelloWorldResourceNames, '/api/hello/<int:count>')

# Login
api.add_resource(LoginResource, '/api/login')

# Todos app
api.add_resource(TodoManagementResource, '/api/todos')
api.add_resource(TodoManagementResourceByID, '/api/todos/<int:todo_id>')
