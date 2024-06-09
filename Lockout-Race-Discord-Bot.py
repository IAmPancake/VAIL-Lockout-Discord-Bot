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

#first we set up all the stuff relating to generating challenges because I mostly already know what I'm doing here
guns = ["MK418", "AK12", "AK303N", "GrotB", "MR96", "UMP45", "Vector45", "Vityaz", "APC9Pro", "G17", "MK23", "PL14","PM9", "Desert Eagle", "G28Z", "ScarH", "Kanto"]
categories = ["Rifle", "DMR", "Sidearm", "SMG", "Grenade"]
sights = [] #implement later maybe? too many to list and no concrete list
maps = ["Cliffside", "Este", "Khidi", "Maar", "Miru", "Volt", "Nine", "Suna", "The Void", "Atmos"]
modes = ["CTO", "Artifact", "TDM", "FFA", "Gun Game", "Hardpoint", "SKZ", "One in the Chamber"]

#if anyone out there has a good list of all the sights in the game please tell me so I can use it to make challenges thanks

#why is this not a default function/method
def listCombiner(list1, list2):
    endlist = list1
    endlist.extend(list2)
    return endlist

#.splitlines at the end turns this into a nice list. one challenge per line
#this list is only for challenges that have no arguments/random parts (i.e. get x kills in one life), where we want to randomize x
#those will be in a separate list  which will be appended to this one
noRngChallenges = """Get a kill with 3 different primary weapons in one life
Kill your Lockout opponent with a headshot
Kill your Lockout opponent twice in one life
Kill while holding the objective IN YOUR HAND (scanner, orb)
Kill an enemy while both you can them are on the hardpoint 
Kill an enemy using the same weapon as them 5 times (No SKZ)
Get a kill while YOU are flashed
Get 2+ kills with one grenade 3 times
Get 2+ kills with one BULLET (MR96 recommended)
Kill through map geometry
Be alive while 5 enemy players are dead (no ART)
Kill while you are airborne
360 spin kill
Get a kill with 5 different weapons with zoom scopes (no MRO or SpitfireAR)
Get 2 kills with each weapon in your loadout in one life
Defuse or plant the Artifact Scanner while the entire enemy team is dead
Get a knife kill on someone you can't see
Get 5+ kills and 0 deaths in one match (not just a single ART round)""".splitlines()

#this list is for challenges that take arguments so that they can vary between games without having to list each possibility
#i had to make it a function otherwise it'd just randomize once when you run the script and then stay the same between races. Fun.
def generateRngChallenges():
    listr = [
        "Win a game of " + random.choice(modes), 
        "Get "+str(random.randint(5, 12))+" frag nade kills", 
        "Get "+str(random.randint(3, 12))+" impact frag kills",  
        "Get "+str(random.randint(7, 25))+" kills with " + random.choice(categories)+"s", 
        "Get "+str(random.randint(5, 15))+" knife kills", #not so much a fan of this one since it can already occur as random from another challenge
        "Get "+str(random.randint(8, 25))+" kills with a "+random.choice(guns), 
        "Get "+str(random.randint(3, 9))+" kills with a "+random.choice(guns)+" in one life", 
        "Get a kill with every "+ random.choice(categories), 
        "Get "+str(random.randint(2, 10))+" kills through smoke", 
        "Get "+str(random.randint(2, 6))+" headshot kills in one life",
        "Get "+str(random.randint(2, 4))+" kills back-to-back "+str(random.randint(2, 4))+" times",
        "Get "+str(random.randint(5, 12))+" kills using your non-dominant hand",
        "Get "+str(random.randint(5, 12))+" headshot kills using iron sights",
        "Get "+str(random.randint(5, 12))+" kills with a SCARH on full auto"
    ]
    return listr

#use these two lines instead of one for actually rerandomizing the full list to pick from. Why does it only work this way? I don't know and probably never will
#and i tried making it reference a dictionary for the rng methods which in theory should make it rerandomize every time an item gets pulled from the list, but it didn't work
RngChallenges = generateRngChallenges()
allChallenges = listCombiner(RngChallenges, noRngChallenges)
#print("\n".join(allChallenges))
#print("\n")

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
    try:
        synced = await bot.tree.sync(guild=None)
        print("command tree synced: " +str(len(synced)))
    except Exception as e:
        print("command tree failed to sync: \n"+str(e))

