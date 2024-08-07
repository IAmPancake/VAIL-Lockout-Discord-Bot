import random
import discord
from discord.ext import commands
from discord import channel
from discord import app_commands
import typing
import asyncio

#==================================================================================================================
#======== In the same folder as this script, make a file named botToken.txt and put your bot's token in it ========
#======================================= otherwise this bot will not work =========================================
#==================================================================================================================
tokenFile = open("botToken.txt")
BOT_TOKEN = tokenFile.read()
tokenFile.close()

#first we set up all the stuff relating to generating challenges
guns = ["MK418", "AK12", "AK303N", "GrotB", "MR96", "UMP45", "Vector45", "Vityaz", "APC9Pro", "G17", "MK23", "PL14","PM9", "Desert Eagle", "NXS Hammer","G28Z", "ScarH", "Kanto"]
#yes, I know it should be called "weapons" and not "guns" because the knife is here, but I already made most of the code before adding the knife so it's staying
categories = ["Rifle", "DMR", "Sidearm", "SMG", "Grenade"]
#might add sights later
maps = ["Cliffside", "Este", "Khidi", "Maar", "Miru", "Volt", "Nine", "Suna", "The Void", "Atmos"]
modes = ["CTO", "Artifact", "TDM", "FFA", "Gun Game", "Hardpoint", "SKZ", "One in the Chamber"]

#if anyone out there has a good list of all the sights in the game please tell me so I can use it to make challenges thanks

#this list is for challenges that take arguments so that they can vary between games without having to list each possibility
#i had to make it a function otherwise it'd just randomize once when you run the script and then stay the same between races. Fun.
def generateChallenges():
    listr =f"""Win a game of {random.choice(modes)}
Get {str(random.randint(3, 12))} frag nade kills
Get {str(random.randint(2, 10))} impact frag kills
Get {str(random.randint(8, 15))} kills with {random.choice(categories)}s 
Get {str(random.randint(5, 10))} knife kills
Get {str(random.randint(8, 15))} kills with the {random.choice(guns)}
Get {str(random.randint(3, 9))} kills with the {random.choice(guns)} in one life
Get a kill with every {random.choice(categories)}
Get {str(random.randint(2, 10))} kills through smoke 
Get {str(random.randint(2, 6))} headshot kills in one life
Get {str(random.randint(2, 4))} kills back-to-back {str(random.randint(1, 4))} time(s)
Get {str(random.randint(5, 10))} kills using your non-dominant hand
Get {str(random.randint(5, 10))} headshot kills using iron sights
Get {str(random.randint(5, 10))} kills with the SCARH on full auto
Capture the Hardpoint at {str(random.randint(2, 3))} different map positions in one life
Get {str(random.randint(3, 6))} kills in your first life of a match
Get {str(random.randint(3, 8))} kills using a primary weapon with one hand
Get {str(random.randint(3, 8))} kills with guns held fully sideways
Get {str(random.randint(4, 10))} kills while dual wielding guns
Win on {random.choice(maps)}
Get a kill with 3 different primary weapons in one life
Kill your Lockout opponent with a headshot
Kill your Lockout opponent twice in one life
Kill while holding the objective IN YOUR HAND (scanner, orb)
Kill an enemy while both you can them are on the hardpoint 
Kill an enemy using the same weapon as them 4 times (No SKZ, OitC)
Get a kill while YOU are flashed
Get 2+ kills with one grenade 3 times
Get 2+ kills with one BULLET
Kill through map geometry
Be alive while 5 enemy players are dead (no ART)
Kill while you are airborne
360 spin kill
Get a kill with 5 different weapons with zoom scopes (no MRO or SpitfireAR, must USE the ZOOM)
Get 2 kills with each weapon in your loadout in one life
Defuse or plant the Artifact Scanner while the entire enemy team is dead
Get a knife kill without line-of-sight on your victim
Get the most kills AND be the last one standing in one OitC game
Get 3 knife kills in one Gun Game round and win
Ride every zipline on Maar (all the way across) in one life
Win a game with fewer players on your team than on the opposing team
Kill someone with their own grenade
Hip Fire Headshot kill""".splitlines()
    return listr

