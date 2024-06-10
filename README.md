# VAIL Lockout Discord Bot
 A Discord.py-based Discord bot that helps users organize Minecraft-style Lockout Races in VAIL. Not affiliated with VAIL/AEXLAB. Does not integrate with the VAIL game directly. 

### What is a Lockout Race?
 A Lockout Race (often just called a "Lockout") is race between two players to complete a set number of challenges in a given game. However, both players are given the same set of challenges, and once one person does a challenge, the other player is Locked Out of completing the same one, hence the name.

This project is very much a work in progress and may break during use. Not (yet) designed for use in highly populated servers.
Just saying, I warned you

If you actually want to use/test this, you'll need
- Python 3 and these libraries
  - discord.py
  - asyncio
- A discord bot of your own to run the script on
  - put the bot's token in a text file called "botToken.txt" in tha same folder as the main script. just paste in the token, no formatting
- some patience

The bot requires permissions to send messages and use slash commands in any server it is added to.
Bot hosters, you also need to enable the "Message Content" Priveleged Gateway Intent. I'm trying to find a way to work around this.
User installation not officially supported in any capacity.


when running the bot, use !help for a command list, and !racehelp for an FAQ.


also if you have any ideas for challenges to add to the list, DM me (@iampancake on Discord)
