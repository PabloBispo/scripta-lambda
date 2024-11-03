import json
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq

import app.prompts as p

load_dotenv()

GROQ_API_KEY = os.environ.get("GROQ_API_KEY")


llm = ChatGroq(model="llama-3.1-70b-versatile", api_key=GROQ_API_KEY)


def base_chain():
    prompt = ChatPromptTemplate.from_template(
        p.REFORMED_MUSIC_INFO_EXTRACTION_PROMPT
    )

    chain = (
        { "music_sheet": RunnablePassthrough()}
        | prompt
        | llm
        | JsonOutputParser()
    )

    return chain


def handler(event, context):
    """
    handler
    """
    music_sheet = event.get("music_sheet")

    if not music_sheet:
        return json.dumps({"statusCode": 400, "message": "Missing question parameter"})

    chain = base_chain()
    response = chain.invoke(music_sheet)

    return {"statusCode": 200, "response": response}
