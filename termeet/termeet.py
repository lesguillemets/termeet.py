#!/usr/bin/env python3

from twython.exceptions import TwythonError
from twython import Twython
import pickle
import readline
import sys
import consts
import pprinter

def log(it):
    print(it)

with open("./.user_info", 'rb') as f:
    user_info = pickle.load(f)

class Termeet(object):
    
    def __init__(self):
        self.setaccount(0)
    
    def setaccount(self,n):
        tokens = user_info[n]['keys']
        try:
            self.api = Twython(
                consts.keys['API_KEY'],
                consts.keys['API_SECRET'],
                tokens['access_token'],
                tokens['access_token_secret'],
            )
        except Exception as e:
            log(e)
        self.mode = 'tl'
        self.tweets = {
            'tl' : [], # home timeline.
            'myfavs' : [],
            'lists' : {},
        }
    
    def getnthtweet(self,n):
        try:
            return self.tweets[self.mode][n]
        except IndexError:
            print("Beyond Index")
            raise TweetBeyondIndexError
    
    def txtupdate(self,text):
        if not text:
            text = sys.stdin.read()
        try:
            self.api.update_status(status=text)
        except TwythonError as e:
            print("Couldn't update status due to")
            print(e.msg)
    
    def txtreply(self,twn,text):
        if not text:
            text = sys.stdin.read()
        try:
            target = self.getnthtweet(twn)
        except TweetBeyondIndexError:
            return
        text = '@' + target['user']['screen_name'] + ' ' + text
        try:
            self.api.update_status(
                status = text,
                in_reply_to_status_id = target['id'])
        except TwythonError as e:
            print(e)
            return
    
    def deltweet(self,twn):
        try:
            targetid = self.getnthtweet(twn)['id']
        except TweetBeyondIndexError:
            return
        try:
            self.api.destroy_status(id=targetid)
        except TwythonError as e:
            print(e)
            return
    
    def gettimeline(self, n):
        if n:
            n = int(n)
        else:
            n = 20 # n might be None, so this lengthy code is required
        self.mode = 'tl'
        if self.tweets['tl']:
            newupdates = self.api.get_home_timeline(since_id=self.getnthtweet(0)['id'])
        else:
            newupdates = self.api.get_home_timeline(count=n)
        self.tweets['tl'] = newupdates + self.tweets['tl']
        for (i,tw) in enumerate(self.tweets['tl'][:n]):
            print(str(i).rjust(3)+pprinter.pptweet(tw))
    
    def fav(self,twnumber):
        try:
            twid = self.getnthtweet(twnumber)['id']
        except TweetBeyondIndexError:
            return
        try:
            self.api.create_favorite(id=twid)
            self.tweets[self.mode][twnumber]['favorited'] = True
            # TODO: doesn't work if ls->f 1 -> gf -> ls
        except TwythonError as e:
            print(e)
    
    def unfav(self,twnumber):
        try:
            twid = self.getnthtweet(twnumber)['id']
        except TweetBeyondIndexError:
            return
        try:
            self.api.destroy_favorite(id=twid)
            self.tweets[self.mode][twnumber]['favorited'] = False
        except TwythonError as e:
            print(e)
            return
    
    def rt(self,twnumber):
        try:
            twid = self.getnthtweet(twnumber)['id']
        except TweetBeyondIndexError:
            return
        try:
            self.api.retweet(id=twid)
            self.tweets[self.mode][twnumber]['retweeted'] = True
        except TwythonError as e:
            print(e)
            return
    
    def view_user_info(self,scrname):
        try:
            users = self.api.lookup_user(screen_name=scrname)
        except TwythonError as e:
            print(e)
            return
        for user in users:
            print(pprinter.ppuser(user))
            self.view_user_tweets(user['screen_name'])
    
    def view_user_tweets(self,scrname,n=10):
        try:
            tweets = self.api.get_user_timeline(
                screen_name=scrname,
                count = n)
        except TwythonError as e:
            print(e)
            return
        for tweet in tweets:
            print(pprinter.pptweet(tweet))
    
    def view_limits(self, resources=["statuses","users"]):
        try:
            rls = self.api.get_application_rate_limit_status(
                resources = ','.join(resources)
            )['resources']
        except TwythonError as e:
            print(e)
            return
        for resource_name in resources:
            res = rls[resource_name]
            for action in [
                    "/statuses/home_timeline",
                    "/statuses/user_timeline",
                    "/users/lookup"
            ]:
                try:
                    print(action + '\t'+ pprinter.pplimit(res[action]))
                except KeyError:
                    pass
    
    def viewmyfavs(self, n=20):
        self.mode = 'myfavs'
        if self.tweets['myfavs']:
            newfavs = self.api.get_favorites(
                since_id=self.myfavs[0]['id'])
        else:
            newfavs = self.api.get_favorites(count=n)
        self.tweets['myfavs'] = newfavs + self.tweets['myfavs']
        print("==Favs==")
        for (i,tw) in enumerate(self.tweets['myfavs'][:n]):
            print(str(i).rjust(3)+pprinter.pptweet(tw))
    
    def checkout(self,n):
        if len(user_info) < n+1:
            print("no such account")
            return
        else:
            self.setaccount(n)
    
    def read_more(self,n=20):
        if n:
            n = int(n)
        else:
            n = 20
        oldestid = self.tweets[self.mode][-1]['id']
        try:
            if self.mode == 'tl':
                older = self.api.get_home_timeline(
                    max_id = oldestid,
                    count = n
                )
            elif self.mode == 'myfavs':
                older = self.api.get_favorites(
                    max_id = oldestid,
                    count = n
                )
        except TwythonError as e:
            print(e)
            return
        if older:
            for tw in older:
                print(pprinter.pptweet(tw))
            self.tweets[self.mode].extend(older)
    
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
            elif cmd == 'r' or cmd == 'rep':
                if ' ' in body:
                    num = int(body[:body.find(' ')])
                    text = body[body.find(' ')+1:]
                else:
                    num = int(body)
                self.txtreply(num,text)
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
            elif cmd == 'rt':
                self.rt(int(body))
            elif cmd == 'rm':
                self.deltweet(int(body))
            elif cmd == "checkout":
                self.checkout(int(body))
            elif cmd == "gu":
                self.view_user_info(body)
            elif cmd == "limits":
                self.view_limits()
            elif cmd == 'more':
                self.read_more()
            elif cmd == ':q':
                break

class TweetBeyondIndexError(Exception):
    pass

if __name__ == "__main__":
    termeet = Termeet()
    termeet.mainloop()
