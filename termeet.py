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
    
    def gettimeline(self, n=20):
        self.tl = self.api.get_home_timeline(count=n)
        for (i,tw) in enumerate(self.tl):
            print(str(i).rjust(3)+pprinter.pptweet(tw))
    
    def fav(self,tlnumber):
        try:
            twid = self.tl[tlnumber]['id']
        except IndexError:
            print("no index")
            return
        self.api.create_favorite(id=twid)
    
    def mainloop(self):
        while True:
            body = None
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
                self.gettimeline(body)
            elif cmd == 'f':
                ids = body.split(' ')
                for i in ids:
                    self.fav(int(i))
            elif cmd == ':q':
                break

if __name__ == "__main__":
    termeet = Termeet()
    termeet.mainloop()
