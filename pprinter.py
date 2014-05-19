#!/usr/bin/env python3

from textwrap import dedent
import re
from colors import prettify as p

htmltag = re.compile(r'<[^>]+>')

def pptweet(tweet):
    """
    get a tweet object and returns pretty-printed string.
    """
    return dedent("""\
        {name} @{scn} {via} {client} {at} {time}:
         »\t{text}"""
    ).format(
        name = p(tweet['user']['name'],'green',None,'bold'),
        scn = p(tweet['user']['screen_name'],'cyan'),
        via = p("via",'dark gray'),
        client = p(htmltag.sub('',tweet['source']), 'light gray'),
        at = p("at",'dark gray'),
        time = p(tweet['created_at'],'light gray'),
        text = tweet['text'],
    )
