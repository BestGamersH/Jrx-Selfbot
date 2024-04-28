# Start of something new


import discord
from discord.ext import commands , tasks

import aiohttp
import asyncio
from discord import Member  # Import the Member class
from colorama import Fore, init, Style  # Import Style from colorama
import json
import base64
import io
import datetime
import time
import re
import random
import tracemalloc
import os
import time
import requests
import ctypes
import sys
import ctypes

if len(sys.argv) < 2:
    print("Usage: python main.py <Window_Title>")
    sys.exit(1)

window_title = sys.argv[1]
ctypes.windll.kernel32.SetConsoleTitleW(window_title)

stock_tasks = {}
afk_users = {}
autoresponder_enabled = True
autoresponder_data = {}
afk_reason = None
afk_timestamp = None  # Initialize the AFK timestamp
afk_notified_users = set()  # Store users who have been notified


config_file_path = 'config.json'



if os.path.isfile(config_file_path):
    # Load the configuration from the existing config.json file
    try:
        with open(config_file_path, 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        print(f"Error: {config_file_path} was not found.")
        config = {}
    except json.JSONDecodeError:
        print(f"Error: Failed to load data from {config_file_path}. Invalid JSON data.")
        config = {}
else:
    # Prompt the user for input to create the configuration
    sellix_link = input("Enter your Sellix link: ")
    bot_token = input("Enter your bot token: ")
    command_prefix = input("Enter the command prefix: ")
    ltc_address = input("Enter your LTC address: ")

    # Ask if the user wants to add UPI information
    add_upi = input("Do you want to add UPI information (yes or no): ").lower()
    if add_upi == "yes":
        upi_id = input("Enter your UPI ID: ")
        qr_code_link = input("Enter the link of your UPI QR code: ")
    else:
        upi_id = ""
        qr_code_link = ""

    # Create a dictionary to store the configuration
    config = {
        "sellixLink": sellix_link,
        "token": bot_token,
        "prefix": command_prefix,
        "ltcAddress": ltc_address,
        "upiInfo": {
            "upiId": upi_id,
            "qrCodeLink": qr_code_link
        },
        "binanceId": binance_id
    }

    # Write the configuration to the config.json file
    try:
        with open(config_file_path, 'w') as f:
            json.dump(config, f, indent=4)
        print("Configuration saved to config.json")
    except Exception as e:
        print(f"Error: Failed to save the configuration to {config_file_path}.")

prefix = config.get('prefix', '')
token = config.get('token', '')
binance_id = config.get('binanceId', '')


bot = commands.Bot(command_prefix=prefix, self_bot=True)


@bot.event
async def on_ready():
    print(f"Logged In as {bot.user.name} | Servers: {len(bot.guilds)} | Prefix: {prefix}")
bot.remove_command("help")

@bot.command()
async def help(ctx, module: str = None):
    await ctx.message.delete()

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    prefix = config["prefix"]
    
    if module is None:
        # If no module is specified, show the BGHub message
        help_message = f"> **★ BG SELFBOT ★**\n\n"
        help_message += f"> {prefix}help <module> to see commands\n\n"
    else:
        help_message = ""

    command_list = {
        "🔍 **Encoding/Decoding**": {
            "base64decode": "Decode base64-encoded text",
            "base64encode": "Encode text in base64",
        },
        "🚫 **User Management**": {
            "block": "Block a user",
            "unblock": "Unblock a user",
            "unfriend": "Remove a friend",
            "kick": "Kick User From Discord Server",
            "ban": "Ban User From Discord Server",
        },
        "🧮 **Calculations**": {
            "calc": "Perform calculations",
        },
        "🌐 **Utility**": {
            "claimvanity": "Set a vanity URL for a server",
            "checktoken": "Token Checker.",
            "iplookup": "Look up information for an IP address",
            "mm": "Display MM (middleman) information",
            "qr": "Display a QR code",
            "serverinfo": "Display server information",
            "tos": "Display terms of service",
            "upi": "Display UPI information",
            "ping": "Check the bot's ping",
        },
        "💰 **Crypto**": {
            "getbal": "Get Litecoin balance for an address",
            "ltc": "Display Litecoin address",
            "binance": "Display Binance Id",
            "cltc": "Show current price of LTC",
        },
        "📦 **Store**": {
            "sellix": "Visit our Sellix store or product",
        },
        "📈 **Stock**": {
            "autosender": "Start Auto Sender `autosender <channelid> <interval>`",
            "stopsender": "Stop Auto Sender `stopsender <channelid>`",
        },
        "🤝 **Miscellaneous**": {
            "purge": "Purge messages from the bot",
            "quote": "Send a Quote",
            "avatar": "Get Anyone's Avatar",
            "banner": "Get Anyone's Banner",
            "fix": "Fucks the server...",
            "spam": "Spam the chat",
            "poll": "Create a Poll",
            "checkpromo": "Check promo links",
        },
        "🔁 **Clone**": {
           "clone": "Clones Whole Server With Emojies And Permissions. `Usage `clone <servertocopy> <servertopaste>` ",
        },
        "🔁 **Activity**": {
            "stream": "Set a streaming status",
            "play": "Set a playing status",
            "watching": "Set a watching status",
            "listening": "Set a listening status",
            "stopactivity": "Stop the current activity",
        },
        "😴 **Afk**": {
            "afk": "Set yourself as AFK (Away From Keyboard)",
            "unafk": "Remove your AFK status",
        },
        "☢️ **Raiding [USE AT YOUR OWN RISK]**": {
            "dcall": "Delete All The Channels",
            "drall": "Delete All The Roles",
            "createroles": "Create Roles",
            "grant_admin": "Grant Admin To A Role `.grant_admin @everyone`",
        },   
        "🤖 **Auto Responder**": {
            "startautoresponder": "Start Auto Responder",
            "stopautoresponder": "Stop Auto Responder",
            "setautoresponder": "Set Auto Responder `setautoresponder (word) (thing it will send)`",
        },       
        "👾 **Status Rotator**": {
            "startrotator": "Start Status Rotator",
            "stoprotator": "Stop Status Rotator",
            "setrotator": "Set Status Rotator `setrotator (status) like this .setrotator Bg,.gg/bestgamershk,Ty`",
        },    
    }

    prefix = config["prefix"]
    help_message = f"> **★ BG SELFBOT ★**\n\n"

    if module is not None:
        module = module.lower()
        module_names = {
            "activity": "🔁 **Activity**",
            "clone": "🔁 **Clone**",
            "miscellaneous": "🤝 **Miscellaneous**",
            "stock": "📈 **Stock**",
            "store": "📦 **Store**",
            "crypto": "💰 **Crypto**",
            "utility": "🌐 **Utility**",
            "calculations": "🧮 **Calculations**",
            "encoding": "🔍 **Encoding/Decoding**",
            "afk": "😴 **Afk**",
            "raiding": "☢️ **Raiding [USE AT YOUR OWN RISK]**",
            "user": "🚫 **User Management**",
            "responder": "🤖 **Auto Responder**",
            "rotator": "👾 **Status Rotator**",
        }
        if module in module_names:
            module_name = module_names[module]
            help_message += f"> {module_name}\n"
            for command, description in command_list[module_name].items():
                help_message += f"`{prefix}{command}`: {description}\n"
        else:
            help_message += "> Invalid module specified."
    else:
        help_message += f"> {prefix}help <module> to see commands\n\n"

        for category in command_list:
            help_message += f"> {category}\n"

    await ctx.send(f"> \n{help_message}")

# Activity
@bot.command(aliases=["streaming"])
async def stream(ctx, *, message):
    stream = discord.Streaming(
        name=message,
        url="https://www.twitch.tv/Wallibear",
    )
    await bot.change_presence(activity=stream)
    await ctx.send("- `Stream Created`")
    await ctx.message.delete()

@bot.command(aliases=["playing"])
async def play(ctx, *, message):
    game = discord.Game(name=message)
    await bot.change_presence(activity=game)
    await ctx.send("- `Done.`")
    await ctx.message.delete()

@bot.command(aliases=["watch"])
async def watching(ctx, *, message):
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.watching,
        name=message,
    ))
    await ctx.send("- `Done.`")
    await ctx.message.delete()

