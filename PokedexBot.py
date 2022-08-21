# Github Release - wtp functions and non-distributable material removed

import discord
from discord import DMChannel
from discord.ext import commands, tasks
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import json
import CustomSpellCheck as sc
import random
import os
import datetime
import time
import cv2
import numpy as np

root = os.getcwd()

client = commands.Bot(command_prefix='/')
slash = SlashCommand(client, sync_commands=True)

charScores = sc.CharScoresJsonLoader(r'.\json\charScores.json')


with open(r'.\json\pokemonALPH_wtp.json', encoding="utf-8") as json_file:
    pokemonList = json.load(json_file)

with open(r'.\json\itemALPH.json', encoding="utf-8") as json_file:
    itemList = json.load(json_file)

with open(r'.\json\environment.json', encoding="utf-8") as json_file:
    environment = json.load(json_file)

with open(r'.\json\guild_ids.json', encoding="utf-8") as json_file:
    client.guild_id_info = json.load(json_file)

with open(r'.\json\colors.json', encoding="utf-8") as json_file:
    colorList = json.load(json_file)

if os.path.exists(r'.\json\member_info.json'):
    use_existing_member_info = True
    with open(r'.\json\member_info.json', encoding="utf-8") as json_file:
        client.member_info = json.load(json_file)
else:
    use_existing_member_info = False
    client.member_info = {}


def CreateMemberInfo(member_id, member_dictionary):
    if member_id not in member_dictionary:
        member_dictionary[member_id] = {
            "opt-out": False
        }


def MemberIsRegisteredCheck(member_id, member_dictionary):
    if member_id in client.member_info:
        return True
    else:
        CreateMemberInfo(member_id, member_dictionary)
        return False


def MemberOptOut(member_id, member_dictionary):
    member_dictionary[member_id]["opt-out"] = True


def MemberOptIn(member_id, member_dictionary):
    member_dictionary[member_id]["opt-out"] = False


def SaveMemberDataToJson(member_dictionary, json_path=r'.\json\member_info.json'):
    json_object = json.dumps(member_dictionary, indent=4)
    f = open(json_path, 'w')
    f.write(json_object)
    f.close()


def DeleteMemberData(member_id, member_dictionary):
    for key in member_dictionary[member_id]:
        if key != "opt-out":
            del member_dictionary[member_id][key]
    SaveMemberDataToJson(client.member_info)


def MemberOptOutCheck(member_id, member_dictionary):
    if MemberIsRegisteredCheck(member_id, member_dictionary):
        if member_dictionary[member_id]["opt-out"]:
            return True
    else:
        return False


def CelebrationLines(celebration_number):
    lines = [
        'Slow an steady wins the race',
        'This party\'s just getting started!',
        'Cha Cha Cha!',
        'Another victory!',
        'That\'s pretty cool',
        'An achievement worthwhile of a jelly filled donut',
        'Let\'s go!',
        'Wow!',
        'Gloomtastic!'
    ]
    return lines[celebration_number]


def strfdelta(tdelta, fmt):
    d = {"days": tdelta.days}
    d["hours"], rem = divmod(tdelta.seconds, 3600)
    d["minutes"], d["seconds"] = divmod(rem, 60)
    return fmt.format(**d)


guild_ids = []
for guild in client.guild_id_info:
    guild_ids.append(int(guild))

# initialize all the wordScores for the dictionaries:
for key in pokemonList:
    pokemonList[key]['wordScore'] = sc.wordScore(pokemonList[key]["name"], charScores)

for key in itemList:
    itemList[key]['wordScore'] = sc.wordScore(key, charScores)

for key in colorList:
    colorList[key]['wordScore'] = sc.wordScore(key, charScores)

num2name_translator = {}
for key in pokemonList:
    newKey = pokemonList[key]["name"]
    newSubKey = key
    num2name_translator[newKey] = {
        "numKey": key,
        "wordScore": pokemonList[key]["wordScore"].copy()
    }

client.max_wtp_no = 493

client.server_specific_info = {}
for guild_id in guild_ids:
    client.server_specific_info[str(guild_id)] = {
        "channel_ids": {},
        "min_wtp_no": 1,
        "max_wtp_no": 493
    }
client.server_specific_info["vote events"] = {}


@client.event
async def on_ready():
    print('Pokedex is online')


@slash.slash(
    name="ping",
    description="pings PokedexBot"
)
async def ping(ctx: SlashContext):
    if not ctx.author.bot:
        await ctx.send(f'Pokedex Pong! {round(client.latency * 1000)}ms')


