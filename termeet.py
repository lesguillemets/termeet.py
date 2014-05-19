#!/usr/bin/env python3

import twython
from twython import Twython
import pickle
import consts
import pprinter

def log(it):
    print(it)

with open("./.user_info", 'rb') as f:
    user_info = pickle.load(f)

class Termeet(object):
    
    def __init__(self):
        tokens = user_info[0]['keys']
        try:
            self.api = Twython(
                consts.keys['API_KEY'],
                consts.keys['API_SECRET'],
                tokens['access_token'],
                tokens['access_token_secret'],
            )
        except:
            log("Error")
    
    def txtupdate(self, text):
        try:
            self.api.update_status(status=text)
        except twython.exceptions.TwythonError as e:
            print("Couldn't update status due to")
            print(e.msg)
    
    def gettimeline(self):
        tl = self.api.get_home_timeline()
        for tw in tl:
            print(pprinter.pptweet(tw))
    
    def mainloop(self):
        while True:
            try:
                cmd = input(' > ')
            except EOFError as e:
                print()
                break
            if ' ' in cmd:
                body = cmd[cmd.find(' ')+1:]
                cmd = cmd[:cmd.find(' ')]
            print("#####{}#####".format(cmd))
            if cmd == 'tw':
                self.txtupdate(body)
            elif cmd == 'ls':
                self.gettimeline()
            elif cmd == ':q':
                break

if __name__ == "__main__":
    termeet = Termeet()
    termeet.mainloop()
