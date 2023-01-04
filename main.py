import asyncio

import discord
import nextcord
import mysql
from nextcord.ext import commands,tasks
from nextcord import Interaction,utils
import random
import os
import time
import json
from itertools import cycle
import mysql.connector


client = commands.Bot(command_prefix="!",intents=nextcord.Intents.default(),case_insensitive=False,strip_after_prefix=False)
dataBaseinfo = {}
elapsedTime = 0.0
rebeccapink = 0xfa00ff
db : mysql.connector.connection
dbCursor : mysql.connector.connection.MySQLCursorBuffered
dbDictCursor : mysql.connector.connection.MySQLCursorBufferedDict
globalVariable = "Global/global.json"
@client.event
async def on_ready():
    print("AcaciaBot is Online")

    try:
        connectodb()
    except:
        channel = client.get_channel(561541369877757952)
        print("No database connection, system will not work.")
        await channel.send("No database connection, system will not work.")



def connectodb():
    global db
    global dbCursor
    global dbDictCursor
    dbinfo = LoadCache(address="Global/db.json",debug=False)
    db = mysql.connector.connect(host = dbinfo["host"],user = dbinfo["user"],passwd = dbinfo["password"],database = dbinfo["database"])
    db.autocommit = True
    dbCursor = db.cursor(buffered=True)
    dbDictCursor = db.cursor(buffered=True,dictionary=True)
    print(f"Connected to {db.database}")
    try:
        maintainconnection.stop()
    finally:
        maintainconnection.start()










@tasks.loop(minutes=4)
async def maintainconnection():
    try:
        database : mysql.connector.connection.MySQLConnectionAbstract = db
        database.ping(reconnect=True,attempts=4,delay=1)
        #print(f"Rebecca still has connection to {database.database}")
    except:
        maintainconnection.stop()
        channel = client.get_channel(561541369877757952)
        await channel.send("Rebecca lost connection to her database and failed to reconnect after 4 attempts. Please contact Baran to re-establish database connection.")







#Legacy Data persistance system relies on json files stored within to function. A default config file is needed to store the default values of the variables stored. Although this bot supports mysql databases now, the legacy json support will remain. A backup system is added to ensure data integrity by hourly backing up the legacy files into the database.
def BringValue(address, Uvariable):
    f = open(address, "r")
    variable = json.load(f)
    print(f"Loaded the {address}, {Uvariable}:{variable[Uvariable]}")
    f.close()
    return variable[Uvariable]



def WriteValue(address, Uvariable, Value):
    a_file = open(address, "r")
    json_object = json.load(a_file)
    a_file.close()
    print(f"Loaded the {address}")
    json_object[Uvariable] = Value
    a_file = open(address, "w")
    print(f"Wrote {Uvariable} : {Value} at {address}")
    json.dump(json_object, a_file, indent=5)
    a_file.close()


def AddValue(address, Uvariable, Value):
    file = open(address, "r")
    variable = json.load(file)
    variable[Uvariable] = Value
    file.close()
    file = open(address, "w")
    json.dump(variable, file, indent=5)
    file.close()
    print(f"Adding new entry {Uvariable} : {Value} to {address} ")


def LoadCache(address,debug = True):
    file = open(address, "r")
    variable = json.load(file)
    file.close()
    if debug:
        print(f"Loaded {variable} to ram from {address}")
    return variable


def EnterCache(address, collection,debug = True):
    file = open(address, "w")
    json.dump(collection, file, indent=5)
    file.close()
    if debug:
        print(f"Loaded the {collection} in ram to the disk.")


def EraseDefaults(address, Uvariable):
    currentCache = LoadCache(address)
    default = BringValue(address=globalVariable, Uvariable=Uvariable)
    newCache = {}
    totalRemoved = 0
    for x in currentCache:
        if currentCache[x] != default:
            newCache[x] = currentCache[x]
        else:
            totalRemoved += 1
    EnterCache(address=address, collection=newCache)
    print(f"{totalRemoved} entries removed from {address}")



