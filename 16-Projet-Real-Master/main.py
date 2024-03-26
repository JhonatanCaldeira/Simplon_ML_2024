import discord
from dotenv import load_dotenv
import os
from components.gpt import openai_request, openai_vision
from components.brave_api import brave_request
from components.tools import download_to_base64
import re

load_dotenv(dotenv_path='components/.env')
token = os.environ['BOT_TOKEN']

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
                content = [{"type":"text", "text": re.sub("<@\d+>", "", msg),}]

                for attch in message.attachments:
                    if "image" in attch.content_type:
                        content.append({"type": "image_url","image_url": {"url":attch.url},})

                vision_input = [{"role": "user", "content": content}]
                print(vision_input)

                reply = openai_vision(vision_input)
                
            else:
                msg_system = """Você é o mestre supremo das mesas de RPG, seu objetivo
                é de ajudar os jogadores com regras e dicas dos mais variados sistemas. 
                Você sempre irá responder no mesmo idioma em que for questionado!
                Se te perguntarem em Frances você responderá em Frances, por exemplo."""
            
                current_conv = [{"role":"system", "content": msg_system}]
                current_conv.append({"role":"user", "content": msg})

                brave_output = brave_request(msg)
                current_conv.append({"role":"system","content": str(brave_output["results"][:5])})
                
                reply = openai_request(current_conv)
                current_conv.append({"role":"assistant", "content":reply})

            await message.reply(reply, mention_author=True)

client.run(token)