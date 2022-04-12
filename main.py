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
import os
from os.path import exists

APIKEY = "key"

bot = commands.Bot(command_prefix='.', help_command=None)

@bot.command()
async def party(ctx, *args): 
    NAME = '{}.config.json'.format(ctx.message.guild.id)
    if args[0] == 'setup':
        if args[1] == 'id':
            party = {
                "category": 0,
                "category_id": int(args[2]),
                "gamemode": []    
            }
            with open(NAME, 'w', encoding='utf8') as outfile:
                outdata = json.dumps(party, ensure_ascii=False)
                outfile.write(outdata)
            await ctx.reply('Party created ✅')
        elif args[1] == 'name':
            party = {
                "category": 1,
                "category_name": args[2],
                "gamemode": []    
            }
            with open(NAME, 'w', encoding='utf8') as outfile:
                outdata = json.dumps(party, ensure_ascii=False)
                outfile.write(outdata)
            await ctx.reply('Party created ✅')
        else:
            await ctx.reply('Invalid argument')
    elif args[0] == 'disconnect':
        if args[1] == 'true':
            file = open(NAME)
            serverdata = json.load(file)
            file.close()

            if exists(NAME):
                if serverdata['category'] == 0:
                    for gm in serverdata['gamemode']:
                        for channel in gm: 
                            c = bot.get_channel(channel['id'])
                            await c.delete()
                else:
                    for gm in serverdata['gamemode']:
                        for channel in gm['channels']: 
                            c = bot.get_channel(channel['id'])
                            await c.delete()
                os.remove(NAME)
                await ctx.reply('Party disconnected ✅')

        elif args[1] == 'false':
            if exists(NAME):
                os.remove(NAME)
            await ctx.reply('Party disconnected ✅')
        else:
            await ctx.reply('Invalid argument')
    else:
        if exists(NAME):
            file = open(NAME)
            serverdata = json.load(file)

            if args[0] == 'gamemode':
                if args[1] == 'add': 
                    name = ""
                    for i in range(len(args)):
                        if i != 0:
                            name += args[i] + " "

                    name = name[0:(len(name)-1)]
                    info = {
                        "name": name,
                        "channels": []
                    }

                    isgm = False

                    for g in serverdata['gamemode']:
                        if g['name'] == name:
                            isgm = True

                    if not isgm:
                        serverdata['gamemode'].append(info)
                        with open(NAME, 'w', encoding='utf8') as outfile:
                            outdata = json.dumps(serverdata, ensure_ascii=False)
                            outfile.write(outdata)
                        await ctx.reply(f'{name}\'s category created')
                    else:
                        await ctx.reply(f'The {name} category already exists')
                elif args[1] == 'del':
                    for i in range(len(serverdata['gamemode'])):
                        if serverdata['gamemode'][i]['name'] == args[2]:
                            for ch in serverdata['gamemode'][i]['channels']:
                                channel = discord.utils.get(ctx.guild.channels, id=ch['id'])
                                await channel.delete()
                            del serverdata['gamemode'][i]
                            break
                    await ctx.reply(f"{args[2]} has been remove from gamemodes")
                else:
                    await ctx.reply('Invalide argument')

            elif args[0] == "create":
                await ctx.reply('Invalide argument')
            elif atgs[1] == "delete":
                await ctx.reply('Invalide argument')
            else:
                await ctx.reply('Invalide argument')                 
        else:
            await ctx.reply('Setup the server settings to use this command')

@bot.command()
async def help(ctx, *args):
    embed = discord.Embed(title="Bot's help", description="Here you can find help for the bot using", colour=0x850F07)
    embed.add_field(name="Player's skin", value=".skin [username]", inline=True)
    embed.add_field(name="Server status", value=".serverstatus [server_ip]", inline=True)
    embed.add_field(name="Player's name history", value=".namehistory [username]", inline=True)
    embed.add_field(name="Hypixel user stats command", value=".user <level/point> [username]", inline=True)
    embed.add_field(name="Hypixel ban info", value=".bans", inline=True)
    embed.add_field(name="Hypixel friend list", value=".friends [username]", inline=True)
    embed.add_field(name="Hypixel player activity status", value=".status [username]", inline=True)
    embed.add_field(name="Hypixel player recent games", value=".recentgames [username] [count]", inline=True)
    await ctx.send(embed=embed)

@bot.command()
async def user(ctx, *args):
    if args[0] == 'level':
        async with aiohttp.ClientSession() as session:
            async with session.get('https://gen.plancke.io/exp/{}.png'.format(args[1])) as resp:
                if resp.status != 200:
                    return await ctx.reply('Could not download file...')
                data = io.BytesIO(await resp.read())
                await ctx.send(file=discord.File(data, '{}.png'.format(args[1])))
    elif args[0] == 'point':
            async with aiohttp.ClientSession() as session:
                async with session.get('https://gen.plancke.io/achievementPoints/{}.png'.format(args[1])) as resp:
                    if resp.status != 200:
                        return await ctx.reply('Could not download file...')
                    data = io.BytesIO(await resp.read())
                    await ctx.send(file=discord.File(data, '{}.png'.format(args[1])))

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
        if i == len(r['games']):
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
