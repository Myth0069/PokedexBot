
#TODO: condense code by figuring out how to handle command aliases

import discord
from discord.ext import commands
import os
import json
import numpy as np
import SpellCheck as sc
import SpellCheck2 as sc2

with open(r'.\pokemonALPH.json', encoding="utf-8") as json_file:
    pokemonList = json.load(json_file)

with open(r'.\itemALPH.json', encoding="utf-8") as json_file:
    itemList = json.load(json_file)

with open(r'.\environment.json', encoding="utf-8") as json_file:
    environment = json.load(json_file)

with open(r'.\commands.json', encoding="utf-8") as json_file:
    commandList = json.load(json_file)

for key in pokemonList:
    dictP = pokemonList[key]
    dictP['wordScore'] = sc.wordScore(key)
    
for key in itemList:
    dictI = itemList[key]
    dictI['wordScore'] = sc.wordScore(key)

for key in commandList:
    dictC = commandList[key]
    dictC['wordScore'] = sc.wordScore(key)
        
client = commands.Bot(command_prefix = '.')


@client.event
async def on_ready():
    print('Pokedex is online')

@client.command()
async def ping(ctx):
    await ctx.send(f'Pokedex Pong! {round(client.latency * 1000)}ms')

#pokedex commands
@client.command()
async def pokedex(ctx, arg):
    try: 
        input = sc.spellCheck(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")
#pokedex aliases
#dex = pokedex

@client.command()
async def pokemon(ctx, arg):
    try: 
        input = sc.spellCheck(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")
#pokemon aliases
#pok =p = pokemon

@client.command()
async def pixelmonmod(ctx, arg):
    try: 
        input = sc.spellCheck(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["pixelmon"])
    except:
        await ctx.send("Pokemon Not Found!")
#pixelmon aliases
#pix = pixelmon = pixelmonmod

@client.command()
async def item(ctx, *args):
    try:         
        input =  ""
        for value in args:
            value = value.lower()
            input = input + value + " "
        input = input[:-1]
        input = sc.spellCheck(input.lower(), itemList)
        dict = itemList[input]       
        await ctx.send(dict["pixelmon item url"])
    except:
        await ctx.send("Item Not Found!")
#item aliases
#i = item

#Start of Smogon Commands
@client.command()
async def smogon(ctx, arg):
    try: 
        input = sc.spellCheck(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon"])
    except:
        await ctx.send("Pokemon Not Found!")
#smogon aliases
#smogen = smogon

@client.command()
async def smogon4(ctx, arg):
    try: 
        input = sc.spellCheck(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon4"])
    except:
        await ctx.send("Pokemon Not Found!")
#smogon4 aliases
#smogen4 = smogon4

@client.event
async def on_command_error(ctx, error):
    args = ctx.message.content.split() #this creates a list of each word the user typed
    args[0] = args[0][1:] #removes the [.] from the first arg
    try:
        if (len(args) == 1) and str(args[0])[0] in ['.']: #dont read if first two chars are ..
            pass
        elif args[0].lower() in ['p', 'pok']: #Beginning of alias cmd search
            await pokemon(ctx, args[1])
        elif args[0].lower() in ['dex']:  # Beginning of alias cmd search
            await pokedex(ctx, args[1])
        elif args[0].lower() in ['pix', 'pixelmon']:
            await pixelmonmod(ctx, args[1])
        elif args[0].lower() in ['i']:
            itemArg = ""
            for arg in args[1:]:
                itemArg = itemArg + str(arg)
            await item(ctx, itemArg)
        elif args[0].lower() in ['smogen']:
            await smogon(ctx, args[1])
        elif args[0].lower() in ['smogen4']:
            await smogon4(ctx, args[1]) #end of alias cmd search

        else:
            input = sc.spellCheck(str(args[0]).lower(), commandList)
            dict = commandList[input]
            intendedCmd = dict["name"]
            #await ctx.send(intendedCmd)
            if intendedCmd in ['ping']:  # Beginning of alias cmd search
                await ping(ctx)
            elif len(args) == 1:
                pass
            elif intendedCmd in ['pokedex']:  # Beginning of cmd spellcheck search
                await pokedex(ctx, args[1])
            elif intendedCmd in ['pokemon']:
                await pokemon(ctx, args[1])
            elif intendedCmd in ['pixelmon']:
                await pixelmonmod(ctx, args[1])
            elif intendedCmd in ['item']:
                itemArg = ""
                for arg in args[1:]:
                    itemArg = itemArg + str(arg)
                await item(ctx, itemArg)
            elif intendedCmd in ['smogon']:
                await smogon(ctx, args[1])
            elif intendedCmd in ['smogon4']:
                await smogon4(ctx, args[1])  # end of cmd spellcheck search
    except:
        await ctx.send("Command Not Found!")

client.run(environment["botToken"])
