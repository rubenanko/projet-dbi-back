from flask import Flask,request
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/v1/auth/signin',methods=['POST'])
def login():
    userData = {"username" : request.data.get('username')}
    return "salut les gars"