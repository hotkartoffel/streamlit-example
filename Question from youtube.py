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


def get_transcript(item_id: str):
    transcript = YouTubeTranscriptApi.get_transcript(item_id)
    return transcript


def get_alteration_from_source(transcript, query):
    results = []
    group_by = 10
    line_groups = [transcript[n:n+group_by]
                   for n in range(0, len(transcript), group_by)]
    for lines in line_groups:
        st.caption('\n'.join([line.get('text') for line in lines]))
        results.append(
            Document('\n'.join([line.get('text') for line in lines])))
    index = GPTTreeIndex(results)
    response = index.query(query)
    return response


def get_video_id_from_link(url):
    parsed_url = urlparse(url)
    captured_value = parse_qs(parsed_url.query)['v'][0]
    return captured_value


def transform(url, query):
    st.subheader('Summary')
    summary_container = st.caption('Loading...')
    videoId = get_video_id_from_link(url)
    # Show loading
    data_load_state = st.text('Loading data for')
    transcript = get_transcript(videoId)
    # Get summary
    summary = get_alteration_from_source(transcript, query)
    data_load_state.text('Done')
    # Display summary
    summary_container.write(summary)


with st.form('my_form'):
    st.title('Retrieve information from YouTube videos')
    url = st.text_input('What video do you want to use?', '',
                        placeholder="https://www.youtube.com/watch?v=HXesSmxVNMs")

    st.caption('You can copy/paste one of the following videos to try it out')
    st.caption('* https://www.youtube.com/watch?v=HXesSmxVNMs')
    st.caption('* https://www.youtube.com/watch?v=IMvffRnRO0E')
    st.caption('* https://www.youtube.com/watch?v=sDqiwmBDbug')

    query = st.text_area('What do you want to do with it?',
                         placeholder="Get ingredients and procedure", )

    st.caption('Copy/paste out the following to try it out')
    st.caption('* What ingredients do I need?')
    st.caption('* How can this be summarized in a few sentences?')
    ready_to_submit = len(url) > 0 and len(query) > 0
    submitted = st.form_submit_button("Submit")
    if submitted:
        transform(url, query)