#use these two lines instead of one for actually rerandomizing the full list to pick from. Why does it only work this way? I don't know and probably never will
#and i tried making it reference a dictionary for the rng methods which in theory should make it rerandomize every time an item gets pulled from the list, but it didn't work
#allChallenges = generateChallenges()


#do not uncomment the above lines

def generateClashChallenges(): #challenge list for Clash Mode only
    return f"""Kill your lockout opponent twice in one life
Kill your lockout opponent with the {random.choice(guns)} {random.randint(1, 5)} time(s)
Kill your lockout opponent with a headshot {random.randint(1, 5)} time(s)
Kill your lockout opponent with Impact Frags {random.randint(1, 5)} time(s)
Kill your lockout opponent with (normal) Frag Grenades {random.randint(1, 5)} time(s)
Kill your lockout opponent while dual wielding guns
Kill your lockout opponent with a knife throw
Kill your lockout opponent with {random.randint(2,5)} different {random.choice(categories)}s (use repeat guns if not enough unlocked)
Kill your lockout opponent using iron sights {random.randint(1, 5)} time(s)
Kill your lockout opponent with a sidearm quickdraw
Kill your lockout opponent with a weapon you didn't spawn with
Kill your lockout opponent while on the hardpoint
Beat your lockout opponent at any non-combat minigame (mini golf, tic-tac-toe, etc.)
Kill your lockout opponent with the {random.choice(guns)} {random.randint(1, 5)} time(s)
Kill your lockout opponent while you are airborne
Trickshot kill your lockout opponent (i.e. 360 spin, hip fire headshot, etc. Must be on purpose)
Kill your lockout opponent through map geometry""".splitlines()

#================actual bot behavior and such starts here

myIntents = discord.Intents.default()
myIntents.message_content = True
bot = commands.Bot(command_prefix='!', intents=myIntents)
client = discord.Client(intents=myIntents) #unnenecessary??
tree = app_commands.CommandTree(client)

usersInChallenges = [] #keep track of who's playing so no one can get challenged twice

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!') #connect bot to discord, put console output once connected
    print("v2.0, the Clash update!")
    try:
        synced = await bot.tree.sync(guild=None)
        print("command tree synced: " +str(len(synced)))
    except Exception as e:
        print("command tree failed to sync: \n"+str(e))

helpMsg = """### What is a Lockout Race?
A Lockout Race (often just called a 'Lockout') is a race between two players to complete a set number of challenges in a given game. However, both players are given the same set of challenges, and once one person does a challenge, the other player is Locked Out of completing the same one, hence the name.

### How do I use the bot?
The bot's command structure is simple. just put in '/lockoutrace' and then ping the person you want to challenge. 
This will start a first-to-13 race with a 120-second ready-up timer, so you can your opponent can open the game and party up before the race starts
you can change those settings at will when you initially call the command. Just use the extra settings in the command prompt

### What are the rules of a VAIL Lockout Race?
Other than the general concept as organized by the bot, there is no official ruleset, so feel free to come up with your own rules! Just make sure to agree on a specific ruleset before you start. 
Here's my reccomended setup:
Both players party up and queue for quickplay together, but swap to opposite teams at every opportunity.
Whenever a player completes a challenge, both players must exit the match and requeue at the end of the current game.
Also, players can agree to requeue at any time, though they MUST always queue together.
Players may not get any intentional help from other players outside the challenge.
For the purposes of challenges related to doing things 'in one life', a life can extend between Artifact rounds but not between games.

### LICENSE INFO
The bot's code can be found online at https://github.com/IAmPancake/VAIL-Lockout-Discord-Bot, under an MIT License. Full license details are available there, in the 'LICENSE' file.
Content creators, you may use my bot for whatever you want, including monetized content, with or without credit. (You may want to add credit anyway, so curious viewers can find the bot.) 

Happy racing!
-IAmPancake"""

