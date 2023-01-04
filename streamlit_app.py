from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
from youtube_transcript_api import YouTubeTranscriptApi
from gpt_index import GPTTreeIndex 
from gpt_index.readers.schema.base import Document
from urllib.parse import urlparse
from urllib.parse import parse_qs


st.title('Summarize a youtube video')


def get_transcript(item_id: str):
    transcript = YouTubeTranscriptApi.get_transcript(item_id)
    return transcript

def get_summary_from_transcript(transcript, query):
    results = []
    for line in transcript:
        results.append(Document(line.get('text')))

    index = GPTTreeIndex(results)
    response = index.query(query)
    return response


def get_video_id_from_link(url):
    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)['v'][0]
    return captured_value


def main():
    # get youtube link
    st.title('Video Examples', )
    st.text('https://www.youtube.com/watch?v=HXesSmxVNMs')
    st.text('https://www.youtube.com/watch?v=IMvffRnRO0E')
    st.title('Alteration examples')
    st.text('Get ingredients and procedure')
    st.text('Create a shopping list')
    st.text('Convert to metric system')
    url = st.text_input('What video do you want to use?', '',
                        placeholder="https://www.youtube.com/watch?v=HXesSmxVNMs")

    query = st.text_input('What do you want to do with it?',
                          placeholder="Get ingredients and procedure", )

    if not url:
        return
    if not query:
        return

    # extra video id
    videoId = get_video_id_from_link(url)
    transcript = get_transcript(videoId)

    # Show loading
    data_load_state = st.text('Loading data...')
    # Get summary
    summary = get_summary_from_transcript(transcript, query)
    data_load_state.text('Done')
    # Display summary
    st.text(summary)

    # Display full transcript
    st.text(transcript)


main()