# pokedex commands
@slash.slash(
    name="pokedex",
    description="looks up Pokedex entries of Pokemon"
)
async def pokedex(ctx: SlashContext, pokemon):
    if not ctx.author.bot:
        input = sc.spellCheck(str(pokemon), num2name_translator, charScores)
        if input in num2name_translator:
            dict = pokemonList[num2name_translator[input]["numKey"]]
            await ctx.send(dict["bulbapedia"])
        else:
            await ctx.send("Pokemon Not Found!")


@slash.slash(
    name="pixelmon",
    description="looks up Pixelmon website entries of Pokemon"
)
async def pixelmon(ctx: SlashContext, pokemon):
    if not ctx.author.bot:
        input = sc.spellCheck(str(pokemon).lower(), num2name_translator, charScores)
        if input in num2name_translator:
            dict = pokemonList[num2name_translator[input]["numKey"]]
            await ctx.send(dict["pixelmon"])
        else:
            await ctx.send("Pokemon Not Found!")


@slash.slash(
    name="item",
    description="looks up Pixelmon website entries of items"
)
async def item(ctx: SlashContext, item):
    if not ctx.author.bot:
        input = sc.spellCheck(str(item).lower(), itemList, charScores)
        if input in itemList:
            dict = itemList[input]
            await ctx.send(dict["pixelmon item url"])
        else:
            ctx.send("item not found!")



# Start of Smogon Commands
@slash.slash(
    name="smogon",
    description="looks up Smogon website entries of Pokemon"
)
async def smogon(ctx: SlashContext, pokemon):
    if not ctx.author.bot:
        input = sc.spellCheck(str(pokemon).lower(), num2name_translator, charScores)
        if input in num2name_translator:
            dict = pokemonList[num2name_translator[input]["numKey"]]
            await ctx.send(dict["smogon"])
        else:
            await ctx.send("Pokemon Not Found!")


@slash.slash(
    name="smogon4",
    description="looks up Smogon website entries of Pokemon (gen 4, DP)"
)
async def smogon4(ctx: SlashContext, pokemon):
    if not ctx.author.bot:
        input = sc.spellCheck(str(pokemon).lower(), num2name_translator, charScores)
        if input in num2name_translator:
            dict = pokemonList[num2name_translator[input]["numKey"]]
            await ctx.send(dict["smogon4"])
        else:
            await ctx.send("Pokemon Not Found!")


# start of chance commands
@slash.slash(
    name="coin",
    description="tosses a coin, returns Heads/Tails"
)
async def coin(ctx: SlashContext):
    if not ctx.author.bot:
        x = random.randint(0, 1)
        if x > 0:
            with open(".\\chance\\Heads.png", "rb") as png:
                attachment = discord.File(png)
                await ctx.send(file=attachment)
                await ctx.send("Heads!")
        else:
            with open(".\\chance\\Tails.png", "rb") as png:
                attachment = discord.File(png)
                await ctx.send(file=attachment)
                await ctx.send("Tails!")


@slash.slash(
    name="dice",
    description="rolls a 6-sided dice"
)
async def dice(ctx: SlashContext):
    if not ctx.author.bot:
        y = random.randint(1, 6)
        with open(f'.\\chance\\dice{y}.png', "rb") as png:
            attachment = discord.File(png)
            await ctx.send(file=attachment)


@slash.slash(
    name="twoDice",
    description="rolls two 6-sided dice"
)
async def twoDice(ctx: SlashContext):
    if not ctx.author.bot:
        x = random.randint(1, 6)
        y = random.randint(1, 6)
        with open(f'.\\chance\\dice{x}.png', "rb") as png1, open(f'.\\chance\\dice{y}.png', "rb") as png2:
            attachment1 = discord.File(png1)
            attachment2 = discord.File(png2)
            await ctx.send(file=attachment1)
            await ctx.send(file=attachment2)


@slash.slash(
    name="d20",
    description="rolls a 20-sided dice"
)
async def d20(ctx: SlashContext):
    if not ctx.author.bot:
        roll = random.randint(1, 20)
        message = f'You rolled {str(roll)}!'
        await ctx.send(message)