@bot.hybrid_command(name="generatechallenges", help="generates a user-set number of VAIL Lockout challenges. does not start a VAIL Lockout race.")
async def getSomeChallenges(ctx, numchallenges: int):
    RngChallenges = generateRngChallenges()
    allChallenges = listCombiner(RngChallenges, noRngChallenges) #generate all challenges
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
    def __init__(self, targetUser, ctx):
        super().__init__()
        self.value = None
        self.targetUser = targetUser
        self.ctx = ctx
        
    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    @discord.ui.button(label='Accept Challenge', style=discord.ButtonStyle.green)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if (interaction.user == self.targetUser):#only the person being challenged can accept
            self.value = True
            self.stop()
        else:
            await self.ctx.send("that challenge wasn't for you, "+interaction.user.mention+"!", delete_after=3.0)
            
        

    # This one is similar to the confirmation button except sets the inner value to `False`
    @discord.ui.button(label='Deny Challenge', style=discord.ButtonStyle.grey)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)
        if (interaction.user == self.targetUser): #only the person being challenged can deny
            self.value = False
            self.stop()
        else:
            await self.ctx.send("that challenge wasn't for you, "+interaction.user.mention+"!", delete_after=3.0)

class DropdownView(discord.ui.View):
    def __init__(self, challengesToList, playersInGame, ctx):
        super().__init__()
        self.challengesToList = challengesToList
        self.ctx = ctx
        self.playersInGame = playersInGame
        
        self.selected_value = None #challenge claimed by user
        self.claimingPlayer = None #player making the claim
        # Adds the dropdown to our view object.
        self.add_item(Dropdown(self.challengesToList, self.playersInGame, self.ctx)) #i wish I didn't need to use separate classes here, but it didn't work if i tried to make it one class for some reason
                                                                                     #I tried all the methods

