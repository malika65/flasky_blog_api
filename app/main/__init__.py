from flask import Blueprint


# now that the application is created at runtime, 
# the app.route decorator begins to exist only after create_app() is invoked, which is too late
# Solution is Blueprint :
# Routes and error handlers are in a dormant state until the blueprint is created
# registered with an application, at which point they become part of it

main = Blueprint('main', __name__)

# modules should be imported at the bottom after main is defined
from . import views, errors