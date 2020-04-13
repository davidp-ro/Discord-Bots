# Steam Stats and News Discord Bot

_Small bot that gives you different stats and the latest news for your favorite games._

#

[**Add this bot to your Discord Server!**](https://discordapp.com/api/oauth2/authorize?client_id=697719810791833680&permissions=52288&scope=bot)

#

## Help command: !plzhelp

### If you want to use this locally, you need to suply your own keys and create a _key.secret_ file with the format:
    
#### _Also take a look at the [License file](LICENSE) to make sure we are on the same page :)_

    DISCORD_KEY     = your_discord_bot_key
    STEAM_API_KEY   = your_steam_api_key
    BOT_MGMT_KEY    = ~Here put whatever you want. Only used when admin/debug commands are used.~
    
* **Requirements**:
        
    [Requests](https://requests.readthedocs.io/en/master/)
    
    [Steam(unofficial)](https://pypi.org/project/steam/)
    
    [Discord.py](https://discordpy.readthedocs.io/en/latest/)

This was built on [Python 3.7.7](https://www.python.org/downloads/release/python-377/)

#

## Command list:
    !plzhelp - list all commands 
    !devhelp - WIP - show the syntax for developer/admin commands
---
    !news Game ID
        This gives you the 3 latest news of a game from it's Steam Page.
        How  to get the Game ID? A couple of ways:
            1. Hovering on the desktop status will display the link which includes the ID
            2. Going to the Steam Page and at the top the link will also display the ID
            3. Guessing :) Maybe you will find something interesting
        Example: !news 730 is CS:GO
---
    !stats Game ID Player Name
        This will get as many stats as Steam provides for the game that you search.
            Game ID - Same as above.
            Player Name - You probably know this :) But if you don't: It's what comes after /id/ on your profile page.
        Example: !stats 730 Bob The Builder will show all the stats from CS:GO for everyones favorite builder, Bob.

# **Disclaimer**:
        Steam Stats Discord Bot is not associated/affiliated with Steam Inc. in any way shape or form.
        Steam Stats Discord Bot is not in any way shape or form endorsed by Steam Inc.

        Any copyright related issues shall be addresed either as an Issue on the github repository,
    https://github.com/davidp-ro/Discord-Bots/issues, if it's not high-priority, or if neccesary on the
    email: davidpescariu12 (at) gmail (dot) com