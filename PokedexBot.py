
#TODO: condense code by figuring out how to handle command aliases

import discord
from discord.ext import commands
import os
import json
import numpy as np
import SpellCheck as sc

with open(r'.\pokemonALPH.json', encoding="utf-8") as json_file:
    pokemonList = json.load(json_file)

with open(r'.\itemALPH.json', encoding="utf-8") as json_file:
    itemList = json.load(json_file)

with open(r'.\environment.json', encoding="utf-8") as json_file:
    environment = json.load(json_file)

for key in pokemonList:
    dict = pokemonList[key]
    dict['wordScore'] = sc.wordScore(key)
    
for key in itemList:
    dict = itemList[key]
    dict['wordScore'] = sc.wordScore(key)

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

@client.command()
async def pok(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def p(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["bulbapedia"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def pixelmon(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["pixelmon"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def pix(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["pixelmon"])
    except:
        await ctx.send("Pokemon Not Found!")

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

@client.command()
async def i(ctx, *args):
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

#Start of Smogon Commands
@client.command()
async def smogon(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def smogen(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def smogon4(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon4"])
    except:
        await ctx.send("Pokemon Not Found!")

@client.command()
async def smogen4(ctx, arg):
    try: 
        input = wordMatch(str(arg).lower(), pokemonList)
        dict = pokemonList[input]
        await ctx.send(dict["smogon4"])
    except:
        await ctx.send("Pokemon Not Found!")
#End of Smogon Commands

client.run(environment["botToken"])