@slash.slash(
    name="card",
    description="draws a card from a 52 card deck"
)
async def card(ctx: SlashContext):
    if not ctx.author.bot:
        suits = ['clubs', 'diamonds', 'hearts', 'spades']
        numbers = ['ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'jack', 'queen', 'king']
        suit = random.randint(0, 3)
        number = random.randint(0, 12)
        with open(f'.\\chance\\PlayingCards\\{numbers[number]}_of_{suits[suit]}.png', "rb") as png:
            attachment = discord.File(png)
            await ctx.send(file=attachment)


@slash.slash(
    name="random_decide",
    description="takes a comma separated list, and returns a random value from it"
)
async def random_decide(ctx: SlashContext, comma_sep_outcomes):
    if not ctx.author.bot:
        outcome_list = str(comma_sep_outcomes).split(',')

        roll = random.randint(0, len(outcome_list) - 1)
        choice = f'{str(outcome_list[roll])}, I choose you!'
        await ctx.send(choice)


@slash.slash(
    name="random_color",
    description="returns a random color with it\'s RGB and hex values"
)
async def random_color(ctx: SlashContext):
    if not ctx.author.bot:
        color_key = random.choice(list(colorList.keys()))
        out_string = f'Name: {colorList[color_key]["color"]}\n' \
                     f'RGB: ({colorList[color_key]["red"]}, {colorList[color_key]["green"]}, {colorList[color_key]["blue"]})\n' \
                     f'hex: {colorList[color_key]["hex"]}'
        await ctx.send(out_string)


@slash.slash(
    name="random_number",
    description="returns a random number between min and max. Also generates a pokemon with that number is applicable"
)
async def random_number(ctx: SlashContext, min, max):
    if not ctx.author.bot:
        if (str(min).isnumeric()) and (str(max).isnumeric()):
            min = int(min)
            max = int(max)
            number = random.randint(min, max)
            await ctx.send(f'{str(number)}')
        else:
            await ctx.send(f'min and/or max values were not integer numeric')


# start of vote commands
@slash.slash(
    name="start_vote",
    description="starts vote with given choices as a comma separated list",
    guild_ids=guild_ids
)
async def start_vote(ctx: SlashContext, vote_event_code, vote_title, vote_choices, duration_up_to_10080_min):
    if not ctx.author.bot:
        choices = str(vote_choices).split(",")
        if str(vote_event_code) in client.server_specific_info["vote events"]:
            await ctx.send("ERROR: vote event code already in use")
        elif not str(duration_up_to_10080_min).isnumeric():
            await ctx.send("ERROR: vote duration requested was not numeric, was negative, or included a decimal")
        elif int(duration_up_to_10080_min) > 10080:
            await ctx.send("ERROR: duration set for longer than 10800 minutes")
        else:
            current_time = datetime.datetime.now()
            client.server_specific_info["vote events"][str(vote_event_code)] = {}
            client.server_specific_info["vote events"][str(vote_event_code)]["title"] = str(vote_title)
            client.server_specific_info["vote events"][str(vote_event_code)]["guild_id"] = ctx.guild_id
            client.server_specific_info["vote events"][str(vote_event_code)]["channel_id"] = ctx.channel_id
            client.server_specific_info["vote events"][str(vote_event_code)]["start time"] = current_time
            client.server_specific_info["vote events"][str(vote_event_code)]["end time"] = \
                current_time + datetime.timedelta(days=int(int(duration_up_to_10080_min) / 1440)
                                                  , minutes=int(duration_up_to_10080_min) % 1440)
            client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"] = {}
            client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"] = {}
            options_string = ''
            for choice in choices:
                choice = str(choice).strip()
                client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"][choice] = {
                    "vote total": 0,
                    "wordScore": sc.wordScore(choice, charScores)
                }
                time_remaining = client.server_specific_info["vote events"][str(vote_event_code)][
                                     "end time"] - current_time
                options_string = options_string + '- ' + choice + '\n'
                time_string = f'Start Time: {client.server_specific_info["vote events"][str(vote_event_code)]["start time"].strftime("%H:%M:%S, %m-%d-%Y")}\n' \
                              f'End Time: {client.server_specific_info["vote events"][str(vote_event_code)]["end time"].strftime("%H:%M:%S, %m-%d-%Y")}\n' \
                              f'Time Remaining: {time_remaining}'

            # store the user ids that have voted and their votes, in case they change their votes later
            client.server_specific_info["vote events"][str(vote_event_code)]["ids_voted"] = {}
            await ctx.send(f'======================\n'
                           f'New vote event created. DM PokedexBot and use /vote to submit your vote!\n\n'
                           f'Title:\n'
                           f'{vote_title}\n\n'
                           f'Vote Options:\n'
                           f'{options_string}\n'
                           f'{time_string}\n'
                           f'Vote Event Code: {str(vote_event_code)}\n'
                           f'======================')
            end_vote_event.start()


