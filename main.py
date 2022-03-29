import discord
import json
from discord.ext import commands
from discord.ext.commands import Bot
from discord.utils import get
import asyncio
import io
import aiohttp

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

bot.run('token')
