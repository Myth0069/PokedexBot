import json


pokemonNames = open('pokemonALPH.txt', 'r')
pokemonNumbers = open('pokemonByNumber.txt', 'r')
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
   
    name = {
        "name": tempname,
        "bulbapedia": BurlB + tempname + BurlE,
        "smogon": SurlB + tempname + SurlE,
        "smogon4": S4urlB + tempname +S4urlE,
	"pixelmon": PixurlB + tempname
        }
    pokemon[tempname] = name
pokemonNames.close()

for entry in pokemonNumbers:
    entryLine = str(entry.strip())
    digitcount = 0
    gen = 8
    no = 0
    write = False
    number = ''
    candidate = ''
    for character in entryLine:
        if character == '#':
            write = True
        if (write == True) and (digitcount < 4):
           number += character
           digitcount += 1                
        elif write == True:
            candidate = candidate + character
    candidate = candidate.strip()
    candidate = candidate.lower()
    number = number[1:]
    no = int(number)
 
    if no < 152:
        gen = 1
    elif no < 252:
        gen = 2
    elif no < 387:
        gen =3
    elif no < 494:
        gen = 4
    elif no < 650:
        gen = 5
    elif no < 722:
        gen = 6
    elif no < 810:
        gen = 7
    elif no == 0:
        gen = 8

    try:
        dict = pokemon[candidate]
        dict["no"] = no
        dict["gen"] = gen
    except:
        pass

pokemonNumbers.close()

json_object = json.dumps(pokemon, indent = 4)
f = open("pokemonALPH.json", "w")
f.write(json_object)
f.close


#with open("pokemonALPH.json", "w") as outfile:
#    json.dump(pokemon, outfile)

    