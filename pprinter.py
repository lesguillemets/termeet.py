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
        {scn} {via} {client} {at} {time} ({name}):
         »\t{text}"""
    ).format(
        name = p(tweet['user']['name'],'light green',None,'bold'),
        scn = p("@"+tweet['user']['screen_name'].ljust(15),'light cyan'),
        via = p("via",'dark gray'),
        client = p(htmltag.sub('',tweet['source']), 'dark gray'),
        at = p("at",'dark gray'),
        time = p(tweet['created_at'],'dark gray'),
        text = tweet['text'],
    )