@slash.slash(
    name="vote",
    description="DM ONLY: vote in an event using an vote event code and your vote submission"
)
@commands.dm_only()
async def vote(ctx: SlashContext, vote_event_code, vote_choice):
    if not ctx.author.bot:
        if vote_event_code in client.server_specific_info["vote events"]:
            sender_id = ctx.author_id
            input = sc.spellCheck(str(vote_choice).lower(),
                                  client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"],
                                  charScores)
            if sender_id in client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"]:
                if client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"][str(sender_id)][
                    "vote"] != input:
                    # this changes the vote of a user who has already submitted a vote
                    reduce_key = \
                        client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"][str(sender_id)][
                            "vote"]
                    client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"][reduce_key][
                        "vote total"] -= 1
                    client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"][input][
                        "vote total"] += 1
                    await ctx.send(f'Your vote has changed to {input}')
                else:
                    await ctx.send("You can only vote once. You may change your vote by voting for a different outcome")
            else:
                client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"][str(sender_id)] = {}
                client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"][str(sender_id)][
                    "vote"] = input
                client.server_specific_info["vote events"][str(vote_event_code)]["ids voted"][str(sender_id)][
                    "id"] = sender_id
                client.server_specific_info["vote events"][str(vote_event_code)]["outcomes"][input]["vote total"] += 1
                await ctx.send(f'You voted for {input}')
        else:
            await ctx.send(f'{str(vote_event_code)} not found!')


@vote.error
async def vote_command_error(ctx, exception):
    if isinstance(exception, commands.PrivateMessageOnly):
        await ctx.send("/vote is a DM only command")


@slash.slash(
    name="get_vote_info",
    description="returns the current tally of votes and other info for a given vote event"
)
async def get_vote_info(ctx: SlashContext, vote_event_code):
    if not ctx.author.bot:
        if vote_event_code in client.server_specific_info["vote events"]:
            current_time = datetime.datetime.now()
            time_remaining = client.server_specific_info["vote events"][str(vote_event_code)]["end time"] - current_time
            time_string = f'Start Time: {client.server_specific_info["vote events"][str(vote_event_code)]["start time"].strftime("%H:%M:%S, %m-%d-%Y")}\n' \
                          f'End Time: {client.server_specific_info["vote events"][str(vote_event_code)]["end time"].strftime("%H:%M:%S, %m-%d-%Y")}\n' \
                          f'Time Remaining: {time_remaining}'
            time_remaining = client.server_specific_info["vote events"][str(vote_event_code)]["end time"] - current_time
            tally_string = f''
            for choice in client.server_specific_info["vote events"][vote_event_code]["outcomes"]:
                vote_total = client.server_specific_info["vote events"][vote_event_code]["outcomes"][choice][
                    "vote total"]
                tally_string = tally_string + f'- {str(choice)}: {vote_total} votes\n'
            await ctx.send(f'======================\n'
                           f'Title:\n{client.server_specific_info["vote events"][str(vote_event_code)]["title"]}\n\n'
                           f'Vote Options:\n{tally_string}\n'
                           f'Time Remaining: {strfdelta(time_remaining, "{days} days, {hours}:{minutes}:{seconds}")}\n'
                           f'{time_string}\n'
                           f'Vote Event Code: {str(vote_event_code)}\n'
                           f'======================')
        else:
            await ctx.send(f'Vote Event with code {str(vote_event_code)} not found')


@tasks.loop(seconds=5.0)
async def end_vote_event():
    event_count = 0
    for vote_event in client.server_specific_info["vote events"].copy():
        event_count += 1
        end_time = client.server_specific_info["vote events"][vote_event]["end time"]
        current_time = datetime.datetime.now()
        max_votes = 0
        top_outcome = ''
        time_remaining = end_time - current_time
        if time_remaining.total_seconds() < 0:
            tally_string = f''
            for choice in client.server_specific_info["vote events"][vote_event]["outcomes"].copy():
                vote_total = client.server_specific_info["vote events"][vote_event]["outcomes"][choice]["vote total"]
                tally_string = tally_string + f'{str(choice)}: {vote_total} votes\n'
                if client.server_specific_info["vote events"][vote_event]["outcomes"][choice]["vote total"] > max_votes:
                    max_votes = client.server_specific_info["vote events"][vote_event]["outcomes"][choice]["vote total"]
                    top_outcome = choice
                elif client.server_specific_info["vote events"][vote_event]["outcomes"][choice][
                    "vote total"] == max_votes:
                    if top_outcome == '':
                        top_outcome = choice
                    else:
                        top_outcome = top_outcome + ', ' + choice
            leader_string = f'{top_outcome} won the vote with a total of {str(max_votes)} votes!'
            channel = client.get_channel(client.server_specific_info["vote events"][vote_event]["channel_id"])
            end_message = f'======================\n' \
                          f'Vote Results are in for {client.server_specific_info["vote events"][vote_event]["title"]}\n\n' \
                          f'Results:\n' \
                          f'{tally_string}\n' \
                          f'{leader_string}\n' \
                          f'======================'
            await channel.send(end_message)
            for sender_id in client.server_specific_info["vote events"][vote_event]["ids voted"]:
                user = await client.fetch_user(
                    client.server_specific_info["vote events"][vote_event]["ids voted"][sender_id]["id"])
                await DMChannel.send(user, end_message)
                # await user.send("Vote over!")
            del client.server_specific_info["vote events"][vote_event]

        if event_count == 0:
            end_vote_event.stop()


