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

----------------
Error code list (theese might get shown on Discord.):

SS--EXCEPT-GET_STATS - An exception occured in the get_player_stats_for_game and got returned to discord. (status_code 1000)
SS--FAIL_UNKNOWN - Something failed where we get the stats, but it was unexpected.
SS--TRIM_FAILED - Got return_code = 9 aka module failed (Trimmer.game_stats).

SS-STEAM--FAILED_CONNECTION - Steam Servers returned 503.
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

# Other Steam Stats Modules:
from text_trim import Trimmer

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
        return id_ # This covers the case where the id is already in the SteamID format.

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
        Int - status_code, 0-Succes, 1-Bot-error, 2-Wait, 500-Internal Server Error(Steam), 503-Steam Unavailable
    """
    player_stats_api_link = 'http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid='+str(game_id)+'&key='+str(TOKENS[1])+'&steamid='+str(player_id)
    stats = []
    try:
        req_ = requests.get(player_stats_api_link)
        status_code = req_.status_code
        if(status_code == 200):
            recived_json = req_.json()
            player_stats_ = recived_json.get('playerstats')
            player_stats = player_stats_.get('stats')

            if(type(player_stats) == list):
                for each in player_stats:
                    for val in each :
                        stats.append(each[val])

                return stats, 0
            else:
                stats.append('no_stats_avail_for_this_game')
                return stats, 0
        
        else:
            # Deal with the errors:
            if (status_code <= 405):
                stats.append('not_found') # steam_stats_failed
                return stats, 1
            if (status_code == 429):
                stats.append('not_found') # rate_limiting
                return stats, 2
            if (status_code > 430):
                stats.append('not_found') # steam_api_failed
                return stats, status_code

    
    except:
        stats.append('not_found')
        return stats, 1000



# Discord Steam Stats Bot - v2.1 - github.com/davidp-ro 
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
            String, String - The 2 strings containing left and right text.
        """
        game_id = msg_[1]
        player_ = msg_[2]
        
        # Convert player id from link to Steam64:
        player_id = transform_steam_url_to_steam64ID(player_)
        # Get the Stats list:
        stats, resp = get_player_stats_for_game(game_id, player_id)
        
        #-------------------------------------
        logging.info(f'[Player-Stats] Response from steam: {resp}')
        #-------------------------------------

        """
            Dealing with errors.
        """ 
        if(stats[0] == 'not_found'):
            if(resp == 0):
                return "No stats found.", "Is your profile set to public?"
            if(resp == 1):
                return "Steam Stats failed :(\nSS--FAIL_UNKNOWN", "Try again later.\n*(This shouldn't have happened)*"
            if(resp == 2):
                return "Too many requests at a time", "Please wait a minute :O"
            if(resp == 500):
                return "Your profile might be private, or...\nSteam Servers are not happy :)\n\n[Response: 500] Internal Server Error", "Check that your profile is public, and check for typo's\nTry again later.\n\nAn unrecoverable error has occurred, please try again."
            if(resp == 503):
                return "Steam Servers are down.\n*Error code:* SS-STEAM--FAILED_CONNECTION", "Check their [status](https://steamstat.us/)"
            if(resp == 1000):
                return ":warning: Exception occured.\n*Error code:* SS--EXCEPT-GET_STATS", "If you know what this means please submit it as an issue [here](https://github.com/davidp-ro/Discord-Bots/issues)."

        elif stats[0] == 'no_stats_avail_for_this_game':
            return f"The player {player_} has no stats for {game_id}", "This can also be caused if the game does not support stats."

        else: #found:
            text_left, text_right = "", ""
            
            i, j = 0, 2
            step = 4
            maxsize = len(stats)

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
        
        embed = discord.Embed(title=f"Steam Stats for {msg_[2]}:", colour=discord.Colour(0x5168bb))

        embed.set_thumbnail(url="https://cdn.discordapp.com/app-icons/697719810791833680/dd6d71e2bd5f3670d3342f5bc714fe41.png?size=256")
        embed.set_footer(text="Suggestion / Issue? github.com/davidp-ro/Discord-Bots | Support me paypal.me/davidpescariu", icon_url="https://cdn.discordapp.com/avatars/474134951109853185/0b0abc779eb1ef4ae755d38e65282abc.png")
        
        if(len(text_left) < 900 or len(text_right) < 900):
            # We are under the 1000 char limit for one embed so we are fine:
            embed.add_field(name="Stats:", value=text_left, inline=True)
            embed.add_field(name="and some more:", value=text_right, inline=True)

            await message.channel.send(embed=embed)
        
        else: # Exceding the limit
            needed = max(len(text_left), len(text_right))
            rnd_needed = round(needed)

            if(needed > rnd_needed):
                needed = rnd_needed + 1
            else:
                needed = rnd_needed

            list_text_left, list_text_right, return_code_trimmer = Trimmer.game_stats(text_left, text_right) # Get our text that got trimmed.

            if (return_code_trimmer == 0):
                embed.add_field(name="Stats:", value=list_text_left[0], inline=True)
                embed.add_field(name="and some more:", value=list_text_right[0], inline=True)
                index = 1
                while index <= needed:
                    embed.add_field(name="...", value=list_text_left[0], inline=True)
                    embed.add_field(name="...", value=list_text_right[0], inline=True)
                    index += 1

                await message.channel.send(embed=embed)

            else:
                embed.add_field(name="Steam Stats Failed.", value="Steam Stats failed :(\nSS--TRIM_FAILED", inline=True)
                embed.add_field(name="...", value="Try again later.\n*(This shouldn't have happened)*", inline=True)

                await message.channel.send(embed=embed)
    
    if message.author == client.user:
        # Ignoring becuase it's the bot...
        return
    else: # Check if it's a command
        # Normal User Commands:
        if message.content.startswith(CALL_TAG + 'plzhelp'):
            await message.channel.send('Steam Stats bot - v2.1\n!news *Game ID* <- latest news from a game, *ex: !news 730 - CS:GO*\n!stats Game Account <- get the player stats for that game')
        
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
