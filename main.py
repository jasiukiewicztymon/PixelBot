import discord
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import io
import aiohttp
import requests
import base64
import json
import datetime 

APIKEY = "key"

def GetUserInfo(name):
    r = requests.get(f"https://api.hypixel.net/player?key={APIKEY}&name={name}")
    return r.json()

bot = commands.Bot(command_prefix='.')

bedwars = [0]
skywars = [0]

@bot.command()
async def play(ctx, *args):
    guild = ctx.message.guild
    for server in bot.guilds:
            for category_id in server.categories:
                if (category_id.id == 958045311853531136):
                    if args[0] == 'bedwars':
                        vname = args[0] + " #" + str(len(bedwars))
                        tname = args[0] + str(len(bedwars))
                        await guild.create_voice_channel(vname, category=category_id)
                        await guild.create_text_channel(tname, category=category_id)
                        for channel in server.channels:
                            if channel.name == tname and len(args) >= 2:
                                wchannel = bot.get_channel(channel.id)
                                await wchannel.send('We play on {} @here'.format(args[1]))

                        bedwars.append(len(bedwars))

                        await ctx.reply('You have open: ' + vname)
                    elif args[0] == 'skywars':
                        vname = args[0] + " #" + str(len(bedwars))
                        tname = args[0] + str(len(bedwars))
                        await guild.create_voice_channel(vname, category=category_id)
                        await guild.create_text_channel(tname, category=category_id)

                        skywars.append(len(skywars))

                        await ctx.reply('You have open: ' + vname)
                    else:
                        await ctx.reply('Invalid game type')
                    break

@bot.command()
async def close(ctx, *args):
    guild = ctx.message.guild

    if args[0] == 'bedwars':
        vname = args[0] + " #" + args[1]
        tname = args[0] + args[1]
        tchannel = discord.utils.get(guild.channels, name=tname)
        vchannel = discord.utils.get(guild.channels, name=vname)

        if vchannel is not None:
            await vchannel.delete()
            bedwars.pop()

        if tchannel is not None:
            await tchannel.delete()
    
        await ctx.reply('You have closed: ' + vname)
    elif args[0] == 'skywars':
        vname = args[0] + " #" + args[1]
        tname = args[0] + args[1]
        tchannel = discord.utils.get(guild.channels, name=tname)
        vchannel = discord.utils.get(guild.channels, name=vname)

        if vchannel is not None:
            await vchannel.delete()
            skywars.pop()

        if tchannel is not None:
            await tchannel.delete()
    
        await ctx.reply('You have closed: ' + vname)
    else:
        await ctx.reply('Invalid game type') 

