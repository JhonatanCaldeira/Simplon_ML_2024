import discord
from dotenv import load_dotenv
import os
from components.gpt import openai_request
from components.brave_api import brave_request
from components.tools import download_pdf_file, get_pdf_text

# load_dotenv(dotenv_path='components/.env')
# token = os.environ['BOT_TOKEN']

# msg = str('Imagine a situação à seguir: Estamos enfrentando um dragão macho e um dos jogadores grita para o dragão Olha! Um dragão femea! O que o dragao faria?')

# # current_conv
# msg_system = """Você é o mestre supremo das mesas de RPG, seu objetivo
#     é de ajudar os jogadores com regras e dicas dos mais variados sistemas. 
#     Você sempre irá responder no mesmo idioma em que for questionado!
#     Se te perguntarem em Frances você responderá em Frances, por exemplo."""

# current_conv = [{"role":"system", "content": msg_system}]
# brave_output = brave_request(msg)

# input_gpt = "Responda a essa pergunta: " + msg + " considerando também esse conteudo: " + str(brave_output["results"][:5])

# current_conv.append({"role":"user", "content": input_gpt})
# current_conv.append({"role":"system","content": str(brave_output["results"][:5])})

# reply = openai_request(current_conv)
# current_conv.append({"role":"assistant", "content":reply})

# download_pdf_file('https://cdn.discordapp.com/attachments/1221765029985128468/1222137700010954802/88_Past-Perfect_US_Student.pdf?ex=66151f6d&is=6602aa6d&hm=4013b9738ac4c6faf440da6641394a6a9d09a00037c5c0748136e9cb04af0268&')

filepath = os.path.join(os.getcwd(), 'prestacao_contas.pdf')
print(get_pdf_text(filepath))