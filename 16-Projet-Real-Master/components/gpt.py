from openai import OpenAI
from dotenv import load_dotenv
import os

def openai_request(conv):

    load_dotenv(dotenv_path='.env')
    client = OpenAI(api_key=os.environ.get("OPENAI_API_TOKEN"),)

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=conv
    )

    return completion.choices[0].message.content

def openai_vision(conv):
    load_dotenv(dotenv_path='.env')
    client = OpenAI(api_key=os.environ.get("OPENAI_API_TOKEN"),)

    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=conv,
        max_tokens=300,
    )

    return response.choices[0].message.content

def abstract_summary_extraction(conv):
    load_dotenv(dotenv_path='.env')
    client = OpenAI(api_key=os.environ.get("OPENAI_API_TOKEN"),)

    response = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=conv
    )
    return response.choices[0].message.content