@bot.command(aliases=["listen"])
async def listening(ctx, *, message):
    await bot.change_presence(activity=discord.Activity(
        type=discord.ActivityType.listening,
        name=message,
    ))
    await ctx.reply("- `Done.`")
    await ctx.message.delete()
    

@bot.command(aliases=['bal', 'ltcbal'])
async def getbal(ctx, ltcaddress):
    await ctx.message.delete()

    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8  
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("Failed to retrieve balance. Please check the Litecoin address.")
        return

    
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("Failed to retrieve the current price of Litecoin.")
        return
    
    
    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    
    message = f"LTC Address: `{ltcaddress}`\n"
    message += f"Current LTC: **${usd_balance:.2f} USD**\n"
    message += f"Total LTC Received: **${usd_total_balance:.2f} USD**\n"
    message += f"Unconfirmed LTC: **${usd_unconfirmed_balance:.2f} USD**"
    
    
    response_message = await ctx.send(message)
    
    
    await asyncio.sleep(60)
    await response_message.delete()




@bot.command()
async def block(ctx, user: discord.User):
    try:
        await user.block()
        await ctx.send(f'{user.mention} has been blocked by {ctx.author.mention}.')
    except discord.NotFound:
        await ctx.send("User not found.")

@bot.command()
async def unblock(ctx, user: discord.User):
    try:
        await user.unblock()
        await ctx.send(f'{user.mention} has been unblocked by {ctx.author}.')
    except discord.NotFound:
        await ctx.send("User not found.")

