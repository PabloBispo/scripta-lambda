import json
import os

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq


from app.cifraclub import chords_, lyrics_, raw_
from app.prompts import REFORMED_MUSIC_INFO_EXTRACTION_PROMPT

load_dotenv()

GROQ_API_KEY = os.environ.get('GROQ_API_KEY')


llm = ChatGroq(model='llama-3.1-70b-versatile', api_key=GROQ_API_KEY)


def base_chain():
    prompt = ChatPromptTemplate.from_template(
        REFORMED_MUSIC_INFO_EXTRACTION_PROMPT
    )

    chain = (
        {'music_sheet': RunnablePassthrough()}
        | prompt
        | llm
        | JsonOutputParser()
    )

    return chain


def handler(event, context):
    """
    handler
    """
    music_sheet = event.get('music_sheet')
    cifraclub_url = event.get('cifraclub_url')

    if not any((music_sheet, cifraclub_url)):
        return json.dumps(
            {
                'statusCode': 400,
                'message': 'Missing ("music_sheet", "cifraclub_url") params',
            }
        )

    if music_sheet:
        chain = base_chain()
        response = chain.invoke(music_sheet)

        return {'statusCode': 200, 'music_analysis': response}

    if cifraclub_url:
        music_raw_sheet = raw_(cifraclub_url)
        music_chords = chords_(raw=music_raw_sheet['raw'])
        music_lyrics = lyrics_(raw=music_raw_sheet['raw'])

        return {
            'statusCode': 200,
            'music_sheets': dict(
                **music_raw_sheet,
                **music_chords,
                **music_lyrics,
            ),
        }


if __name__ == '__main__':
    event = {
  "cifraclub_url": "https://www.cifraclub.com.br/isaias-saad/bondade-de-deus/"
}
    response = handler(event, None)
    print(response)