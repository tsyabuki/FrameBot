import random
import discord
from discord.ext import commands
from characterdict import ufdPage
from eightball import eightballResponse

with open('token.dat') as TokenFile:
    TOKEN = TokenFile.read()

prefix = "%"

bot = commands.Bot(command_prefix=prefix)
client = discord.Client()



@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))



async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send(':RyujiThumbsUp: Welcome {0.mention}! :RyujiThumbsUp:'.format(member))



@bot.listen() # Random response message every once in a while
async def on_message(message):
    if message.author == bot.user or message.content.startswith(prefix):
        return

    random.seed() # Generates new seed
    randNum = random.random()*100 # Randomizes
    responseOdds = 1 # Percentage chance that the bot will respond

    if randNum < responseOdds: # Checks if the bot should respond
        randNum = random.random()*100 # Generates new random number 
        if randNum < 30:
            await message.channel.send('Hmmm...') 
        elif randNum < 60:
            await message.channel.send('Absolutely right')
        elif randNum < 80:
            await message.channel.send('FrameBot has analyzed the frame data, and has determined you\'re stupid')
        elif randNum < 95:
            await message.channel.send(':sink_noodles:')
        elif randNum < 99:
            await message.channel.send('Jair')
        else: # If anyone who isn't from cstat reads this one, this one is a copypasta from the discord server this bot was for
            await message.channel.send('I fucking hate Cheeky from cstat. That little shit waltzes into the MSC acting like she owns the place, rigging brackets on cstat.challonge.com and acting like she doesn’t know the same people fight every week. Brick, being the good TO that he is, naturally doesn\'t want Cheeky running his bracket, showing his loyalty to cstat smash. But this stupid e-girl is absolutely determined to be a pest and completely take over the scene. Cheeky’s devices for messing with our hero Brick can only be described as the work of a criminal mastermind. She utilizes the bracket at his disposal in the MSC, causing great drops in ELO rankings just so she can watch and laugh at Brick. She even bribes the rest of the scene to carry out her sick little game. What\'s worse, at the end of each bracket, she usually wins! What a god damn asshole.')
        return

    randNum = random.random()*100 # If he doesn't respond with anything else, 1% of the time, FrameBot will post a hydration reminder
    
    if randNum < 1:
        await message.channel.send(':cup_with_straw: Remember to stay hydrated! :cup_with_straw:')

        



@bot.command()
async def ping(ctx):
    '''
    Use this command to get the latency of the bot!
    '''
    latency = bot.latency*1000
    await ctx.send(':ping_pong: Pong! - Sent in {0:.4}ms :ping_pong:'.format(latency))

@bot.command()
async def echo(ctx, *, content:str):
    '''
    Returns the content of the message back to the sender!
    '''
    await ctx.send(content)

@bot.command()
async def eightball(ctx, *, content:str):
    '''
    Gives a response to an eightball question given
    '''
    random.seed()
    randNum = random.randrange(len(eightballResponse))
    await ctx.send(eightballResponse[randNum])

@bot.command()
async def coinflip(ctx):
    '''
    Gives either heads or tails!
    '''
    random.seed()
    randNum = random.randrange(2)
    if randNum == 0:
        await ctx.send('Heads!')
    else:
        await ctx.send('Tails!')



@bot.command()
async def ufd(ctx, *, content:str):
    '''
    Finds the Ultimate Frame Data page of the character!
    '''
    content = content.lower()
    if content in ufdPage:
        await ctx.send(ufdPage[content])
    else:
        await ctx.send('UFD page not found')

@bot.command()
async def event(ctx, id):
    '''
    Under construction! The bot will find the resulfs of a tournament, given the smashgg ID.
    '''
    await ctx.send('This command is currently under construction! Try again later.')

@bot.command()
async def rage(ctx, percentIn):
    '''
    Calculates rage at a given %!
    '''
    percent = float(percentIn)
    rage = 0.0
    if percent <= 35:
        rage = 1.0
    elif percent >= 150:
        rage = 1.1
    else:
        rage = 1 + (percent-35) * (.1/115)
    await ctx.send('The rage multiplier at **{0}%** is **{1:.3}x**'.format(percent, rage))
    

bot.run(TOKEN)