# STREAM, PLAYING, LISTEN, WATCHING STOP CMD>>
@bot.command(aliases=[
    "stopstreaming", "stopstatus", "stoplistening", "stopplaying",
    "stopwatching"
])
async def stopactivity(ctx):
    await ctx.message.delete()
    await bot.change_presence(activity=None, status=discord.Status.dnd)

#autoresponder
# Autoresponder functions
def load_autoresponder_data():
    try:
        with open("autoresponder.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_autoresponder_data(data):
    with open("autoresponder.json", "w") as f:
        json.dump(data, f, indent=4)

# Load initial autoresponder data
autoresponder_data = load_autoresponder_data()

# Enable/disable autoresponder
@bot.command()
async def startautoresponder(ctx):
    global autoresponder_enabled
    autoresponder_enabled = True
    await ctx.send("Autoresponder feature has been enabled.")

@bot.command()
async def stopautoresponder(ctx):
    global autoresponder_enabled
    autoresponder_enabled = False
    await ctx.send("Autoresponder feature has been disabled.")

# Set autoresponder
@bot.command()
async def setautoresponder(ctx, word, *, thingtosend):
    if not autoresponder_enabled:
        await ctx.send("Autoresponder feature is currently disabled. Use `.startautoresponder` to enable.")
        return

    autoresponder_data[word.lower()] = thingtosend
    save_autoresponder_data(autoresponder_data)
    response = f"Autoresponder set for '{word}': {thingtosend}"

    if isinstance(ctx.channel, discord.DMChannel):
        await ctx.author.send(response)
    else:
        await ctx.send(response)

# AFK
@bot.event
async def on_message(message):
    if not message.author.bot:
        if autoresponder_enabled:
            if isinstance(message.channel, discord.DMChannel):
                for word, response in autoresponder_data.items():
                    if word.lower() in message.content.lower():
                        await message.author.send(response)

        if isinstance(message.channel, discord.DMChannel):
            if afk_reason is not None and message.author.id not in afk_notified_users:
                if message.author != bot.user:
                    reply_message = f"**Nitro Prices** Yearly Booster: 16$ Monthly Booster 2$"
                    await message.author.send(reply_message)
                    afk_notified_users.add(message.author.id)
        else:
            if bot.user in message.mentions and message.author != bot.user:
                if afk_reason is not None:
                    if afk_timestamp is not None:
                        current_time = int(time.time())
                        reply_message = f"**Nitro Prices** Yearly Booster: 16$ Monthly Booster 2$"
                        await message.channel.send(reply_message)
                    else:
                        await message.channel.send("I'm currently AFK, but I don't have a specific start time.")

    await bot.process_commands(message)


    
@bot.command()
async def afk(ctx, *, reason="No reason provided"):
    global afk_reason, afk_timestamp
    afk_reason = reason
    afk_timestamp = int(time.time())  # Store the current timestamp
    afk_users[ctx.author.id] = afk_reason
    await ctx.send(f"You are now showing price on ping")

@bot.command()
async def unafk(ctx):
    global afk_reason
    afk_reason = None
    if ctx.author.id in afk_users:
        del afk_users[ctx.author.id]
        await ctx.send(f"Welcome back, {ctx.author.mention}! You are no longer AFK.")
        

@bot.command()
async def allcmd(ctx):
    await ctx.message.delete()

    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    prefix = config["prefix"]

    command_list = {
        "🔍 **Encoding/Decoding**": {
            "base64decode": "Decode base64-encoded text",
            "base64encode": "Encode text in base64",
        },
        "🚫 **User Management**": {
            "block": "Block a user",
            "unblock": "Unblock a user",
            "unfriend": "Remove a friend",
            "kick": "Kick User From Discord Server",
            "ban": "Ban User From Discord Server",
        },
        "🧮 **Calculations**": {
            "calc": "Perform calculations",
        },
        "🌐 **Utility**": {
            "claimvanity": "Set a vanity URL for a server",
            "checktoken": "Token Checker.",
            "iplookup": "Look up information for an IP address",
            "mm": "Display MM (middleman) information",
            "qr": "Display a QR code",
            "serverinfo": "Display server information",
            "tos": "Display terms of service",
            "upi": "Display UPI information",
            "ping": "Check the bot's ping",
        },
        "💰 **Crypto**": {
            "getbal": "Get Litecoin balance for an address",
            "ltc": "Display Litecoin address",
            "binance": "Display Binance Id",
            "cltc": "Show current price of LTC",
        },
        "📦 **Store**": {
            "sellix": "Visit our Sellix store or product",
        },
        "📈 **Stock**": {
            "autosender": "Start Auto Sender `autosender <channelid> <interval>`",
            "stopsender": "Stop Auto Sender `stopsender <channelid>`",
        },
        "🤝 **Miscellaneous**": {
            "purge": "Purge messages from the bot",
            "quote": "Send a Quote",
            "avatar": "Get Anyone's Avatar",
            "banner": "Get Anyone's Banner",
            "fix": "Fucks the server...",
            "spam": "Spam the chat",
            "poll": "Create a Poll",
            "checkpromo": "Check promo links",
        },
        "🔁 **Clone**": {
           "clone": "Clones Whole Server With Emojies And Permissions. `Usage `clone <servertocopy> <servertopaste>` ",
        },
        "🔁 **Activity**": {
            "stream": "Set a streaming status",
            "play": "Set a playing status",
            "watching": "Set a watching status",
            "listening": "Set a listening status",
            "stopactivity": "Stop the current activity",
        },
        "😴 **Afk**": {
            "afk": "Set yourself as AFK (Away From Keyboard)",
            "unafk": "Remove your AFK status",
        },
        "☢️ **Raiding [USE AT YOUR OWN RISK]**": {
            "dcall": "Delete All The Channels",
            "drall": "Delete All The Roles",
            "createroles": "Create Roles",
            "grant_admin": "Grant Admin To A Role `.grant_admin @everyone`",
        },   
        "🤖 **Autoresponder**": {
            "startautoresponder": "Start Auto Responder",
            "stopautoresponder": "Stop Auto Responder",
            "setautoresponder": "Set Auto Responder `setautoresponder (word) (thing it will send)`",
        },       
        "👾 **Status Rotator**": {
            "startrotator": "Start Status Rotator",
            "stoprotator": "Stop Status Rotator",
            "setrotator": "Set Status Rotator `setrotator (status) like this .setrotator Bg,.gg/bestgamershk,Ty`",
        },    
    }

    help_message = "Here are all available commands:\n\n"

    for category in command_list:
        help_message += f"{category}\n"
        for command, description in command_list[category].items():
            help_message += f"`{prefix}{command}`: {description}\n"

    await ctx.send(help_message)

# Clone
def print_add(message):
    print(f'{Fore.GREEN}[+]{Style.RESET_ALL} {message}')

def print_delete(message):
    print(f'{Fore.RED}[-]{Style.RESET_ALL} {message}')

def print_warning(message):
    print(f'{Fore.RED}[WARNING]{Style.RESET_ALL} {message}')

def print_error(message):
    print(f'{Fore.RED}[ERROR]{Style.RESET_ALL} {message}')

class Clone:
    @staticmethod
    async def roles_delete(guild_to: discord.Guild):
        for role in guild_to.roles:
            try:
                if role.name != "@everyone":
                    await role.delete()
                    print_delete(f"Deleted Role: {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Delete Role: {role.name}")

    @staticmethod
    async def roles_create(guild_to: discord.Guild, guild_from: discord.Guild):
        roles = []
        role: discord.Role
        for role in guild_from.roles:
            if role.name != "@everyone":
                roles.append(role)
        roles = roles[::-1]
        for role in roles:
            try:
                await guild_to.create_role(
                    name=role.name,
                    permissions=role.permissions,
                    colour=role.colour,
                    hoist=role.hoist,
                    mentionable=role.mentionable
                )
                print_add(f"Created Role {role.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Role: {role.name}")
            except discord.HTTPException:
                print_error(f"Unable to Create Role: {role.name}")

    @staticmethod
    async def channels_delete(guild_to: discord.Guild):
        for channel in guild_to.channels:
            try:
                await channel.delete()
                print_delete(f"Deleted Channel: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Channel: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Channel: {channel.name}")

    @staticmethod
    async def categories_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channels = guild_from.categories
        channel: discord.CategoryChannel
        new_channel: discord.CategoryChannel
        for channel in channels:
            try:
                overwrites_to = {}
                for key, value in channel.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                new_channel = await guild_to.create_category(
                    name=channel.name,
                    overwrites=overwrites_to)
                await new_channel.edit(position=channel.position)
                print_add(f"Created Category: {channel.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Category: {channel.name}")
            except discord.HTTPException:
                print_error(f"Unable To Delete Category: {channel.name}")

    @staticmethod
    async def channels_create(guild_to: discord.Guild, guild_from: discord.Guild):
        channel_text: discord.TextChannel
        channel_voice: discord.VoiceChannel
        category = None
        for channel_text in guild_from.text_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_text.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_text.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_text.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position,
                        topic=channel_text.topic,
                        slowmode_delay=channel_text.slowmode_delay,
                        nsfw=channel_text.nsfw)
                except:
                    new_channel = await guild_to.create_text_channel(
                        name=channel_text.name,
                        overwrites=overwrites_to,
                        position=channel_text.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Text Channel: {channel_text.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Text Channel: {channel_text.name}")
            except:
                print_error(f"Error While Creating Text Channel: {channel_text.name}")

        category = None
        for channel_voice in guild_from.voice_channels:
            try:
                for category in guild_to.categories:
                    try:
                        if category.name == channel_voice.category.name:
                            break
                    except AttributeError:
                        print_warning(f"Channel {channel_voice.name} doesn't have any category!")
                        category = None
                        break

                overwrites_to = {}
                for key, value in channel_voice.overwrites.items():
                    role = discord.utils.get(guild_to.roles, name=key.name)
                    overwrites_to[role] = value
                try:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position,
                        bitrate=channel_voice.bitrate,
                        user_limit=channel_voice.user_limit,
                        )
                except:
                    new_channel = await guild_to.create_voice_channel(
                        name=channel_voice.name,
                        overwrites=overwrites_to,
                        position=channel_voice.position)
                if category is not None:
                    await new_channel.edit(category=category)
                print_add(f"Created Voice Channel: {channel_voice.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")
            except discord.HTTPException:
                print_error(f"Unable To Creating Voice Channel: {channel_voice.name}")
            except:
                print_error(f"Error While Creating Voice Channel: {channel_voice.name}")

    @staticmethod
    async def emojis_delete(guild_to: discord.Guild):
        for emoji in guild_to.emojis:
            try:
                await emoji.delete()
                print_delete(f"Deleted Emoji: {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Deleting Emoji{emoji.name}")
            except discord.HTTPException:
                print_error(f"Error While Deleting Emoji {emoji.name}")

    @staticmethod
    async def emojis_create(guild_to: discord.Guild, guild_from: discord.Guild):
        emoji: discord.Emoji
        for emoji in guild_from.emojis:
            try:
                emoji_image = await emoji.url.read()
                await guild_to.create_custom_emoji(
                    name=emoji.name,
                    image=emoji_image)
                print_add(f"Created Emoji {emoji.name}")
            except discord.Forbidden:
                print_error(f"Error While Creating Emoji {emoji.name} ")
            except discord.HTTPException:
                print_error(f"Error While Creating Emoji {emoji.name}")

    @staticmethod
    async def guild_edit(guild_to: discord.Guild, guild_from: discord.Guild):
        try:
            try:
                icon_image = await guild_from.icon_url.read()
            except discord.errors.DiscordException:
                print_error(f"Can't read icon image from {guild_from.name}")
                icon_image = None
            await guild_to.edit(name=f'{guild_from.name}')
            if icon_image is not None:
                try:
                    await guild_to.edit(icon=icon_image)
                    print_add(f"Guild Icon Changed: {guild_to.name}")
                except:
                    print_error(f"Error While Changing Guild Icon: {guild_to.name}")
        except discord.Forbidden:
            print_error(f"Error While Changing Guild Icon: {guild_to.name}")

@bot.command()
async def clone(ctx, source_guild_id, destination_guild_id):
    # Convert guild IDs to integers
    source_guild_id = int(source_guild_id)
    destination_guild_id = int(destination_guild_id)

    # Fetch the guilds from their IDs
    source_guild = bot.get_guild(source_guild_id)
    destination_guild = bot.get_guild(destination_guild_id)

    if source_guild is None or destination_guild is None:
        await ctx.send("One or both of the guilds couldn't be found.")
        return

    # Clone roles, channels, categories, emojis, and edit guild information
    await Clone.roles_delete(destination_guild)
    await Clone.roles_create(destination_guild, source_guild)
    await Clone.channels_delete(destination_guild)
    await Clone.categories_create(destination_guild, source_guild)
    await Clone.channels_create(destination_guild, source_guild)
    await Clone.emojis_delete(destination_guild)
    await Clone.emojis_create(destination_guild, source_guild)
    await Clone.guild_edit(destination_guild, source_guild)

    # Send the completion message to the same channel where the command was invoked
    await ctx.send("Cloning completed!")

# RAIDING
@bot.command(name='dcall')
async def delete_channels(ctx):
    guild = ctx.guild
    text_channels = guild.text_channels
    channels_to_delete = [channel for channel in text_channels if channel != ctx.channel]
    await asyncio.gather(*[channel.delete() for channel in channels_to_delete])
    await ctx.send("All existing channels, except the command invocation channel, have been deleted.")

@bot.command(name='drall')
async def delete_all_roles(ctx):
    guild = ctx.guild

    if guild is not None:
        roles = guild.roles

        for role in roles:
            if role != guild.default_role:
                try:
                    await role.delete()
                except discord.Forbidden:
                    await ctx.send(f"Cannot delete role '{role.name}' due to permission restrictions.")
                except discord.HTTPException:
                    await ctx.send(f"An error occurred while deleting role '{role.name}'.")

        await ctx.send("All non-default roles have been deleted.")
    else:
        await ctx.send("The bot is not currently in a server.")

@bot.command(name='createroles')
async def create_roles(ctx, number_of_roles: int, role_name: str):
    guild = ctx.guild

    if guild is not None:
        for _ in range(number_of_roles):
            try:
                await guild.create_role(name=role_name)
            except discord.Forbidden:
                await ctx.send(f"Cannot create the role '{role_name}' due to permission restrictions.")
            except discord.HTTPException:
                await ctx.send(f"An error occurred while creating the role '{role_name}'.")

        await ctx.send(f"Created {number_of_roles} roles with the name '{role_name}'.")
    else:
        await ctx.send("The bot is not currently in a server.")


@bot.command()
async def grant_admin(ctx, role_name):
    # Check if the user has the 'Administrator' permission
    if ctx.message.author.guild_permissions.administrator:
        # Find the role by name
        role = discord.utils.get(ctx.guild.roles, name=role_name)
        if role:
            # Grant administrator permissions to the role
            await role.edit(permissions=discord.Permissions.all())

            await ctx.send(f"Administrator permissions granted to the {role.name} role.")
        else:
            await ctx.send("Role not found.")
    else:
        await ctx.send("You do not have the required permissions to use this command.")

# uh

@bot.command()
async def base64encode(ctx, *, text):
    # Encode the text to base64
    encoded_text = base64.b64encode(text.encode()).decode()
    await ctx.send(f'Base64 encoded: {encoded_text}')

@bot.command()
async def base64decode(ctx, *, encoded_text):
    try:
        # Decode the base64 encoded text
        decoded_text = base64.b64decode(encoded_text).decode()
        await ctx.send(f'Base64 decoded: {decoded_text}')
    except base64.binascii.Error:
        await ctx.send('Invalid base64 encoded text.')


# uhhh
@bot.command()
async def avatar(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    avatar_url = user.avatar_url if user.avatar else user.default_avatar_url

    try:
        await ctx.send(avatar_url)
        await ctx.message.add_reaction('<a:v_:1105968883833241742>')
    except discord.errors.HTTPException:
        await ctx.message.add_reaction('❌')

@bot.command()
async def banner(ctx, user: discord.User = None):
    if user is None:
        user = ctx.author

    req = await bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=user.id))
    banner_id = req["banner"]

    if banner_id:
        banner_url = f"https://cdn.discordapp.com/banners/{user.id}/{banner_id}"
        
        # Check if the banner is a GIF
        if banner_id.startswith("a_"):  # Check if it's a GIF by checking if it starts with "a_"
            banner_url += ".gif?size=1024"
        else:
            banner_url += ".png?size=1024"

        await ctx.send(f"{banner_url}")
    else:
        await ctx.send("User does not have a banner.")



