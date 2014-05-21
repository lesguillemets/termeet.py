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
        {scn} {via} {client} {at} {time} ({name}) [faved : {fvcnt}, RT-ed : {rtcnt}]
         »{faved}{rt}\t{text}"""
    ).format(
        name = p(tweet['user']['name'],'light green',None,'bold'),
        scn = p("@"+tweet['user']['screen_name'].ljust(15),'light cyan'),
        via = p("via",'dark gray'),
        client = p(htmltag.sub('',tweet['source']), 'dark gray'),
        at = p("at",'dark gray'),
        time = p(tweet['created_at'],'dark gray'),
        text = wraptext(tweet['text']),
        faved = (p('f',None,'yellow') if tweet['favorited']
                        else p('f','dark gray')),
        rt = (p('R', None,'green') if tweet['retweeted']
                else p('R', 'dark gray')),
        fvcnt = tweet['favorite_count'],
        rtcnt = tweet['retweet_count'],
    )

def wraptext(text, heading="    \t"):
    return ('\n'+heading).join(text.split('\n'))
