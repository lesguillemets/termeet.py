#!/usr/bin/env python3
from twython import Twython
import pickle
import consts

def adduser():
    tw = Twython(
        consts.keys['API_KEY'],
        consts.keys['API_SECRET'],
    )
    auth = tw.get_authentication_tokens()
    tw = Twython(
        consts.keys['API_KEY'],
        consts.keys['API_SECRET'],
        auth['oauth_token'],
        auth['oauth_token_secret']
    )
    print("Please visit the following page and authenticate!")
    print(auth['auth_url'])
    print(" ... and enter the PIN code.")
    pin = input(" PIN? \t>")
    final = tw.get_authorized_tokens(pin)
    oauth_token = final['oauth_token']
    oauth_token_secret = final['oauth_token_secret']
    try:
        api = Twython(
                consts.keys['API_KEY'],
                consts.keys['API_SECRET'],
                oauth_token,
                oauth_token_secret
        )
    except Exception as e:
        print("Error:{}\n Please try again.".format(e))
        return
    print("Successfully authenticated @{}".format(final['screen_name']))
    
    with open("./.user_info", 'rb') as f:
        user_info = pickle.load(f)
    user_info.append(
        {'name' : final['screen_name'],
         'keys' :
            { 'access_token' : oauth_token,
              'access_token_secret' : oauth_token_secret}
        }
    )
    with open("./.user_info", 'wb') as f:
        pickle.dump(user_info,f)

adduser()
