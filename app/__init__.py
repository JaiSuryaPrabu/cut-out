from flask import Flask

app = Flask(__name__)

# always import the router below the app to avoid circular imports
from app import logics

# in the flask, the handlers for the application routers are called as view funtions