class Dropdown(discord.ui.Select):
    def __init__(self, bChallengesToList, players, ctx): #the "b" in "bChallengesToList" is just to differentiate from challengesToList in DropdownView
        self.bChallengesToList = bChallengesToList
        self.players = players
        self.ctx = ctx
        # Set the options that will be presented inside the dropdown
        options = []
        #print(" ".join(self.bChallengesToList)) #debugging
        for i in self.bChallengesToList:
            options.append(discord.SelectOption(label=i, value=i))
        print("challenges have been generated for dropdown")
        
        # The placeholder is what will be shown when no option is chosen
        # The min and max values indicate we can only pick one of the three options
        # The options parameter defines the dropdown options. We defined this above
        super().__init__(placeholder="Choose a challenge once you've completed it", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        # Use the interaction object to send a response message containing
        # the user's choice. The self object refers to the select obj and blah blah blah idc abt text from template
        await interaction.response.defer()
        if (interaction.user in self.players):#only people in this race can claim
            print("a challenge has been claimed")
            self.view.claimingPlayer = interaction.user
            self.view.selected_value = self.values[0]
            #await self.ctx.send("challenge **"+self.view.selected_value+"** has been claimed by "+interaction.user.mention)
            self.view.stop()
        else:
            await self.ctx.send("You aren't part of this race, "+interaction.user.mention+"!", delete_after=3.0)
        

@bot.hybrid_command(name="lockoutrace", help="Challenge another user to a VAIL Lockout Race. Default to first to 13." )
async def LockoutRace(ctx, membertochallenge:discord.Member,challengestowin:typing.Optional[int] = 13,challengegeneratetimer:typing.Optional[int]=120):
    print("lockout race cmd sent")
    
    global usersInChallenges
    numChallenges = (challengestowin*2)-1
    RngChallenges = generateRngChallenges()
    allChallenges = listCombiner(RngChallenges, noRngChallenges) #generate all challenges

    if membertochallenge == ctx.author:
        await ctx.send("You can't challenge yourself to a race! try using !generateChallenges if you want to get some challenges to do by yourself.")
    elif membertochallenge in usersInChallenges:
        await ctx.send("that person has either already been challenged, or is currently participating in a Lockout Race. Try again later, or with someone else.") #prevent people from being challenged multiple times
    elif ctx.author in usersInChallenges:
        await ctx.send("you cannot issue a challenge when you have already been challenged! Either deny the incoming challenge or finish your race, whichever is applicable") #prevent people from challenging multiple others at once
    elif (numChallenges > 25): 
        await ctx.send("You requested more challenges than can be generated. The maximum is first to 13 (total 25).") #prevent users from generating more unique challenges than there are unique challenges possible to be generated
    elif (numChallenges < 1):
        await ctx.send("Cannot generate less than 1 challenge") #obvious
    
    else:
        print("lockout race input legit")
        challengeMsg = (ctx.author.mention +" has challenged "+membertochallenge.mention+" to a VAIL Lockout Race!\nfirst to "+str(challengestowin)+" challenges complete wins!\nPress the 'Accept Challenge' button once ready, or press 'Deny Challenge' to deny. Expires in about 3 minutes.")
        usersInChallenges.append(ctx.author)
        usersInChallenges.append(membertochallenge)
        view = Confirm(membertochallenge, ctx)
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
                #async with channel.typing():
                print("waiting for challenge timer")
                await asyncio.sleep(challengegeneratetimer)
            await ctx.send(ctx.author.mention+" and "+membertochallenge.mention+", here are your challenges!\nFirst to complete **"+str(challengestowin)+"** of them wins!\n"+("\n".join(challengesPerGame)))
            print("game start")

            while((scores[ctx.author]<challengestowin)and(scores[membertochallenge]<challengestowin)):
                view = DropdownView(challengesAvailable, players, ctx)
                await ctx.send("The score is **"+str(ctx.author.mention+" "+str(scores[ctx.author])+" : "+str(scores[membertochallenge])+" "+membertochallenge.mention+"**\nFirst to "+str(challengestowin)+" challenges complete wins!\nChoose a challenge to claim (note: claims as soon as you click!"), view=view, delete_after=180.0, silent=True)
                await view.wait() 
                if view.selected_value != None:
                    print("Continue with the code post-selection")
                    print(view.selected_value)
                    print(view.claimingPlayer.mention)
                    x = players.copy() #temp copy of players list to find the one who *wasn't* claiming
                    x.remove(view.claimingPlayer)
                    nonClaimingPlayer = x[0]
                    await ctx.send("Hey "+nonClaimingPlayer.mention+","+view.claimingPlayer.mention+" just claimed **"+view.selected_value+".**\nYou're out of luck if you were going for it, because now you're Locked Out!", delete_after=3600.0)
                    challengesAvailable.remove(view.selected_value)
                    challengesCompleted[view.claimingPlayer].append(view.selected_value)
                    scores[view.claimingPlayer] = len(challengesCompleted[view.claimingPlayer])
                    scores[nonClaimingPlayer] = len(challengesCompleted[nonClaimingPlayer])
                    await asyncio.sleep(1)
                else:
                    print("users took too long to answer interaction. generating new dropdown message.")
            print("racing users removed from list of users in play")
            usersInChallenges.remove(ctx.author) #at the end of the game, remove both players from the "in a game" list so they can play again.
            usersInChallenges.remove(membertochallenge)
            if(scores[ctx.author]>=challengestowin):
                winner = ctx.author
            else:
                winner = membertochallenge
            await ctx.send("GAME OVER\nEnd Score: **"+ctx.author.mention+" "+str(scores[ctx.author])+" : "+str(scores[membertochallenge])+" "+membertochallenge.mention+"**\n**"+winner.display_name+"** is the winner!")
            
            #uncomment the below line if you want the bot to print out a list of who did what challenges after the game ends. NOT TESTED. LIKELY WILL SEND A LARGE MESSAGE
            #await ctx.send("**Challenges completed by "+ctx.author.display_name+": "+str(scores[ctx.author])+"**\n"+"\n".join(challengesCompleted[ctx.author])+"\n \n**Challenges completed by "+membertochallenge.display_name+": "+str(scores[membertochallenge])+"**\n"+"\n".join(challengesCompleted[membertochallenge]))
            
        else:
            print('Cancelled...')
            await ctx.send(membertochallenge.mention +" has denied the challenge. Sorry, "+ctx.author.mention+".")
            usersInChallenges.remove(ctx.author)
            usersInChallenges.remove(membertochallenge)
        
@LockoutRace.error
async def info_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('you forgot to ping a person to challenge. Write it after the command name, before the "challenges to win" number, if you used one.')

bot.run(BOT_TOKEN)