//**************** Deps: ****************/
const request = require('request');
const _ = require('lodash');

//*************** Discord ***************/
const Discord = require('discord.js');
const client = new Discord.Client();

/***************************************************************************************/

/***************************************************************************************/

/* functie provizorie */
function extractItems(data) {
  var playerstats = _.get(data, 'playerstats');
  if (!playerstats) {
    return [];
  }
  return _(playerstats)
    .keys()
    .map(function(id) {
      return _.pick(playerstats[id], ['name', 'value']);
    })
    .value();
}
/*********************/



/* Discord Steam Stats Bot - v1.1 - github.com/davidp-ro */

/* Initial setup for discord: */
client.on('ready', () => {
    client.user.setActivity(`Use f!help.`, {type: "playing"});  
    console.log(`[Start] Logged in as ${client.user.tag}!`);
});

/* Main bot code: */
client.on('message', msg => {
    msg_ = msg.content
    var steamid = msg_.match(/\d/g);
    if (steamid != null) {
        steamid = steamid.join("");
    }

    /* Debug/Developer commands: */
    if(msg_.includes('!db_refresh_bot')){
        if(msg_.includes(dev_key)){
            msg.reply('Update-ing...') 
        }
        else {
            msg.reply('Developer settings / debug settings require a private key.\nSyntax: !cmd key=DEV_KEY')
            console.log('[WARN] Attempt to run a db command without key - user: ' + msg.author.tag);
        }
    }
    if(msg_.includes('!db_version')){
        if(msg_.includes(dev_key)){
            msg.reply('v1.1 github.com/davidp-ro')
        }
        else {
            msg.reply('Developer settings / debug settings require a private key.\nSyntax: !cmd key=DEV_KEY')
            console.log('[WARN] Attempt to run a db command without key - user: ' + msg.author.tag);
        }
    }
         
    /* Normal commands: */
    if(msg_.includes('!test')){
        msg.channel.send(":white_check_mark: ", {files: ["https://gifimage.net/wp-content/uploads/2017/08/its-working-gif-9.gif"]})
    }
    if(msg_.includes('!serv')){
        msg.reply('[OK] - Google Compute Engine\n[OK] - Imports\n[OK] - Steam API')
    }
    if(msg_.includes('!plzhelp')){
        msg.reply('Steam Stats bot - v1.1\n!news + Game ID <- latest news from a game\n!getstatsforcs + Steam ID (!getid)')
    }
    if(msg_.includes('!getid')){
        msg.reply('Enter your steam account here: https://steamid.io/lookup then use the steamID64 for all commands.')
    }
    if(msg_.includes('!news')){
        msg.reply('[WIP]')
    }
    if(msg_.includes('!getstatsforcs')){
        const csgo_appid = '730'

        console.log('[Info] ' + steamid + ' requested CS:GO Stats');

        var url = ' http://api.steampowered.com/ISteamUserStats/GetUserStatsForGame/v0002/?appid=' + csgo_appid + '&key=' + key + '&steamid=' + steamid;
        request(url, function(err, response, body) {
            if(!err && response.statusCode < 400) {
                //msg.reply('merge, kinda');
                
                result = extractItems(JSON.parse(body))
                
                console.log(result)
                msg.reply(result)
                
            }
        });
    }
    if(msg_.includes('!make_me_admin_pls')) {
        msg.reply('*insert teapa cumetre meme here*');
    }


}); // End of main bot code.

//**************************************************/
//*************** Discord bot upload ***************/
//**************************************************/
client.login(token);
//**************************************************/
//*********************** END **********************/
//**************************************************/