@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.kick(reason=reason)
    await ctx.send(f"{member.mention} has been kicked from the server. Reason: {reason}")

@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="No reason provided"):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} has been banned from the server. Reason: {reason}")

@bot.command()
async def poll(ctx, *options):
    if len(options) < 2:
        await ctx.send('Please provide at least two options for the poll.')
        return

    poll_message = await ctx.send(f"Poll by {ctx.author.display_name}:\n\n" + "\n".join([f"{i + 1}. {option}" for i, option in enumerate(options)]))

    for i in range(len(options)):
        await poll_message.add_reaction(f"{i + 1}\u20e3")

@bot.command()
async def quote(ctx):
    api_url = 'https://api.quotable.io/random'
    response = requests.get(api_url)
    data = response.json()

    if 'content' in data and 'author' in data:
        quote_content = data['content']
        quote_author = data['author']
        await ctx.send(f"Random Quote:\n{quote_content}\n- {quote_author}")
    else:
        await ctx.send('Failed to fetch a quote.')

@bot.command()
async def spam(ctx, times: int, *, message):
    for _ in range(times):
        await ctx.send(message)
        await asyncio.sleep(0.1)     


@bot.command()
async def ping(ctx):
    
    latency = round(bot.latency * 1000)  

    
    await ctx.send(f'**~ {latency}ms**')



