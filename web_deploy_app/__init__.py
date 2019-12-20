from flask import Flask

app = Flask(__name__)

from web_deploy_app import run
