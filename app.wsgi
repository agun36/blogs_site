import os
import sys

sys.append('/Users/akindeleagun/Documents/GitHub/blogs_site')

from flask_app import app as my_app
app = Flask(__name__)
my_app.secret_key = 'mykey'

