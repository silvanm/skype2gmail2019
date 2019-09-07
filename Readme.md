Skype2Gmail
===========

Imports Skype messages to Gmail for better indexability.

In this case it's using the export file from https://secure.skype.com/en/data-export as 
it is not possible anymore to access the Skype message database anymore. 

How it works
------------

1. Setup the Gmail-API as described [here](https://github.com/silvanm/slack2gmail)
2. Install dependencies using `poetry install`
3. Place the file `messages.json` you downloaded from https://secure.skype.com/en/data-export in 
   the root directory of this app
4. Run `python3 skype2gmail.py`

It will import all messages more recent than the date specified in /var/status.json