@bot.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"The current price of Litecoin (LTC) is ${price:.2f}")
    else:
        await ctx.send("Failed to fetch Litecoin price")

@bot.command(aliases=["clear"])
async def purge(ctx, amount: int = None):
    await ctx.message.delete()
    
    def filter_messages(message):
        return message.author == ctx.bot.user
    
    if amount is None:
        await ctx.send("Please specify the number of messages to delete.")
        return
    
    messages_to_delete = []
    
    async for message in ctx.message.channel.history(limit=amount):
        if filter_messages(message):
            messages_to_delete.append(message)
    
    for message in messages_to_delete:
        try:
            await message.delete()
        except discord.Forbidden:
            pass
        except discord.NotFound:
            pass
    
    print(f"{Fore.GREEN}[+] PURGED SUCCESSFULLY✅")

@bot.command()
async def hackclear(ctx):
    await ctx.send("⠀" + "\n"*1998 + "⠀")
    await ctx.message.delete()

@bot.command()
async def autosender(ctx, channel: discord.TextChannel, interval_minutes: float):
    try:
        # Check if the provided channel is valid
        if not channel:
            await ctx.send("Invalid channel.")
            return

        # Ask the user for the message
        await ctx.send("Please enter the message you want to send:")

        def check_reply(message):
            return message.author == ctx.author and message.channel == ctx.channel

        message = await bot.wait_for("message", check=check_reply, timeout=60)
        content = message.content

        # Create a loop to send the message at the specified interval
        async def send_message():
            while ctx.channel.id in stock_tasks:
                await asyncio.sleep(interval_minutes * 60)  # Convert minutes to seconds
                await channel.send(content)

        # Start the task and store it in the dictionary
        stock_task = bot.loop.create_task(send_message())
        stock_tasks[ctx.channel.id] = stock_task
        await ctx.send(f"Stock messages started in {channel.mention} with an interval of {interval_minutes} minutes.")

    except asyncio.TimeoutError:
        await ctx.send("You took too long to provide the input. The command has been canceled.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")



