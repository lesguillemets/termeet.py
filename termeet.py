#!/usr/bin/env python3

from twython.exceptions import TwythonError
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
        except Exception as e:
            log(e)
        self.tl = []  # home timeline.
        self.tweets = []  # tweets now indexed.
        self.myfavs = []
    
    def txtupdate(self, text):
        try:
            self.api.update_status(status=text)
        except TwythonError as e:
            print("Couldn't update status due to")
            print(e.msg)
    
    def gettimeline(self, n):
        if n:
            n = int(n)
        else:
            n = 20
        if self.tl:
            newupdates = self.api.get_home_timeline(since_id=self.tl[0]['id'])
        else : newupdates = self.api.get_home_timeline(count=n)
        self.tl = newupdates + self.tl
        self.tweets = self.tl[:n]
        for (i,tw) in enumerate(self.tweets):
            print(str(i).rjust(3)+pprinter.pptweet(tw))
    
    def fav(self,twnumber):
        try:
            twid = self.tweets[twnumber]['id']
        except IndexError:
            print("no index")
            return
        try:
            self.api.create_favorite(id=twid)
            self.tweets[twnumber]['favorited'] = True
        except TwythonError as e:
            print(e)
    
    def unfav(self,twnumber):
        try:
            twid = self.tweets[twnumber]['id']
        except IndexError:
            print("no index")
            return
        try:
            self.api.destroy_favorite(id=twid)
            self.tweets[twnumber]['favorited'] = False
        except TwythonError as e:
            print(e)
            return
    
    def viewmyfavs(self, n=20):
        if self.myfavs:
            newfavs = self.api.get_favorites(
                since_id=self.myfavs[0]['id'])
        else:
            newfavs = self.api.get_favorites(count=n)
        self.myfavs = newfavs + self.myfavs
        self.tweets = self.myfavs[:n]
        print("==Favs==")
        for (i,tw) in enumerate(self.tweets):
            print(str(i).rjust(3)+pprinter.pptweet(tw))
    
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
            elif cmd == 'uf':
                ids = body.split(' ')
                for i in ids:
                    self.unfav(int(i))
            elif cmd == 'gf':
                self.viewmyfavs()
            elif cmd == ':q':
                break

if __name__ == "__main__":
    termeet = Termeet()
    termeet.mainloop()
