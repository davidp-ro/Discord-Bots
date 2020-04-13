"""
Author: David Pescariu, github.com/davidp-ro

Built with ❤️ and fully open-source.

How to use:
    -- Detailed explaination of the commands in the README.md file
    
    * If you want to use this locally, you need to suply your own keys and create a key.secret file with the format:
        DISCORD_KEY     = your_discord_bot_key
        STEAM_API_KEY   = your_steam_api_key
        BOT_MGMT_KEY    = ~Here put whatever you want. Only used when admin/debug commands are used.~
    
    Requirements:
        Requests: https://requests.readthedocs.io/en/master/
        Steam(unofficial): https://pypi.org/project/steam/
        Discord.py: https://discordpy.readthedocs.io/en/latest/

    This was built on Python 3.7.7

License:
    
    MIT License ~~~ Copyright (c) 2020 David Pescariu

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Disclaimer:
    Steam Stats Discord Bot is not associated/affiliated with Steam Inc. in any way shape or form.
    Steam Stats Discord Bot is not in any way shape or form endorsed by Steam Inc.

    Any copyright related issues shall be addresed either as an Issue on the github repository,
https://github.com/davidp-ro/Discord-Bots/issues, if it's not high-priority, or if neccesary on the
email: davidpescariu12 (at) gmail (dot) com

"""

# Logger:
import logging
logging.basicConfig(filename='Steam-Stats.log', filemode='w', level='INFO',format='%(asctime)s - %(name)s [%(levelname)s] %(message)s', datefmt='%d-%b-%y %H:%M:%S')
logging.info('Importing...')

# Imports:
import requests
import steam
import re
import datetime

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

logging.info('Imports succesfull.')


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
    try:
        link = 'https://steamcommunity.com/id/' + str(id_)
        return steam.steamid.steam64_from_url(link, http_timeout=30)
    except Exception as exc:
        logging.warning('Unexpected exception!')
        logging.exception('Execption in transform_steam_url_to_steam64ID')

def get_news_from_steamNetAPI(game_id):
    """
        This is the function that gets the latest news of a game from the Steam API.

    Params:
        game_id - Integer

    Returns:
        List - Contains 3 dictionaries with the 'actual' news.
    """
    try:
        game_news_api_link = 'http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid='+game_id+'&count=3&maxlength=300&format=json'
        req_ = requests.get(game_news_api_link)
        recived_json = req_.json()

        appnews_ = recived_json.get("appnews")
        news_ = appnews_.get("newsitems")

        return news_
    except Exception as exc:
        logging.warning('Unexpected exception!')
        logging.exception('Execption in get_news_from_steamNetAPI')

def get_player_stats_for_game(game_id, player_id):
    """
        This is the function that get the stats and puts them in a nice format(a list) to show in discord.

    Params:
        game_id - Integer
        player_id - Integer, MUST be the Steam64ID!

    Returns:
        List - even=item, odd=value
    """
    player_stats_api_link = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid='+str(game_id)+'&key='+str(TOKENS[1])+'&steamid='+str(player_id)
    stats = []
    try:
        req_ = requests.get(player_stats_api_link)
        recived_json = req_.json()
        player_stats_ = recived_json.get('playerstats')
        player_stats = player_stats_.get('stats')

        for each in player_stats:
            for val in each :
                stats.append(each[val])

        return stats
    
    except:
        stats.append('not_found')
        return stats



# Discord Steam Stats Bot - v2.0 - github.com/davidp-ro 
# Initial setup for discord: 
@client.event
async def on_ready():
    """
        Starting and setting the rich pressence for the bot.

    Params:
        None
    
    Returns:
        None
    """
    print('[Start] Bot logged on as {0.user}'.format(client))
    await client.change_presence(activity=discord.Game(name='!plzhelp'))
    logging.info('Bot logged on as {0.user}'.format(client))

# Main Bot Code
@client.event
async def on_message(message):
    """
        Responding to recived messages.

    Params:
        None here. Called by discord.js
    
    Returns:
        None
    """

    # Doing some stuff in fucntions to try and clean the code a bit.
    # Getting player stats and show them in an embed:
    def get_player_stats_to_show(msg_):
        """
            Function that generates the player stats and separates them in oreder to be used in the embed that shows them.

        Params:
            msg_ - String, user !stats command message.

        Returns:
            List, List - The 2 lists containing left and right text.
        """
        game_id = msg_[1]
        player_ = msg_[2]
        
        # Convert player id from link to Steam64:
        player_id = transform_steam_url_to_steam64ID(player_)
        # Get the Stats list:
        stats = get_player_stats_for_game(game_id, player_id)
        
        text_left, text_right = "", ""
        i, j = 0, 2
        step = 4
        maxsize = len(stats) / 4 #FIXME: THIS IS TEMPORARY. Maximum limit for each embed element is 1024 chars but atm I am doing this dirty just to have a working stats command.

        while i < (maxsize - step):
            if(str(stats[i]).startswith('GI')):
                i += step # I want to ignore them because they're just too long and not very usefull.
            else:
                stats[i] = str(stats[i]).replace('_', ' ') # Switch from snake case
                stats[i] = stats[i].title() # Capitalize each first letter
                text_left += stats[i] + ' - ' + str(stats[i+1]) + '\n'
                i += step
        while j < (maxsize - 2):
            if(str(stats[j]).startswith('GI')):
                j += step # I want to ignore them because they're just too long and not very usefull.
            else:
                stats[j] = str(stats[j]).replace('_', ' ') # Switch from snake case
                stats[j] = stats[j].title() # Capitalize each first letter
                text_right += stats[j] + ' - ' + str(stats[j+1]) + '\n'
                j += step

        return text_left, text_right

    # Actually showing the embed.
    async def show_player_stats(text_left, text_right):
        """
            This function sends the embed message containing the player stats for the respective game.

        Params:
            text_left - String, left side of the embed
            text_right - String right side of the embed

            Both can be generated using the get_player_stats_to_show(msg_) function.

        Returns:
            None
        """
        embed = discord.Embed(title="WIP(aka not all stats shown)", colour=discord.Colour(0x5168bb), timestamp=datetime.datetime.utcfromtimestamp(1586763369))

        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/697719810791833680/dd6d71e2bd5f3670d3342f5bc714fe41.png?size=256")
        embed.set_author(name="All the steam stats :)", url="https://discordapp.com")
        embed.set_footer(text="Lots of data so sorry for the spam :)", icon_url="https://cdn.discordapp.com/avatars/474134951109853185/0b0abc779eb1ef4ae755d38e65282abc.png")

        embed.add_field(name="Stats:", value=text_left, inline=True)
        embed.add_field(name="and some more:", value=text_right, inline=True)

        await message.channel.send(embed=embed)

    if message.author == client.user:
        # Ignoring becuase it's the bot...
        return
    else: # Check if it's a command
        # Normal User Commands:
        if message.content.startswith(CALL_TAG + 'plzhelp'):
            await message.channel.send('Steam Stats bot - v2.0\n!news *Game ID* <- latest news from a game, *ex: !news 730 - CS:GO*\n!stats Game Account')
        
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
            #end !news TODO: Maybe make the news in an embed as well.


        if message.content.startswith(CALL_TAG + 'stats'):
            msg_ = str(message.content).split(' ')
            text_left, text_right = get_player_stats_to_show(msg_)

            #print('LEFT:' + text_left + 'RIGHT:' + text_right + '\n')
            #await message.channel.send('.')
            
            await show_player_stats(text_left, text_right)
            

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
