
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



def wordMatch(inputText, list):
    score = sc.wordScore(inputText)
    min = 9999999 #an extremely high value to intialize min
    for key in list:
        candidate = key
        dict = list[key]
        sim = np.dot(score - dict['wordScore'], score - dict['wordScore'])
        if sim < min:
            answer = candidate
            min = sim
    return str(answer)
        
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
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def pokemon(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")
#pokemon aliases
#pok =p = pokemon

@client.command()
async def pixelmon(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["pixelmon"])
    except:
        await ctx.send("Pokemon Not Found!")
#pixelmon aliases
#pix = pixelmon

@client.command()
async def item(ctx, *args):
    try:         
        input =  ""
        for value in args:
            value = value.lower()
            input = input + value + " "
        input = input[:-1]
        input = wordMatch(input.lower(), itemList)
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
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon"])
    except:
        await ctx.send("Pokemon Not Found!")
#smogon aliases
#smogen = smogon

@client.command()
async def smogon4(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
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
    #for arg in args: #FOR DEBUG
    #    await ctx.send('Arg Found: ' + arg) #FOR DEBUG
    #await ctx.send(str(error)) #FOR DEBUG
    #await ctx.send('Spellcheck this: ' + Userin[0]) #FOR DEBUG
    if args[0].lower() in ['p', 'pok']: #Beginning of alias cmd search
        await pokemon(ctx, args[1])
    elif args[0].lower() in ['pix']:
        await pixelmon(ctx, args[1])
    elif args[0].lower() in ['i']:
        await item(ctx, args[1])
    elif args[0].lower() in ['smogen']:
        await smogon(ctx, args[1])
    elif args[0].lower() in ['smogen4']:
        await smogon4(ctx, args[1]) #end of alias cmd search
    else:
        try:

            input = wordMatch(str(args[0]).lower(), commandList)
            dict = commandList[input]
            intendedCmd = dict["name"]
            #await ctx.send(intendedCmd)
            if intendedCmd in ['ping']:  # Beginning of alias cmd search
                await ping(ctx)
            elif intendedCmd in ['pokedex']:  # Beginning of cmd spellcheck search
                await pokedex(ctx, args[1])
            elif intendedCmd in ['pokemon']:
                await pokemon(ctx, args[1])
            elif intendedCmd in ['pixelmon']:
                await pixelmon(ctx, args[1])
            elif intendedCmd in ['item']:
                await item(ctx, str(args[1:]))
            elif intendedCmd in ['smogon']:
                await smogon(ctx, args[1])
            elif intendedCmd in ['smogon4']:
                await smogon4(ctx, args[1])  # end of cmd spellcheck search
        except:
            await ctx.send("Command Not Found!")

client.run(environment["botToken"])
