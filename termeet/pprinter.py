#!/usr/bin/env python3

from textwrap import dedent
import re
from colors import prettify as p
from html.parser import unescape as usc

htmltag = re.compile(r'<[^>]+>')

def pptweet(tweet):
    """
    get a tweet object and returns pretty-printed string.
    """
    return dedent("""\
        {scn} {via} {client} {at} {time} ({name}) [faved : {fvcnt}, RT-ed : {rtcnt}]
         »{faved}{rt}\t{text}"""
    ).format(
        name = p(usc(tweet['user']['name']),'light green',None,'bold'),
        scn = p("@"+tweet['user']['screen_name'].ljust(15),'light cyan'),
        via = p("via",'dark gray'),
        client = p(usc(htmltag.sub('',tweet['source'])), 'dark gray'),
        at = p("at",'dark gray'),
        time = p(tweet['created_at'],'dark gray'),
        text = wraptext(usc(tweet['text'])),
        faved = (p('f',None,'yellow') if tweet['favorited']
                        else p('f','dark gray')),
        rt = (p('R', None,'green') if tweet['retweeted']
                else p('R', 'dark gray')),
        fvcnt = tweet['favorite_count'],
        rtcnt = tweet['retweet_count'],
    )

def ppuser(user):
    if user['following']:
        status = p("✔",'green') + "following"
    elif user['follow_request_sent']:
        status = p("request pending", 'yellow')
    else:
        status = "Not following"
    return dedent("""\
    {usrname} {scrname} {verified}
    \t{loc}
    \t{dscr}
    \t{tweets} tweets / {favs} favs / {fling} following / {flers} followers / {listed} listed
    \t{status} {protected}
    \tSince {since} / lang:{lang} / timezone:{timezone}
    """).format(
        usrname = p(usc(user['name'],None,None,'bold')),
        scrname = p("@"+usc(user['screen_name']),'yellow'),
        verified = p("Verified",'blue') if user['verified'] else "",
        loc = usc(user['location']),
        dscr = wraptext(usc(user['description']),"\t"),
        tweets = user['statuses_count'],
        favs = user['favourites_count'],
        fling = user['friends_count'],
        flers = user['followers_count'],
        listed = user['listed_count'],
        status = status,
        protected = "Protected" if user['protected'] else '',
        since = user['created_at'],
        lang = user['lang'],
        timezone = user['time_zone'],
    )

def wraptext(text, heading="    \t"):
    return ('\n'+heading).join(text.split('\n'))
