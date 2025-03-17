from flask import Flask,request
from flask_cors import CORS

import configparser
import openai
import time
import os


#flask
# app = Flask(__name__)
# cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#config
CONFIG_PATH = os.path.split(os.path.realpath(__file__))[0] + "\\..\\config.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)

#openai
openai.api_key = CONFIG["OPENAI"]["API_KEY_MAIN"]

#génération de la correction
#création de thread
thread = openai.beta.threads.create()

#création du prompt
message = openai.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="Quel est le nom exact des documents ?"
)

#lancement de la run
run = openai.beta.threads.runs.create(thread_id=thread.id,assistant_id=CONFIG["OPENAI"]["ASSISTANT_ID_CORRECTION"])

#attente du traitement de la run
wait = True
while wait:
    run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
    wait = (run_status.status == "completed")
    time.sleep(1)

#attente de la réponse de l'assistant
wait = True
while wait:
    messages = openai.beta.threads.messages.list(thread_id=thread.id)
    wait = [msg for msg in messages.data if msg.role == "assistant"]
    time.sleep(1)

#traitement du résultat
messages = openai.beta.threads.messages.list(thread_id=thread.id)

for msg in messages.data:
    print(msg.content[0].text.value)

#asynchrone ?
#créer un endpoint d'initiation du thread

# @app.route('/api/v1/auth/signin',methods=['GET'])
# def login():
#     return "salut les gars"