Termeet
========

 **Termeet** (/təːmiːt/), coined from ‘terminal’ + ‘tweet’, is yet another twitter client that runs on terminal.
 This aims to be i) first basic and minimalist, and ii) one-of-a-kind client by having tiny yet useful-for-some features.
 Under development: won’t work for you for now.

### Requirements

* python3.3 or later (probably works with older versions of python3, but I’ve never tried.)
* [twython](https://github.com/ryanmcgrath/twython) that is not too old.
* Terminal that supports 256-colour (16 colours might be sufficient. That depends on future developments.).

### Possible Features in the Future

Some of these shall be implemented, some of these not.

- [ ] Usual stuff: tweet, RT, fav, follow, view sb’s profile, ...
- [ ] Fancy colours on terminal.
- [ ] Multi accounts support.
- [ ] View images on terminal (no, really!)
- [ ] Nicely script-able.
- [ ] User stream support?
- [ ] Comprehensive mute settings.
- [ ] Tweet self-destructive tweets.
- [ ] “Virtual Follow” : follow on this client, not on twitter.
- [ ] Works like an interpreter : type `rgb #ff33dd` to post the colour sample, use `suddendeath` comand to surround your text, or `weather [cityname]` command to tweet your local weather forecast!

### License

This is mostly for my personal use, but in case somebody finds it useful, termeet is licensed under MIT.
See ./LICENSE for the actual license terms.

### Acknowledgements

The basic concept of this client --- twitter client working on CUI via commands --- is from [popotter](https://subversion.assembla.com/svn/popotter/),
from which some command names such as `ls` and `:q` are borrowed. The script itself is written from scratch, though.