# start of canvas functions
def create_new_canvas(width, height, guild_id):
    canvas_root = '.\\guild_ids\\' + str(guild_id)
    if not os.path.exists(canvas_root):
        os.mkdir(canvas_root)
    client.guild_id_info[str(guild_id)]["server_canvas_path"] = canvas_root
    enlarged_canvas_filepath = os.path.join(canvas_root, f'enlarged_canvas_{str(guild_id)}.png') # show_canvas
    client.guild_id_info[str(guild_id)]["enlarged_canvas_path"] = enlarged_canvas_filepath # show_canvas
    canvas = np.zeros((height, width, 3))
    for i in range(0, height):
        for j in range(0, width):
            canvas[i, j] = (255, 255, 255)
    canvas_filepath = os.path.join(canvas_root, f'canvas_{str(guild_id)}.png')
    client.guild_id_info[str(guild_id)]["server_canvas_path"] = canvas_filepath
    cv2.imwrite(canvas_filepath, canvas)
    #await ctx.send('No server canvas found, generating server canvas')
    return canvas
def edit_canvas(canvas, x, y, width, height, color_rgb):
    x = int(x) - 1
    y = int(y) - 1
    if x > width:
        #await ctx.send(f'Width value out of bound, only integers between 0 and {str(width)} are valid')
        return False
    elif y > height:
        #await ctx.send(f'Height value out of bound, only integers between 0 and {str(height)} are valid')
        return False
    else:
        # converts np y-axis to standard y-axis
        d_from_mid = np.absolute(y-40)
        if y < 40:
            y = 39 + d_from_mid
        elif y > 40:
            y = 39 - d_from_mid

        canvas[y, x] = tuple(color_rgb)
        return canvas


def save_canvas(canvas, path):
    cv2.imwrite(path, canvas, [cv2.IMWRITE_PNG_COMPRESSION, 0])
    json_object = json.dumps(client.guild_id_info, indent=4)
    f = open(r'.\json\guild_ids.json', 'w')
    f.write(json_object)
    f.close()


async def show_canvas_fxn(ctx, g_id):
    if "server_canvas_path" in client.guild_id_info[str(g_id)]:
        if os.path.exists(client.guild_id_info[str(g_id)]["server_canvas_path"]):
            canvas = cv2.imread(client.guild_id_info[str(g_id)]["server_canvas_path"], cv2.IMREAD_UNCHANGED)
            show_size = (480, 320)
            canvas = cv2.resize(canvas, show_size)
            guild_id = str(g_id)
            cv2.imwrite(client.guild_id_info[str(guild_id)]["enlarged_canvas_path"], canvas)
            json_object = json.dumps(client.guild_id_info, indent=4)
            f = open(r'.\json\guild_ids.json', 'w')
            f.write(json_object)
            f.close()
            if "enlarged_canvas_path" in client.guild_id_info[str(g_id)]:
                cv2.imwrite(client.guild_id_info[str(guild_id)]["enlarged_canvas_path"], canvas)
                json_object = json.dumps(client.guild_id_info, indent=4)
                f = open(r'.\json\guild_ids.json', 'w')
                f.write(json_object)
                f.close()
                with open(client.guild_id_info[str(g_id)]["enlarged_canvas_path"], "rb") as png:
                    attachment = discord.File(png)
                    await ctx.send(file=attachment)
            else:
                client.guild_id_info[str(g_id)]["enlarged_canvas_path"] = ''
        else:
            await ctx.send(f'Server canvas hasn\'t been created yet, use /canvas command to generate')
    else:
        await ctx.send(f'Server canvas hasn\'t been created yet, use /canvas command to generate')