@bot.command()
async def stopsender(ctx):
    # Check if a stock task is running in the channel
    if ctx.channel.id in stock_tasks:
        # Cancel the task
        stock_tasks[ctx.channel.id].cancel()
        del stock_tasks[ctx.channel.id]
        await ctx.send("Stock messages stopped.")
    else:
        await ctx.send("No stock messages are running in this channel.")
        

@bot.command()
async def mm(ctx):
    await ctx.message.delete()
    await ctx.send(
        '`MM`: discord.gg/use-mm'
    )

@bot.command()
async def restart(ctx):
    await ctx.send("Restarting bot...")
    os.execl(sys.executable, sys.executable, *sys.argv)

@bot.command()
async def iplookup(ctx, ip):
    api_key = 'a91c8e0d5897462581c0c923ada079e5'  
    api_url = f'https://api.ipgeolocation.io/ipgeo?apiKey={api_key}&ip={ip}'
    
    response = requests.get(api_url)
    data = response.json()
    
    if 'country_name' in data:
        country = data['country_name']
        city = data['city']
        isp = data['isp']
        current_time_unix = data['time_zone']['current_time_unix']

        current_time_formatted = f"<t:{int(current_time_unix)}:f>"
        
        message = f"IP Lookup Results for {ip}:\n"
        message += f"Country: {country}\n"
        message += f"City: {city}\n"
        message += f"ISP: {isp}\n"
        message += f"Current Time: {current_time_formatted}\n"
        
        await ctx.send(message)
    else:
        await ctx.send("Invalid IP address or an error occurred during the lookup.")

