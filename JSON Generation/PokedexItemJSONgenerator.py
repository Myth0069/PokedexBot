import json

itemNames = open('itemListRaw.txt', 'r')
line = 0

urlB = r'https://pixelmonmod.com/wiki/'

count = 0
item = {}
name = ''
for line in itemNames:
    row = str(line.strip())
    for element in row:
        if element == ',':
            count += 1
        if element != ',' and count == 2:
            name += element
            
            
                
    name = name.title()
    tempname = name
    tempname  = tempname.replace(' ', '_')
    count = 0


    entry = {
	    "pixelmon item url": urlB + tempname
        }
    item[name] = entry
    name = ''
itemNames.close()

json_object = json.dumps(item, indent = 4)
f = open("itemALPH.json", "w")
f.write(json_object)
f.close


#with open("pokemonALPH.json", "w") as outfile:
#    json.dump(pokemon, outfile)
