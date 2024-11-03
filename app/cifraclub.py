import re

import requests
from bs4 import BeautifulSoup


def get_music_details(soup):
    track_metadata = {}
    track_metadata['name'] = soup.find('h1', class_='t1').text
    track_metadata['artist'] = soup.find('h2', class_='t3').text
    print(track_metadata)
    # img_youtube = soup.find('div', class_='player-placeholder').img['src']
    # cod = img_youtube.split('/vi/')[1].split('/')[0]
    # track_metadata['youtube_url'] = f"https://www.youtube.com/watch?v={cod}"

    return track_metadata


def is_chord(string):
    # Regex para detectar acordes com diferentes tipos e notas de baixo, incluindo "7M"
    pattern = r'^(?:[A-G](?:#|b)?)(?:m|maj|min|sus|dim|aug|add|7M)?\d*(?:#|b)?\d*(?:\/[A-G](?:#|b)?)?$'

    # Verifica se a string corresponde ao padrão de acorde
    match = re.match(pattern, string)

    # Retorna True se houver correspondência completa, senão False
    return match is not None and match.group(0) == string


def remove_intro_chords(raw: str):
    lines = raw.split('\n')
    out_lines = []
    for l in lines:
        if '[intro]' in l.lower():
            # out_lines.append('[Intro]')
            continue
        out_lines.extend([l])
    return '\n'.join(out_lines)


def remove_tabs(raw: str):
    return re.sub(r'^[EADGBE]\|[^\n]*\n?', '', raw, flags=re.MULTILINE)


def get_raw(url: str, get_metadata: bool = False):
    response = requests.get(url)
    html_content = response.text

    soup = BeautifulSoup(html_content, 'html.parser')

    track_metadata = get_music_details(soup)

    pre_section = soup.find('pre')

    output = pre_section.text
    if get_metadata:
        return output, track_metadata
    return output


def get_chords(raw: str):
    chords = []
    has_solo = False

    for line in raw:
        if '-' in line[0]:
            has_solo = True
        elif any(is_chord(x) for x in line):
            chords.extend([x for x in line if is_chord(x)])

    return list(set(chords)), has_solo


def get_lyrics(raw: list[str], trim_intro_chords: bool = True):
    lyrics = []

    if trim_intro_chords:
        raw = remove_intro_chords(raw)

    for line in raw.split('\n'):
        if not line:
            lyrics.append('')
            continue
        # print(f'[{any(not is_chord(x.strip()) for x in line.split())}]line -> ', line, '-> ', line.split())
        if (
            any(
                not is_chord(x.strip()) and x not in list('()')
                for x in line.split()
            )
            and line
        ):
            lyrics.extend([line.strip()])

    return '\n'.join(lyrics).strip()


def chords_(raw: str = None, url: str = None):
    if not raw:
        raw = get_raw(url)
    chords, has_solo = get_chords(raw)
    return {'chords': chords, 'has_solo': has_solo}


def raw_(url: str):
    raw, metadata = get_raw(url, get_metadata=True)
    return {'raw': raw, 'metadata': metadata}


def lyrics_(raw: str = None, url: str = None):
    if not raw:
        raw = get_raw(url)
    return {'lyrics': get_lyrics(raw)}
