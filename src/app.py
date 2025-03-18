from flask import Flask,request
from flask_cors import CORS

import configparser
import openai
import time
import os

TOPIC_PROMPT = { "logiciel" : "Rédige un énoncé relatif aux brevets sur les logiciels.", "default" : "Rédige un énoncé."}

#flask
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

#config
CONFIG_PATH = os.path.split(os.path.realpath(__file__))[0] + "\\..\\config.ini"
CONFIG = configparser.ConfigParser()
CONFIG.read(CONFIG_PATH)

#openai
openai.api_key = CONFIG["OPENAI"]["API_KEY_MAIN"]

@app.route('/api/v1/correction',methods=['POST'])
def correction():
    #récupération du corps de la requête
    question = request.json["question"]
    answer = request.json["answer"]
    #génération de la correction
    #création de thread
    thread = openai.beta.threads.create()

    #création du prompt
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=f"La question posée est : \n\n{question}\n\nMa réponse est : \n\n{answer}\n\n"
    )

    #lancement de la run
    run = openai.beta.threads.runs.create(thread_id=thread.id,assistant_id=CONFIG["OPENAI"]["ASSISTANT_ID_CORRECTION"])

    #attente du traitement de la run et de la réponse de l'assistant
    waitForRunCompletion = True
    waitForAnswer = True
    while waitForRunCompletion or waitForAnswer:
        if waitForRunCompletion:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            waitForRunCompletion = (run_status.status == "completed")
        elif waitForAnswer:
                messages = openai.beta.threads.messages.list(thread_id=thread.id)
                response = [msg for msg in messages.data if msg.role == "assistant"]    
                if response: waitForAnswer = not response[0].content
                else:   waitForAnswer = True
        time.sleep(1)

    #traitement du résultat
    return { "assistant" : response[0].content[0].text.value }

@app.route('/api/v1/question',methods=['POST'])
def question():
    #récupération du corps de la requête
    topic = request.json["topic"]
    #génération de la correction
    #création de thread
    thread = openai.beta.threads.create()

    #création du prompt
    message = openai.beta.threads.messages.create(
        thread_id=thread.id,
        role="user",
        content=TOPIC_PROMPT[topic]
    )

    #lancement de la run
    run = openai.beta.threads.runs.create(thread_id=thread.id,assistant_id=CONFIG["OPENAI"]["ASSISTANT_ID_QUESTION"])

    #attente du traitement de la run et de la réponse de l'assistant
    waitForRunCompletion = True
    waitForAnswer = True
    while waitForRunCompletion or waitForAnswer:
        if waitForRunCompletion:
            run_status = openai.beta.threads.runs.retrieve(thread_id=thread.id, run_id=run.id)
            waitForRunCompletion = (run_status.status == "completed")
        elif waitForAnswer:
                messages = openai.beta.threads.messages.list(thread_id=thread.id)
                response = [msg for msg in messages.data if msg.role == "assistant"]    
                if response: waitForAnswer = not response[0].content
                else:   waitForAnswer = True
        time.sleep(1)

    #traitement du résultat
    return { "assistant" : response[0].content[0].text.value }