@bot.hybrid_command(description="FAQ for the bot and VAIL Lockout races in general.", help="FAQ for the bot and VAIL Lockout races in general.") #DM's the command user with basically a README
async def racehelp(ctx): 
    global helpMsg
    try:
        await ctx.interaction.response.defer(ephemeral=True)
    finally:
        dmChannel = await ctx.author.create_dm()
        await dmChannel.send("__**TLDR; When you hit accept challenge, there'll be a short timer so you can get ready in a party with your opponent. Then, you both will be given the same list of challenges. Completing a challenge blocks your opponent from the same one. Complete the majority to win.**__")
        await dmChannel.send(helpMsg)
        #============================================================================================
        #=====================comment out the below line if hosting your own bot=====================
        #============================================================================================
        await dmChannel.send("Additional note: if you're using the instance of the bot hosted by IAmPancake (as opposed to hosting your own instance), be aware that the bot goes down for a few minutes and resets active races every day/night at <t:1718694000:t>. \n Oh, and don't be afraid to DM me if you have any issues or suggestions for challenges to add! I may not get back to you immediately, but I try to read every DM I get (for now). My tag is @iampancake.")
        try:
            await ctx.interaction.followup.send("Check your DMs for the FAQ.")
        except:
            await ctx.channel.send(f"Check your DMs for the FAQ, {ctx.author.mention}.", delete_after=5.0)
    
@bot.hybrid_command(name="generatechallenges", help="generates a user-set number of VAIL Lockout challenges.") #just give out some challenges, no racing
async def getSomeChallenges(ctx, numchallenges: int):
    allChallenges = generateChallenges() #generate the set of challenges to pull from
    if (numchallenges > len(allChallenges)):
        await ctx.send("You requested more challenges than can be generated.", delete_after = 10.0) #prevent users from generating for unique challenges than there are unique challenges
    elif (numchallenges < 1):
        await ctx.send("Cannot generate less than 1 challenge", delete_after = 10.0) #obvious
    else:
        response = random.sample(allChallenges, numchallenges) #pick a random sample of unique challenges. note that it cannot pick two of the same random challenge even if the random makes it non duplicate
        await ctx.send("\n".join(response))

@getSomeChallenges.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('you forgot to put in the number of challenges you wanted, silly.')

#------------------

