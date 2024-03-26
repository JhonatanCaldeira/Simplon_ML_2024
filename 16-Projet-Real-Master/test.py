import discord
from dotenv import load_dotenv
import os
from components.gpt import openai_request
from components.brave_api import brave_request

load_dotenv(dotenv_path='components/.env')
token = os.environ['BOT_TOKEN']

msg = str('Preciso de ajuda com o jogo de RPG Dragon Age')

# current_conv
msg_system = """Você é o mestre supremo das mesas de RPG, seu objetivo
    é de ajudar os jogadores com regras e dicas dos mais variados sistemas. 
    Você sempre irá responder no mesmo idioma em que for questionado!
    Se te perguntarem em Frances você responderá em Frances, por exemplo."""

current_conv = [{"role":"system", "content": msg_system}]
brave_output = brave_request(msg)

input_gpt = "Responda a essa pergunta: " + msg + " considerando também esse conteudo: " + str(brave_output["results"][:5])

current_conv.append({"role":"user", "content": input_gpt})
current_conv.append({"role":"system","content": str(brave_output["results"][:5])})

reply = openai_request(current_conv)
current_conv.append({"role":"assistant", "content":reply})