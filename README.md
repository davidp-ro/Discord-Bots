# Steam Stats and News Discord Bot

Small bot that gives you different stats and the latest news for your favorite games.

[Add this bot to your Discord Server!](https://discordapp.com/api/oauth2/authorize?client_id=697719810791833680&permissions=52288&scope=bot)

#

### Help command: !plzhelp

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
        Note: This is still Work In Progress.
        This will get as many stats as Steam provides for the game that you search.
            Game ID - Same as above.
            Player Name - You probably know this :) But if you don't: It's what comes after /id/ on your profile page.
        Example: !stats 730 Bob The Builder will show all the stats from CS:GO for everyones favorite builder, Bob.