# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

#expose bot
# Create a Discord client instance and set the command prefix
intents = discord.Intents.all()
intents.presences = True
intents.guilds = True
intents.members = True
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents, member_cache_flags=discord.MemberCacheFlags.all(), guild_subscriptions=True)

league_cycle = 0
@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='!list_activites'))
commands_list = []
#set the confirmation message when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name='Minecraft'))



@bot.event
async def on_member_update(before, after):
    print(f'{after.name} updated')

#set the commands for your bot
@bot.command()
async def greet(ctx):
    response = 'Hello, I am your discord bot'
    await ctx.send(response)
commands_list.append('!greet')
@bot.command()
async def commands(ctx):
    response = 'You can use the following commands:\n!greet\n!list_command\n!functions'
    await ctx.send(response)
commands_list.append('!help')
@bot.command()
async def functions(ctx):
    response = 'I am a simple Discord chatbot! I will reply to your command!'
    await ctx.send(response)
commands_list.append('!functions')
@bot.command()
async def list_activities(ctx):
    members = ctx.guild.members
    await ctx.send('Let\'s see what everyone\'s up to:')
    for member in members:
        #print(member)
        #member.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name='lol'))
        #await ctx.send(member.name)
        if member.activity is not None:
            activity_type = str(member.activity.type)
            activity_type = activity_type[13:]
            activity_type = f'{activity_type[0].upper()}{activity_type[1:].lower()}'
            await ctx.send(f'{member.name} is {activity_type} {member.activity.name}')
        else:
            await ctx.send(f'{member.name} is not doing anything')
@bot.command()
async def expose(ctx):
    global league_cycle
    members = ctx.guild.members
    for member in members:
        if member.activity is not None:
            if member.activity.name.lower() == 'league of legends':
                if league_cycle == 0:
                    await ctx.send(f'LMAO {member.mention} hop of league and go take a shower!!')
                    await ctx.send('~embarassing~ :joy:')
                elif league_cycle == 1:
                    await ctx.send(f'LOL {member.mention} plays league!!\n:point_up_2::joy:everyone point and laugh! ')
                elif league_cycle == 2:
                    await ctx.send(f'Even Yuumi mains do more damage than you.')
                elif league_cycle == 3:
                    await ctx.send(f'I didn\'t know \'Inting\' was a legitimate playstyle!')
                league_cycle += 1
                if league_cycle > 3: league_cycle = 0
            elif member.activity.name.lower() == 'minecraft':
                await ctx.send(f"{member.mention} Aren't you a little old to be playing Minecraft??")
            elif member.activity.name.lower() == 'google chrome':
                await ctx.send(f"{member.mention} What you searching for? A life??????? :joy:")
#Retrieve token from the .env file

load_dotenv()
bot.run(os.getenv('BOT_TOKEN'))


