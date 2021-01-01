import json


pokemonNames = open('pokemonALPH.txt', 'r')
line = 0

BurlB = r'https://bulbapedia.bulbagarden.net/wiki/'
BurlE = '_(Pok%C3%A9mon)'

SurlB = r'https://www.smogon.com/dex/sm/pokemon/'
SurlE = '/'

S4urlB = r'https://www.smogon.com/dex/dp/pokemon/'
S4urlE = '/'

PixurlB = r'https://pixelmonmod.com/wiki/'


count = 0
pokemon = {}

for line in pokemonNames:
    count += 1
    name = str(line.strip())
    tempname = name
    score = wordScore(tempname)
    name = {
        "name": tempname,
        "bulbapedia": BurlB + tempname + BurlE,
        "smogon": SurlB + tempname + SurlE,
        "smogon4": S4urlB + tempname +S4urlE,
	"pixelmon": PixurlB + tempname
        }
    pokemon[tempname] = name
pokemonNames.close()

json_object = json.dumps(pokemon, indent = 4)
f = open("pokemonALPH.json", "w")
f.write(json_object)
f.close


#with open("pokemonALPH.json", "w") as outfile:
#    json.dump(pokemon, outfile)

    