def IncrementTime():
    global elapsedTime
    elapsedTime+=1


async def restart(ctx):

    await exec(open("main.py").read())
    await ctx.send("Restart in progress")
    #await shutdown(ctx=ctx)

@client.slash_command(name="shutdown",description="Shuts down the bot",guild_ids=[560911418896023553])
async def shutdown(ctx):
    await ctx.send("Bot is shutting down.")
    await client.close()


def externalUnload(extension):
    client.unload_extension(extension)
    print(f"unloaded {extension} ")


def timeformatter(entry: float):
    text = "Days"
    time = int(round(entry/ (24*3600),1))  # day
    if time == 0:
        time = int(round(entry/3600,1))
        text = "Hours"
    if time == 0:
        time = int(round(entry/60,1))  # minutes
        text = "Minutes"
    if time == 0:
        time = entry  # second
        text = "Seconds"
    text = f"{time} {text}"

    return text



async def ping(ctx):
    await ctx.send(f"Bot Latency = {round(client.latency, 2)}ms")
    print(f"Bot Latency = {round(client.latency, 2)}ms")



async def load(ctx, extension):
    client.load_extension(f"cogs.{extension}")
    print(f"loaded {extension} ")
    await ctx.send(f"loaded {extension}")



async def reload(ctx, extension):
    await unload(ctx, extension)
    await load(ctx, extension)




async def flushtoken(ctx):
    newtoken = {}
    EnterCache(address="Token.json",collection=newtoken)




async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print(f"unloaded {extension} ")
    await ctx.send(f"unloaded {extension}")


def leaderboard(address, number=10, order=True,symbol = ""):
    all = LoadCache(address=address)
    a = sorted(all, key=all.get, reverse=order)
    length = len(a)
    if length > number:
        length = number
    number = 1
    t = """"""
    for x in range(length):
        t = t + f"""{number:,}. <@{a[number - 1]}> - {all[a[number - 1]]:,} {symbol}

"""
        number = number + 1
    if length == 0:
        t = "No data"

    return t
def leaderboardbycache(all : dict, number=10, order=True,symbol = ""):
    a = sorted(all, key=all.get, reverse=order)
    length = len(a)
    if length > number:
        length = number
    number = 1
    t = """"""
    for x in range(length):
        t = t + f"""{number:,}. <@{a[number - 1]}> - {all[a[number - 1]]:,} {symbol}

"""
        number = number + 1
    if length == 0:
        t = "No data"

    return t


def getTotal(address):
    cache = LoadCache(address)
    total = 0
    for key in cache:
        total += cache[key]

    return total


def inspectVariable(author, uvariable, address):
    try:
        value = BringValue(address=address, Uvariable=f"{author}")
    except:
        value = BringValue(address=globalVariable, Uvariable=uvariable)
        AddValue(address=address, Uvariable=f"{author}", Value=value)


def getrank(address, author):
    rank = 0
    cache = LoadCache(address)
    rankSuffix = ["th", "st", "nd", "rd"]
    s = sorted(cache, key=cache.get, reverse=True)

    for x in range(len(s)):

        if author == s[x]:
            rank += 1
            break
        rank += 1

    if rank % 10 in [1, 2, 3] and rank not in [11, 12, 13]:
        t = f"{rank}{rankSuffix[rank % 10]}"
    else:
        t = f"{rank}{rankSuffix[0]}"
    return t

def attempt(s):
    client.load_extension(s)

for filename in os.listdir('./cogs'):
    if filename.endswith(".py"):
        attempt(f"cogs.{filename[:-3]}")
        print(f"Loaded {filename[:-3]}")
try:
    token = BringValue("Token.json", "Token")
except:
    token = ""

if token == "":
    print("Token in the Token.json file is missing, please enter the bot token by hand:")
    token = input()
    WriteValue("Token.json", "Token", token)


client.run(token)