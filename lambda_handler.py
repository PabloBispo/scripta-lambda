import json
import logging
import os
from typing import Dict

from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_groq import ChatGroq
from pydantic import ValidationError

from app.cifraclub import chords_, lyrics_, raw_
from app.core.config import settings
from app.core.logger import get_advanced_logger
from app.models import MusicInfoExtractEvent, Context
from app.prompts import REFORMED_MUSIC_INFO_EXTRACTION_PROMPT


log = get_advanced_logger('LambdaHandlerLogger', level=logging.DEBUG)

llm = ChatGroq(model='llama-3.1-70b-versatile', api_key=settings.GROQ_API_KEY)


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


def get_music_sheet(music_info_event: MusicInfoExtractEvent) -> Dict:
    if music_info_event.song_raw_sheet:
        return {'raw': music_info_event.song_raw_sheet}

    if music_info_event.cifra_club_url:
        song_raw_sheet = raw_(music_info_event.cifra_club_url)
        music_chords = chords_(raw=song_raw_sheet['raw'])
        music_lyrics = lyrics_(raw=song_raw_sheet['raw'])

        return dict(
            **song_raw_sheet,
            **music_chords,
            **music_lyrics,
        )


def get_music_analysis(music_info_event: MusicInfoExtractEvent) -> Dict:
    if music_info_event.song_raw_sheet:
        chain = base_chain()

        song_data_dict = {k:v for k, v in music_info_event.song_raw_sheet.items() if k in ('raw', 'metadata') }
        result = chain.invoke(song_data_dict)

        return result


def lambda_handler(event: dict | None = None, context=None) -> dict:
    if context is None:
        context = {}

    log.info('event', extra=event)
    log.info('context', extra=context)

    try:
        music_info_event = MusicInfoExtractEvent.model_validate(event)
        context_data = Context.model_validate(context)
    except ValidationError as e:
        return {'result': 'error', 'message': e.errors(include_url=False)}

    song_raw_sheet = get_music_sheet(music_info_event)
    if (
        not music_info_event.song_raw_sheet
        and music_info_event.download_and_analyse_song
    ):
        music_info_event.song_raw_sheet = song_raw_sheet

    song_analysis = get_music_analysis(music_info_event)

    return {
        'result': 'success',
        'event': music_info_event.model_dump(mode='json'),
        'request_id': context_data.aws_request_id,
        'data': {
            'song_analysis': song_analysis,
            'song_raw_sheet': song_raw_sheet,
        },
    }


if __name__ == '__main__':
    event_ = {
        'cifra_club_url': 'https://www.cifraclub.com.br/isaias-saad/bondade-de-deus/',
        'download_and_analyse_song': True
    }
    response = lambda_handler(event_, None)
    print(response)
