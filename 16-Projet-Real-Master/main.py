import discord
from dotenv import load_dotenv
import os
from components.gpt import openai_request, openai_vision
from components.brave_api import brave_request
from components.tools import download_pdf_file, get_pdf_text
import re

load_dotenv(dotenv_path='components/.env')
token = os.environ['BOT_TOKEN']

msg_system = """
Você é o mestre supremo das mesas de RPG, seu objetivo é: 
1- Ajudar os jogadores com regras e dicas dos mais variados sistemas. 
2- Ser cordial e se o jogador quiser bater papo você deve responde-lo 
de forma cordial e puxar assunto com o mesmo.
3- Você sempre irá responder no mesmo idioma em que for questionado!
Se te perguntarem em Frances você responderá em Frances, por exemplo.
"""

msg_summarization = """
You are a highly skilled AI trained in language comprehension and summarization. 
I would like you to read the following text and summarize it into a concise 
abstract paragraph. Aim to retain the most important points, providing a 
coherent and readable summary that could help a person understand the main 
points of the discussion without needing to read the entire text. 
Please avoid unnecessary details or tangential points.
You need to generate the abstract paragraph in the same language of the original text.
"""

# connect to discord
intents = discord.Intents.all()
client = discord.Client(intents=intents)

# log
@client.event
async def on_ready():
    print("Logged as {0.user}".format(client))

# answerer
@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if (message.channel.name in ["bot"] 
        and client.user.mentioned_in(message)
        and message.mention_everyone is False):

        async with message.channel.typing():

            msg = str(message.content)

            if message.attachments:
                if "image" in message.attachments[0].content_type:
                    content = [{"type":"text", 
                                "text": re.sub("<@\d+>", "", msg),}]

                    for attch in message.attachments:
                        content.append({"type": "image_url",
                                        "image_url": {"url":attch.url},})
                        
                    vision_input = [{"role": "user", "content": content}]
                    reply = openai_vision(vision_input)      

                elif "pdf" in message.attachments[0].content_type:
                    response, filepath = download_pdf_file(message.attachments[0].url)
                    if response:
                        pdf_text = get_pdf_text(filepath)

                        summarization = [{"role":"system", 
                                          "content": msg_summarization}]
                        
                        summarization.append({"role":"user", "content": pdf_text})
                        reply = openai_request(summarization)
                
            else:         
                current_conv = [{"role":"system", "content": msg_system}]
                current_conv.append({"role":"user", "content": msg})

                if len(msg) < 200:
                    brave_output = brave_request(msg)
                    current_conv.append({"role":"system","content": 
                                         str(brave_output["results"][:5])})
                
                reply = openai_request(current_conv)
                current_conv.append({"role":"assistant", "content":reply})

            await message.reply(reply, mention_author=True)

client.run(token)