@bot.command()
async def claimvanity(ctx, vanity: str, guildid: int):
    try:
        guild = bot.get_guild(guildid)
        if guild:
            await guild.edit(vanity_code=vanity)
            await ctx.send(f"Vanity URL set to discord.gg/{vanity} for the server {guild.name}")
        else:
            await ctx.send("Guild not found.")
    except discord.Forbidden:
        await ctx.send("I don't have permission to change the vanity URL.")
    except discord.HTTPException as e:
        await ctx.send(f"An error occurred: {e}")
    except Exception as e:
        await ctx.send(f"An unexpected error occurred: {e}")


@bot.command()
async def unfriend(ctx, *, user: discord.User):
    await user.remove_friend()
    await ctx.reply('> **User has been removed**')


with open('config.json') as config_file:
    config_data = json.load(config_file)

# Get the values you need from the config data
sellix_link = config_data.get("sellixLink", "")
ltc_address = config_data.get("ltcAddress", "")
upi_info = config_data.get("upiInfo", {})
binance_id = config.get('binanceId', '')

@bot.command()
async def binance(ctx):
    await ctx.message.delete()
    await ctx.send(f'`Binance ID`: **{binance_id}**')

@bot.command()
async def qr(ctx):
    await ctx.message.delete()
    qr_code_link = upi_info.get('qrCodeLink', '')
    await ctx.send(qr_code_link)

@bot.command()
async def upi(ctx):
    await ctx.message.delete()
    upi_id = upi_info.get('upiId', '')
    await ctx.send(f'`UPI`: **{upi_id}**')

@bot.command()
async def sellix(ctx):
    await ctx.message.delete()
    await ctx.send(f'`Sellix -->`: **{sellix_link}**')

@bot.command()
async def ltc(ctx):
    await ctx.message.delete()
    await ctx.send(f'`LTC ADDY`: **{ltc_address}**')

@bot.command()
async def vouch(ctx, arg, args):
    await ctx.reply(f'`+rep <@{ctx.author.id}> Legit Got {arg} FOR {args}`')


@bot.command()
async def calc(ctx, *, equation: str):
    try:
        result = eval(equation)
        await ctx.message.delete()
        await ctx.send(f"Result of `{equation}` is: **{result}**")
    except Exception as e:
        await ctx.send(f"An error occurred: {str(e)}")