# server canvas commands
@slash.slash(
    name="canvas",
    description="a 120x80 canvas painted by the server members one pixel at a time",
    guild_ids=guild_ids
)
async def canvas(ctx: SlashContext, x, y, color):
    x = int(x)
    y = int(y)
    g_id = str(ctx.guild.id)
    width = 120
    height = 80
    use_rgb = False
    i = 0
    color_rgb = color.split(',')
    for value in color_rgb:
        if value.strip().isnumeric():
            color_rgb[i] = value.strip()
            i += 1
        else:
            break
        use_rgb = True
    if i > 2:
        color_rgb_temp = color_rgb.copy()
        color_rgb[0] = color_rgb_temp[2]
        color_rgb[2] = color_rgb_temp[0]
        color_string = str(color_rgb_temp)
    if i > 3:
        use_rgb = False
    if not use_rgb:
        input_color = sc.spellCheck(str(color).lower(), colorList, charScores)
        color_rgb = [colorList[input_color]["blue"], colorList[input_color]["green"], colorList[input_color]["red"]]
        color_string = str(input_color)
    if not ctx.author.bot:
        if (x > width) or (y > height) or (x < 1) or (y < 1):
            await ctx.send(f'({str(x)}, {str(y)}) is out of bounds! Only values between (1, 1) and  ({str(width)},'
                           f' {str(height)}) are valid')
        else:
            if "server_canvas_path" in client.guild_id_info[str(g_id)]:
                if os.path.exists(client.guild_id_info[str(g_id)]["server_canvas_path"]):
                    canvas = cv2.imread(client.guild_id_info[str(g_id)]["server_canvas_path"], cv2.IMREAD_UNCHANGED)
                    edit_canvas(canvas, x, y, width, height, color_rgb)
                    save_canvas(canvas, client.guild_id_info[str(g_id)]["server_canvas_path"])
                    """
                    with open(client.guild_id_info[str(ctx.guild_id)]["server_canvas_path"], "rb") as png:
                        attachment = discord.File(png)
                        await ctx.send(file=attachment)
                    """
                    await show_canvas_fxn(ctx, g_id)
                    # await show_canvas(ctx) # original sized canvas
                    await ctx.send(f'{color_string} at ({str(x)}, {str(y)}) placed by {str(ctx.author)[:-5]}')
                else:
                    canvas = create_new_canvas(width, height, guild_id)
                    edit_canvas(canvas, x, y, width, height, color_rgb)
                    save_canvas(canvas, client.guild_id_info[str(g_id)]["server_canvas_path"])
                    """
                    with open(client.guild_id_info[str(ctx.guild_id)]["server_canvas_path"], "rb") as png:
                        attachment = discord.File(png)
                        await ctx.send(file=attachment)
                    """
                    await show_canvas_fxn(ctx, g_id)
                    # await show_canvas(ctx) # original sized canvas
                    await ctx.send(f'{color_string} at ({str(x)}, {str(y)}) placed by {str(ctx.author)[:-5]}')
            else:
                canvas = create_new_canvas(width, height, guild_id)
                edit_canvas(canvas, x, y, width, height, color_rgb)
                save_canvas(canvas, client.guild_id_info[str(g_id)]["server_canvas_path"])
                """
                with open(client.guild_id_info[str(ctx.guild_id)]["server_canvas_path"], "rb") as png:
                    attachment = discord.File(png)
                    await ctx.send(file=attachment)
                """
                await show_canvas_fxn(ctx, g_id)
                # await show_canvas(ctx) # original sized canvas
                await ctx.send(f'{color_string} at ({str(x)}, {str(y)}) placed by {str(ctx.author)[:-5]}')


@slash.slash(
    name="show_canvas",
    description="shows an enlarged version of the server canvas",
    guild_ids=guild_ids
)
async def show_canvas(ctx: SlashContext):
    if not ctx.author.bot:
        g_id = str(ctx.guild.id)
        await show_canvas_fxn(ctx, g_id)


@slash.slash(
    name="get_all_color_data",
    description="returns a .json file with all colors on file",
    guild_ids=guild_ids
)
async def get_all_color_data(ctx: SlashContext):
    if not ctx.author.bot:
        with open(".\json\colors.json", "rb") as json:
            attachment = discord.File(json)
            await ctx.send(file=attachment)


client.run(environment["botToken"])