@bot.command()
async def stats(ctx, *args):
    if args[0] == 'user':
        if args[1] == 'level':
            async with aiohttp.ClientSession() as session:
                async with session.get('https://gen.plancke.io/exp/{}.png'.format(args[2])) as resp:
                    if resp.status != 200:
                        return await ctx.reply('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.send(file=discord.File(data, '{}.png'.format(args[2])))
        elif args[1] == 'point':
                async with aiohttp.ClientSession() as session:
                    async with session.get('https://gen.plancke.io/achievementPoints/{}.png'.format(args[2])) as resp:
                        if resp.status != 200:
                            return await ctx.reply('Could not download file...')
                        data = io.BytesIO(await resp.read())
                        await ctx.send(file=discord.File(data, '{}.png'.format(args[2])))

@bot.command()
async def bans(ctx, *args):
    r = requests.get(f"https://api.hypixel.net/watchdogstats?key={APIKEY}")
    r = r.json()
    embed = discord.Embed(title="Hypixel's bans", description="Here are the ban stats on Hypixel", colour=0x850F07)
    embed.add_field(name="Total", value=r['staff_total'], inline=True)
    embed.add_field(name="Today", value=r['staff_rollingDaily'], inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def friends(ctx, *args):
    name = args[0]
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    uuid = uuid.json()
    useruuid = uuid['id']

    r = requests.get(f"https://api.hypixel.net/friends?key={APIKEY}&uuid={useruuid}")
    r = r.json()

    embed = discord.Embed(title=f"{name}'s Friends", description=f"Here are all the {name} friends", colour=0x850F07)
    for friend in r['records']:
        sender = friend['uuidSender']
        reciver = friend['uuidReceiver']

        if sender == useruuid:
            f = requests.get(f"https://api.hypixel.net/player?key={APIKEY}&uuid={reciver}")
            f = f.json()
            
            try:
                embed.add_field(name=f"{f['player']['displayname']}", value=f"Rank: {f['player']['packageRank']}", inline=True)
            except:
                embed.add_field(name=f"{f['player']['displayname']}", value=f"Rank: None", inline=True)
        else:
            f = requests.get(f"https://api.hypixel.net/player?key={APIKEY}&uuid={sender}")
            f = f.json()

            try:
                embed.add_field(name=f"{f['player']['displayname']}", value=f"Rank: {f['player']['packageRank']}", inline=True)
            except:
                embed.add_field(name=f"{f['player']['displayname']}", value=f"Rank: None", inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def status(ctx, *args):
    name = args[0]
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    uuid = uuid.json()
    useruuid = uuid['id']

    r = requests.get(f"https://api.hypixel.net/status?key={APIKEY}&uuid={useruuid}")
    r = r.json()

    if r['session']['online'] == True:
        try:
            mode = r['session']['mode'].lower()
            gameType = r['session']['gameType'].lower()
            mapName = r['session']['map'].lower()
            await ctx.reply(f"{name} plays {gameType} on the {mapName} map 🟢")
        except:
            mode = r['session']['mode'].lower()
            gameType = r['session']['gameType'].lower()
            await ctx.reply(f"{name} plays {mode} in {gameType} 🟢")
    else:
        await ctx.reply(f"{name} is offline 🔴")

@bot.command()
async def recentgames(ctx, *args):  
    name = args[0]
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    uuid = uuid.json()
    useruuid = uuid['id']

    r = requests.get(f"https://api.hypixel.net/recentgames?key={APIKEY}&uuid={useruuid}")
    r = r.json()

    embed = discord.Embed(title=f"{name}'s recent games", description=f"Here are {args[1]} game list of {name}", colour=0x850F07)
    for i in range(int(args[1])):
        timestamp = datetime.datetime.fromtimestamp(r['games'][i]['date'] / 1e3)
        date = timestamp.strftime("%d/%m/%Y")
        hour = timestamp.strftime("%H:%M")

        embed.add_field(name=f"{r['games'][i]['mode']}", value=f"Played {date} at {hour} on {r['games'][i]['map']}", inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def namehistory(ctx, *args): 
    name = args[0]
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    uuid = uuid.json()
    useruuid = uuid['id']

    r = requests.get(f"https://api.mojang.com/user/profile/{useruuid}/names")
    r = r.json()

    embed = discord.Embed(title=f"{name} names history", description=f"Current pseudo is {name}", colour=0x850F07)
    for i in range(len(r)):
        if i != 0:
            timestamp = datetime.datetime.fromtimestamp(r[i]['changedToAt'] / 1e3)
            date = timestamp.strftime("%d/%m/%Y")
            hour = timestamp.strftime("%H:%M")
            
            embed.add_field(name=r[i]['name'], value=f"{date} {hour}", inline=True)

    await ctx.send(embed=embed)

@bot.command()
async def skin(ctx, *args): 
    name = args[0]
    uuid = requests.get(f"https://api.mojang.com/users/profiles/minecraft/{name}")
    uuid = uuid.json()
    useruuid = uuid['id']

    r = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{useruuid}")
    r = r.json()

    key = r['properties'][0]['value']
    bkey = base64.b64decode(key)
    dkey = bkey.decode('ascii')

    dkey = json.loads(dkey)

    async with aiohttp.ClientSession() as session:
        async with session.get(dkey['textures']['SKIN']['url']) as resp:
            if resp.status != 200:
                return await ctx.reply('Could not download file...')
            data = io.BytesIO(await resp.read())
            await ctx.send(file=discord.File(data, '{}.png'.format(args[0])))

@bot.command()
async def serverstatus(ctx, *args): 
    ip = args[0]
    r = requests.get(f"https://api.mcsrvstat.us/2/{ip}")
    r = r.json()

    status = r['online'] 
    if status:
        status = 'online 🟢'
    else:
        status = 'offline 🔴'

    embed = discord.Embed(title=f"{ip}'s server status", description=f"The server is {status}", colour=0x850F07)

    if status == 'online 🟢':
        embed.add_field(name='Max players', value=f"{r['players']['max']}", inline=True)
        embed.add_field(name='Online players', value=f"{r['players']['online']}", inline=False)
        embed.add_field(name='Versions', value=f"{r['version']}", inline=True)
        embed.add_field(name='Ip', value=f"{r['hostname']}", inline=True)
    else:
        embed.add_field(name='Ip', value=f"{r['hostname']}", inline=True)

    await ctx.send(embed=embed)

bot.run('token')