class Confirm(discord.ui.View): #buttons for accepting or denying a challenge
    def __init__(self, targetUser, clashmode, ctx):
        super().__init__()
        self.value = None
        self.targetUser = targetUser
        self.clashmode = clashmode
        self.ctx = ctx
        if(self.clashmode):
            self.add_item(ClashModeInfoButton())
        
    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    @discord.ui.button(label='Accept Challenge', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if (interaction.user == self.targetUser):#only the person being challenged can accept
            self.value = True
            button.disabled = True
            #interaction.response.edit_message(view=self) #I'll try this again later
            self.stop()
        else:
            await self.ctx.send("that challenge wasn't for you, "+interaction.user.mention+"!", delete_after=3.0)
        
    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Deny Challenge', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if (interaction.user == self.targetUser): #only the person being challenged can deny
            self.value = False
            self.stop()
        else:
            await self.ctx.send("that challenge wasn't for you, "+interaction.user.mention+"!", delete_after=3.0)

    @discord.ui.button(label="What's a Lockout Race?", style=discord.ButtonStyle.blurple, row=1)
    async def helpMe(self, interaction: discord.Interaction, button: discord.ui.Button):
        #anyone can click this button to get the faq without needing to do /racehelp
        global helpMsg
        await interaction.response.send_message("in a moment, check your DMs for the FAQ.", ephemeral=True)
        dmChannel = await interaction.user.create_dm()
        await dmChannel.send("__**TLDR; When you hit accept challenge, there'll be a short timer so you can get ready in a party with your opponent. Then, you both will be given the same list of challenges. Completing a challenge blocks your opponent from the same one. Complete the majority to win.**__")
        await dmChannel.send(helpMsg)

class ClashModeInfoButton(discord.ui.Button):
    def __init__(self):
        super().__init__(style=discord.ButtonStyle.blurple, label="What is Clash Mode?", row=1)
    async def callback(self, interaction: discord.Interaction):
        print("help button2 pressed")
        await interaction.response.send_message("Clash Mode is an alternative mode for Lockout Races that features smaller challenges that focus on playing directly against your lockout opponent.\nPress \"What is a Lockout Race?\" for a description of lockout races in general.", ephemeral=True)
        print("help button2 msg sent")


class DropdownView(discord.ui.View):
    def __init__(self, challengesToList, playersInGame, ctx):
        super().__init__(timeout=300)
        self.challengesToList = challengesToList
        self.ctx = ctx
        self.playersInGame = playersInGame
        
        self.selected_value = None #challenge claimed by user
        self.claimingPlayer = None #player making the claim

        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.challengesToList, self.playersInGame, self.ctx)) #i wish I didn't need to use separate classes here, but it didn't work if i tried to make it one class for some reason. I tried every way
    
    @discord.ui.button(label='View Unclaimed Challenges', style=discord.ButtonStyle.grey) #if you just want to see the remaining challenges laid out, this button was added to do so w/o cluttering chat (uses ephemeral message)
    async def viewChallengesLeft(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("**Challenges Remaining: "+str(len(self.challengesToList))+"**\n"+"\n".join(self.challengesToList), ephemeral=True)

class Dropdown(discord.ui.Select):
    def __init__(self, bChallengesToList, players, ctx): #the "b" in "bChallengesToList" is just to differentiate from challengesToList in DropdownView
        self.bChallengesToList = bChallengesToList
        self.players = players
        self.ctx = ctx
        
        options = []
        #print(" ".join(self.bChallengesToList)) #debugging
        for i in self.bChallengesToList:
            options.append(discord.SelectOption(label=i, value=i)) 
        print("challenges have been listed for dropdown") #debug stuff
        
        super().__init__(placeholder="Choose a challenge once you've completed it", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer()
        if (interaction.user in self.players):#only people in this race can claim
            print("a challenge has been claimed")
            self.view.claimingPlayer = interaction.user
            self.view.selected_value = self.values[0] #so we can get the claiming player and what they claimed from outside this class
            self.view.stop() #prevent people from claiming multiple times from the same dropdown.
        else:
            await self.ctx.send("You aren't part of this race, "+interaction.user.mention+"!", delete_after=3.0)
        
class ViewAllChallenges(discord.ui.View): #button for seeing all challenges at end of game. Done as such to prevent clutter.
    def __init__(self, players, scores, claimedChallenges, unclaimedChallenges,):
        super().__init__()
        self.value = None
        self.players = players
        self.scores = scores
        self.claimedChallenges = claimedChallenges
        self.unclaimedChallenges = unclaimedChallenges
        
    @discord.ui.button(label='View All Challenges', style=discord.ButtonStyle.grey)
    async def viewAllChallengesEnd(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(("**Uncompleted Challenges:**\n"+"\n".join(self.unclaimedChallenges)+"\n**Challenges completed by "+self.players[0].display_name+": "+str(self.scores[self.players[0]])+"**\n"+"\n".join(self.claimedChallenges[self.players[0]])+"\n \n**Challenges completed by "+self.players[1].display_name+": "+str(self.scores[self.players[1]])+"**\n"+"\n".join(self.claimedChallenges[self.players[1]])), ephemeral=True)




#this is the actual lockout race command.
@bot.hybrid_command(name="lockoutrace", help="Challenge someone to a VAIL Lockout Race. /racehelp for desc", description="Challenge someone to a VAIL Lockout Race. /racehelp for desc")
@app_commands.describe(
    membertochallenge="Who to challenge to a Lockout Race", 
    challengestowin="Default is first to 13 challenges complete wins.",
    challengegeneratetimer="The amount of time (seconds) between challenge accepted and race start. Default is 120, to allow time to open VAIL.",
    clashmode="Type 'True' for this parameter to do a Clash Race, where all challenges are directly against your opponent")
async def LockoutRace(ctx, membertochallenge:discord.Member,challengestowin:typing.Optional[int] = 13,challengegeneratetimer:typing.Optional[int]=120,clashmode:typing.Optional[bool]=False):
    print("lockout race cmd sent")
    
    global usersInChallenges #global so that people can't be in two races at once
    numChallenges = (challengestowin*2)-1

    if clashmode: #clash mode has a different challenge set
        allChallenges = generateClashChallenges()
    else:
        allChallenges = generateChallenges() #generate list of challenges to select from at random

    if membertochallenge == ctx.author:
        await ctx.send("You can't challenge yourself to a race! try using /generatechallenges if you want to get some challenges to do by yourself.", delete_after = 30.0)
    elif membertochallenge.bot:
        await ctx.send("You can't challenge bots to races, silly.", delete_after = 10.0)
    elif ctx.author in usersInChallenges:
        await ctx.send("you cannot issue a challenge when you are already in a challenge! Either deny the incoming challenge or finish your race, whichever is applicable", delete_after = 30.0) #prevent people from challenging multiple others at once
    elif membertochallenge in usersInChallenges:
        await ctx.send("that person has either already been challenged, or is currently participating in a Lockout Race. Try again later, or with someone else.", delete_after = 30.0) #prevent people from being challenged multiple times
    elif (numChallenges > min(len(allChallenges),25)): 
        if(clashmode and (challengestowin==13)):
            await ctx.send("For clash mode, you have to specify the score limit you want yourself. Right now, the limit is first to "+str(min((int((len(allChallenges)+1)/2)),13))+".", delete_after=30.0)
        else:
            await ctx.send("You requested more challenges than can be generated. The max for this mode is first to "+str(min((int((len(allChallenges)+1)/2)),13))+".", delete_after = 30.0) #prevent users from generating more unique challenges than there are unique challenges possible to be generated
    elif (numChallenges < 1):
        await ctx.send("Cannot generate less than 1 challenge.", delete_after = 10.0) #obvious
    
    else:
        print("lockout race input legit")
        if clashmode:
            challengeMsg = (ctx.author.mention +" has challenged "+membertochallenge.mention+" to a **Clash Mode** VAIL Lockout Race!\nfirst to "+str(challengestowin)+" challenges complete wins!\nPress the 'Accept Challenge' button once ready, or press 'Deny Challenge' to deny. Expires in about 3 minutes.")
        else:
            challengeMsg = (ctx.author.mention +" has challenged "+membertochallenge.mention+" to a VAIL Lockout Race!\nfirst to "+str(challengestowin)+" challenges complete wins!\nPress the 'Accept Challenge' button once ready, or press 'Deny Challenge' to deny. Expires in about 3 minutes.")
        usersInChallenges.append(ctx.author)
        usersInChallenges.append(membertochallenge)
        view = Confirm(membertochallenge, clashmode, ctx)
        await ctx.send(challengeMsg, view=view, delete_after=181.0)
    # Wait for the View to stop listening for input...
        await view.wait()

        if view.value is None:
            print('Timed out...')
            await ctx.send(membertochallenge.mention +" took too long to accept the challenge. Sorry, "+ctx.author.mention+".")
            usersInChallenges.remove(ctx.author)
            usersInChallenges.remove(membertochallenge)
        elif view.value:
            print('Confirmed!')

            players = [ctx.author, membertochallenge] #only ppl involved may interact with buttons and stuf
            challengesCompleted = {ctx.author:[], membertochallenge:[]}
            scores = {ctx.author:0, membertochallenge:0}

            #we generated challenges before
            challengesPerGame = random.sample(allChallenges,numChallenges) #save them so they stay the same every time they get called
            challengesAvailable = challengesPerGame

            await ctx.send(ctx.author.mention+", your challenge was accepted! Hop in a party together, queue, and race to be the first to do **"+str(challengestowin)+"** of these challenges\n(and remember, once one player does a challenge, the other one is Locked Out from doing it!)")
            if challengegeneratetimer != 0:
                await ctx.send("Your challenges will be generated in about "+str(round(challengegeneratetimer/60,2))+" minutes. Take the time to open VAIL and get in a party, because the race starts as soon as the challenges are shown!")
                print("waiting for challenge timer")
                await asyncio.sleep(challengegeneratetimer) #give ppl time to open game
            DropdownMessageToSend = (ctx.author.mention+" and "+membertochallenge.mention+", here are your challenges!\nFirst to complete **"+str(challengestowin)+"** of them wins!\n"+("\n".join(challengesPerGame)))
            IsDropdownMessageSilent = False
            print("game start")
            #DropdownMessageToSend is used to consolidate multiple messages that would precede the one with the dropdown into one message 
            while((scores[ctx.author]<challengestowin)and(scores[membertochallenge]<challengestowin)):
                view = DropdownView(challengesAvailable, players, ctx)
                DropdownMessageToSend += ("\nThe score is **"+str(ctx.author.mention+" "+str(scores[ctx.author])+" : "+str(scores[membertochallenge])+" "+membertochallenge.mention+"**\nFirst to "+str(challengestowin)+" challenges complete wins!\nChoose a challenge to claim (note: claims as soon as you click!"))
                await ctx.send(DropdownMessageToSend, view=view, silent=IsDropdownMessageSilent, delete_after=300.0)
                DropdownMessageToSend = ""
                await view.wait() #wait for a valid challenge claim
                if view.selected_value != None:
                    IsDropdownMessageSilent=False
                    print("Continue with the code post-selection")
                    print(view.selected_value)
                    print(view.claimingPlayer.mention)

                    x = players.copy() #temp copy of players list to find the one who *wasn't* claiming
                    x.remove(view.claimingPlayer)
                    nonClaimingPlayer = x[0]
                    
                    DropdownMessageToSend += ("Hey "+nonClaimingPlayer.mention+","+view.claimingPlayer.mention+" just claimed **"+view.selected_value+".**\nYou're out of luck if you were going for it, because now you're Locked Out!")
                    
                    challengesAvailable.remove(view.selected_value) #remove completed challenge from list
                    challengesCompleted[view.claimingPlayer].append(view.selected_value)
                    
                    scores[view.claimingPlayer] = len(challengesCompleted[view.claimingPlayer])
                    scores[nonClaimingPlayer] = len(challengesCompleted[nonClaimingPlayer])
                    
                    #await asyncio.sleep(1) #prevent rate limiting by self rate limiting lol
                else:
                    print("users took too long to answer interaction. generating new dropdown message.")
                    IsDropdownMessageSilent=True
            
            print("racing users removed from list of users in play")
            usersInChallenges.remove(ctx.author) #at the end of the game, remove both players from the "in a game" list so they can play again.
            usersInChallenges.remove(membertochallenge)
            if(scores[ctx.author]>=challengestowin):
                winner = ctx.author
            else: #since there's only 2 ppl, no need for elif
                winner = membertochallenge
            gameEndButtonView = ViewAllChallenges(players, scores, challengesCompleted, challengesAvailable) #add a button to send an ephemeral message of which challenges were claimed by whom
            await ctx.send("GAME OVER\nEnd Score: **"+ctx.author.mention+" "+str(scores[ctx.author])+" : "+str(scores[membertochallenge])+" "+membertochallenge.mention+"**\n**"+winner.display_name+"** is the winner!", view=gameEndButtonView)
            print("a race ended")
            
            
        else:
            print('Cancelled...') #if challenge denied
            await ctx.send(membertochallenge.mention +" has denied the challenge. Sorry, "+ctx.author.mention+".")
            usersInChallenges.remove(ctx.author)
            usersInChallenges.remove(membertochallenge)
        
@LockoutRace.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('you forgot to ping a person to challenge. Write it after the command name.', delete_after = 15.0)


bot.run(BOT_TOKEN)