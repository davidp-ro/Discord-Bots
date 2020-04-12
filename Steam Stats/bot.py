"""
Author: David Pescariu, github.com/davidp-ro
License: MIT, see my github.

How to use:
    -- Detailed explaination in the README.md file
    TODO: Complete this.
"""

# Imports:
import requests
import steam
import re

# Discord:
import discord
client = discord.Client()

# Constants and keys/tokens:
CALL_TAG = '!'
TOKENS = [] # 0-Discord 1-Steam Api 2-Bot Dev Commands
with open('key.secret', 'r') as tokens:
    lines = tokens.readlines()
    for line in lines:
        TOKENS.append(str(line)[18:-1])


# Steam:
def transform_steam_url_to_steam64ID(id_):
    """
        This is used in order to conevert the 'readable' steam URL to the Steam64 ID,
    that's used in the official API.

    Params:
        id_ - Anything, The characters next to the /id/ in the steam profile link.

    Returns:
        Int - SteamID64
    """
    link = 'https://steamcommunity.com/id/' + str(id_)
    return steam.steamid.steam64_from_url(link, http_timeout=30)

def get_news_from_steamNetAPI(game_id):
    """
        This is the function that gets the latest news of a game from the Steam API.

    Params:
        game_id - Integer, usually 3 digits.

    Returns:
        List - Contains 3 dictionaries with the 'actual' news.
    """
    game_news_api_link = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid='+game_id+'&count=3&maxlength=300&format=json'
    req_ = requests.get(game_news_api_link)
    recived_json = req_.json()

    appnews_ = recived_json.get("appnews")
    news_ = appnews_.get("newsitems")

    return news_


# Discord Steam Stats Bot - v1.2 - github.com/davidp-ro 
# Initial setup for discord: 
@client.event
async def on_ready():
    print('[Start] Bot logged on as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='!plzhelp'))

# Main Bot Code
@client.event
async def on_message(message):
    if message.author == client.user:
        # Ignoring becuase it's the bot...
        return
    else: # Check if it's a command
        # Normal User Commands:
        if message.content.startswith(CALL_TAG + 'plzhelp'):
            await message.channel.send('Steam Stats bot - v1.1\n!news *Game ID* <- latest news from a game, *ex: !news 730 - CS:GO*\n!getstatsforcs *account*')
        
        if message.content.startswith(CALL_TAG + 'devhelp'):
            await message.channel.send('Syntax: !key=DEV_KEY <admin command>')


        if message.content.startswith(CALL_TAG + 'news'):
            game_id = str(message.content)[6:]
            news = get_news_from_steamNetAPI(game_id)
            news_1 = str(news[0].get('contents'))
            news_2 = str(news[1].get('contents'))
            news_3 = str(news[2].get('contents'))

            news_1 = re.sub('<[^>]+>', '', news_1)
            news_2 = re.sub('<[^>]+>', '', news_2)
            news_3 = re.sub('<[^>]+>', '', news_3)

            await message.channel.send('Some small bugs are still here, sometimes random characters show due to the way Valve formats their news ¯\_(ツ)_/¯')
            await message.channel.send('```' + news_1 + '```')
            await message.channel.send('```' + news_2 + '```')
            await message.channel.send('```' + news_3 + '```')
            #end !news


        if message.content.startswith(CALL_TAG + 'getstatsforcs'):
            await message.channel.send('Not implemented yet. ¯\_(ツ)_/¯')
        
        
        # Admin Commands:
        if message.content.startswith(CALL_TAG + 'key=' + TOKENS[2]):
            if(str(message.content)[18:30] == 'bot_ban_user'):
                '''
                Usage: !key=DEV_KEY UserTag

                Add users to a ban list.

                FIXME: Not fully implemented yet.
                '''
                usr_to_ban = str(message.content)[31:]
                print(f'[Info] {usr_to_ban} has been added to the banned people list')

# Discord bot upload:
client.run(TOKENS[0])

#*********************** END **********************