@bot.command()
async def tos(ctx):
    await ctx.message.delete()
    tos_message = (
        "🟢 **Terms of Service (TOS)**\n"
        "1. No refunds, only replacements.\n"
        "2. Respect the product you receive.\n"
        "3. Do not share products with others.\n"
        "4. No unauthorized products resale or distribution."
        "5. If You Fail To Follow TOS No Refunds/No Replacement."
    )
    await ctx.send(tos_message)

def hide_token(token, visible_chars=10):
    hidden_chars = len(token) - visible_chars
    return f'{token[:visible_chars]}{"*" * hidden_chars}'

def get_nitro_type_info(nitro_type):
    if nitro_type == 1:
        return 'Nitro Classic (Nitro)'
    elif nitro_type == 2:
        return 'Nitro Boost'
    else:
        return 'None'

def calculate_account_age(created_at):
    now = datetime.datetime.utcnow()
    epoch = datetime.datetime.utcfromtimestamp(0)
    created_at_datetime = epoch + datetime.timedelta(milliseconds=created_at)
    age = now - created_at_datetime
    return age

def calculate_nitro_expiry_days(expiry_timestamp):
    if expiry_timestamp:
        now = datetime.datetime.utcnow()
        expiry_datetime = datetime.datetime.utcfromtimestamp(expiry_timestamp / 1000)
        remaining_days = (expiry_datetime - now).days
        return remaining_days
    return None

@bot.command(name='checktoken')
async def check_token(ctx, token):
    await ctx.message.delete()
    url = 'https://discord.com/api/v9/users/@me'
    headers = {'Authorization': token}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        await ctx.send(f'Token {token} is invalid.')
        return
    
    data = response.json()
    
    try:
        created_at = int(data['id']) >> 22
        nitro_type_info = get_nitro_type_info(data.get('premium_type', 0))
        username = data.get('username', 'Unknown')
        hidden_token = hide_token(token)
        age = calculate_account_age(created_at)
        expiry_timestamp = data.get('premium_expires', None)
        remaining_days = calculate_nitro_expiry_days(expiry_timestamp)
        
        expiry_message = f'Nitro Expires in: {remaining_days} days.' if remaining_days is not None else 'Nitro Expires: Never'
        
        formatted_message = (
            f'Token {hidden_token} is valid and belongs to {username}.\n'
            f'Display Name: {data.get("username")}#{data.get("discriminator")}\n'
            f'Discord Nitro: **{nitro_type_info}**.\n'
            f'Account created: {age.days} days ago.\n'
        )
        await ctx.send(formatted_message)
    except KeyError:
        await ctx.send(f'Unable to retrieve account information for Token {token}.')


@bot.command()
async def serverinfo(ctx):
    await ctx.message.delete()
    server_name = ctx.guild.name
    server_id = ctx.guild.id
    member_count = ctx.guild.member_count 
    server_created_at = ctx.guild.created_at
    server_owner = ctx.guild.owner
    
    response = f"Server name: {server_name}\n"
    response += f"Server ID: {server_id}\n"
    response += f"Server created at: {server_created_at}\n"
    response += f"Server owner: {server_owner}\n"
    response += f"Server Members: {member_count}\n"    
    
    await ctx.send(response)

url = "https://discord.com/api/v9/users/@me/settings"

def read_token():
    with open("config.json", "r") as config_file:
        config_data = json.load(config_file)
        return config_data["token"]

authorization_token = read_token()

with open("status.txt", "r") as file:
    status_lines = file.readlines()

headers = {
    "Authorization": authorization_token
}

status_lines = []  # Initialize an empty list for statuses


index = 0
status_task = None

@bot.command()
async def setrotator(ctx, *, statuses):
    global status_lines
    status_lines = statuses.split(',')
    status_lines = [status.strip() for status in status_lines]
    await ctx.send(f"Status set to: {', '.join(status_lines)}")

@bot.command()
async def startrotator(ctx):
    global status_task
    if status_task is None:
        status_task = bot.loop.create_task(update_status())
        await ctx.send("Status update task started.")
    else:
        await ctx.send("Status update task is already running.")

@bot.command()
async def stoprotator(ctx):
    global status_task
    if status_task is not None:
        status_task.cancel()
        status_task = None
        await ctx.send("Status update task stopped.")
    else:
        await ctx.send("Status update task is not running.")

async def update_status():
    global index
    while True:
        if index >= len(status_lines):
            index = 0

        status_message = status_lines[index].strip()

        json_data = {
            "status": "dnd",
            "custom_status": {
                "text": status_message
            }
        }

        response = requests.patch(url, headers=headers, json=json_data)

        if response.status_code == 200:
            print(f"Status changed to: {status_message}")
        else:
            print(f"Failed to change status. Status code: {response.status_code}")

        index += 1

        await asyncio.sleep(2)

bot.run(token, bot=False)
