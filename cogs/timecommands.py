import asyncio
from datetime import datetime

import nextcord
import pytz
from nextcord import Interaction, Member, Embed, utils, SlashOption, TextChannel, ChannelType, Permissions, ActionRow, \
    Button, ButtonStyle
from nextcord.abc import GuildChannel
from nextcord.ext import commands, tasks
from nextcord.ext.commands import TextChannelConverter, Bot

import main
import models.models
from models.models import *


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")
class TimeCommands(commands.Cog):
    presencecounter = 0

    def __init__(self, client):
        self.client: Bot = client

    @commands.Cog.listener()
    async def on_ready(self):

        print("Time Commands Loaded")
        self.presencecounter = 0
        self.changepresence.start()

    @tasks.loop(minutes=5)
    async def changepresence(self):
        match (self.presencecounter):
            case 0:
                await self.client.change_presence(activity=nextcord.Game(name="/help"))
                self.presencecounter += 1
            case 1:
                await self.client.change_presence(activity=nextcord.Game(name="with time"))
                self.presencecounter += 1
            case 2:
                await self.client.change_presence(activity=nextcord.Game(name="with timezones"))
                self.presencecounter += 1
            case _:
                await self.client.change_presence(
                    activity=nextcord.Game(name=f"with {len(self.client.guilds)} servers"))
                self.presencecounter = 0

    @nextcord.slash_command(name="time", description="Get the time in a specific timezone")
    async def time(self, interaction: Interaction):
        if type(interaction.user) == Member:
            serversettings = Serversettings.findifexists(str(interaction.guild.id))
            if serversettings is None:
                serversettings = Serversettings(serverid =str(interaction.guild.id))
                serversettings.create()
            if serversettings.allowusertime == False:
                await interaction.send("This server has disabled this command.")
                return
        time = usertime.findifexists(str(interaction.user.id))
        if time is None:
            time = usertime(str(interaction.user.id)).create()
        f = f""" {time.userbeforetext} `{time.time()}`
        
        {time.useraftertext}"""
        embed = Embed(title=time.usertitle, description=f, colour=time.usercolor)
        embed.set_footer(text=time.userfooter)
        await interaction.send(embed=embed)

    @nextcord.slash_command(name="settime", description="Set the time settings for your custom clock")
    async def settime(self, interaction: Interaction,
                      timezone=SlashOption(description="The timezone you want to set", required=False),
                      title=SlashOption(description="The title of your clock", required=False),
                      beforetext=SlashOption(description="The text before the time", required=False),
                      aftertext=SlashOption(description="The text after the time", required=False),
                      color = SlashOption(description="The color of your clock", required=False),
                      footer=SlashOption(description="The footer of your clock", required=False)):
        settingstochange = {}
        if type(interaction.user) == Member:
            serversettings = Serversettings.findifexists(str(interaction.guild.id))
            if serversettings is None:
                serversettings = Serversettings(serverid=str(interaction.guild.id))
                serversettings.create()
            if serversettings.allowusertime == False:
                await interaction.send("This server has disabled this command.")
                return
        time = usertime.findifexists(userid=str(interaction.user.id))
        if time is None:
            time = usertime(userid=str(interaction.user.id)).create()
        if timezone is not None:
            if (time.update(usertz=timezone) is False):
                await interaction.send("Invalid timezone please try the format `America/New_York`")
                return
        if title is not None:
            settingstochange["usertitle"] = title
        if beforetext is not None:
            settingstochange["userbeforetext"] = beforetext
        if aftertext is not None:
            settingstochange["useraftertext"] = aftertext
        if footer is not None:
            settingstochange["userfooter"] = footer
        if color is not None:
            try:
                color = color.replace("#", "")
                color = int(color, 16)
                settingstochange["usercolor"] = color
            except:
                await interaction.send("Invalid color please try the format `#FFFFFF`")
                return
        changeresult = time.update(**settingstochange)
        if changeresult is False:
            await interaction.send("Settings could not be updated")
            return
        await interaction.send("Updated your time settings")

    @nextcord.slash_command(name="servertime", description="Get the time in a specific timezone for the server")
    async def servertime(self, ctx: Interaction):
        serversettings = Serversettings.findifexists(str(ctx.guild.id))
        if serversettings is None:
            serversettings = Serversettings(str(ctx.guild.id))
            serversettings.create()
        if serversettings.allowservertime == False:
            await ctx.send("This server has disabled this command.")
            return
        time = servertime.findifexists(str(ctx.guild.id))
        if time is None:
            time = servertime(str(ctx.guild.id)).create()
        f = f"""{time.serverbeforetext} `{time.time()}`
        
        {time.serveraftertext}"""
        embed = Embed(title=time.servertitle, description=f, colour=time.servercolor)
        embed.set_footer(text=time.serverfooter)
        await ctx.send(embed=embed)

    @nextcord.slash_command(name="setservertime", description="Set the time for the server",
                            default_member_permissions=Permissions(manage_guild = True))
    async def setservertime(self, ctx: Interaction,
                            timezone=SlashOption(description="The timezone you want to set", required=False),
                            title=SlashOption(description="The title of your clock", required=False),
                            beforetext=SlashOption(description="The text before the time", required=False),
                            aftertext=SlashOption(description="The text after the time", required=False),
                            color = SlashOption(description="The color of your clock", required=False),
                            footer=SlashOption(description="The footer of your clock", required=False)):
        serversettings = Serversettings.findifexists(str(ctx.guild.id))
        if serversettings is None:
            serversettings = Serversettings(str(ctx.guild.id))
        serversettings.create()
        if serversettings.allowservertime == False:
            await ctx.send("This server has disabled this command.")
            return
        time = servertime.findifexists(str(ctx.guild.id))
        if time is None:
            time = servertime(str(ctx.guild.id)).create()
        if timezone is not None:
            if (time.update(servertz=timezone) is False):
                await ctx.send("Invalid timezone please try the format `America/New_York`")
                return
        if title is not None:
            time.update(servertitle=title)
        if beforetext is not None:
            time.update(serverbeforetext=beforetext)
        if aftertext is not None:
            time.update(serveraftertext=aftertext)
        if footer is not None:
            time.update(serverfooter=footer)
        if color is not None:
            try:
                color = int(color.replace("#", ""))
            except:
                await ctx.send("Invalid color please try a hex value like `#fa00ff`")
                return
            if time.update(servercolor=color) is False:
                await ctx.send("Invalid color please try a hex value like `#fa00ff`")
                return
        await ctx.send("Updated the server time settings")

    @nextcord.slash_command(name="allowedtimezones",description="Get a list of all allowed timezones")
    async def allowedtimezones(self, ctx: Interaction):
        await ctx.send("https://en.wikipedia.org/wiki/List_of_tz_database_time_zones")

    @nextcord.slash_command(name="membertime",
                            description="Get the time in a specific timezone for a member in a server",dm_permission=False)
    async def membertime(self, ctx: Interaction):
        time = MemberTime.findifexists(serverid=str(ctx.guild.id), userid=str(ctx.user.id))
        serversettings = Serversettings.findifexists(str(ctx.guild.id))
        if serversettings is None:
            serversettings = Serversettings(str(ctx.guild.id))
            serversettings.create()
        if serversettings.allowmembertime == False:
            await ctx.send("This server has disabled this command.")
            return
        if time is None:
            time = MemberTime(str(ctx.guild.id), userid=str(ctx.user.id)).create()
        f = f""" {time.userserverbeforetext} `{time.time()}`
            
            {time.userserveraftertext}"""
        embed = Embed(title=time.userservertitle, description=f, colour=time.userservercolor)
        embed.set_footer(text=time.userserverfooter)
        await ctx.send(embed=embed)


    @nextcord.slash_command(name="setmembertime", description="Set the time for a member in a server")
    async def setmembertime(self, interaction: Interaction,
                            timezone=SlashOption(name="timezone", description="The timezone you want to set",
                                                 required=False),
                            title=SlashOption(name="title", description="The title of your clock", required=False),
                            beforetext=SlashOption(name="beforetext",description="The text before the time", required=False),
                            aftertext=SlashOption(name="aftertext",description="The text after the time", required=False),
                            color = SlashOption(name="color",description="The color of your clock", required=False),
                            footer=SlashOption(description="The footer of your clock", required=False)):
        serversettings = Serversettings.findifexists(str(interaction.guild.id))
        if serversettings is None:
            serversettings = Serversettings(str(interaction.guild.id))
            serversettings.create()
        if serversettings.allowmembertime == False:
            await interaction.send("This server has disabled this command.",ephemeral=True)
            return
        time = MemberTime.findifexists(serverid=str(interaction.guild.id), userid=str(interaction.user.id))
        if time is None:
            time = MemberTime(serverid=str(interaction.guild.id), userid=str(interaction.user.id)).create()

        settingstochange = {}
        if timezone is not None:
            if timezone not in pytz.all_timezones:
                await interaction.send("Invalid timezone please try the format `America/New_York`")
                return
            settingstochange["membertz"] = timezone
        if title is not None:
            settingstochange["membertitle"] = title
        if beforetext is not None:
            settingstochange["memberbeforetext"] = beforetext
        if aftertext is not None:
            settingstochange["memberaftertext"] = aftertext
        if footer is not None:
            settingstochange["memberfooter"] = footer
        if color is not None:
            try:
                color = int(color.replace("#", ""))
            except:
                await interaction.send("Invalid color please try a hex value like `#fa00ff`")
                return
            settingstochange["membercolor"] = color
        changeresult = time.update(**settingstochange)
        if changeresult is False:
            await interaction.send("Settings were not changed")
            return
        await interaction.send("Updated the member time settings")





    @nextcord.slash_command(name="serversettings", description="Get the settings for the server")
    async def server_settings(self, ctx: Interaction):
        settings = Serversettings.findifexists(str(ctx.guild.id))
        if settings is None:
            settings = Serversettings(str(ctx.guild.id)).create()
        permemojis = (":x:",":white_check_mark:")
        f = f"""**User Time:** {permemojis[settings.allowusertime]}\n**Server Time:** {permemojis[settings.allowservertime]}\n**Member Time:** {permemojis[settings.allowmembertime]}
            
            Only people with the manage server permission can change these settings"""
        embed = Embed(title="Server Settings", description=f, colour=main.rebeccapink)
        embed.set_footer(text="To change these settings use /setserversettings")
        await ctx.send(embed=embed)


    @nextcord.slash_command(name="setserversettings", description="Set the settings for the server",
                            default_member_permissions=Permissions(manage_guild = True))
    async def set_server_settings(self, ctx: Interaction, allowusertime :str = SlashOption(
                                                                                description="Whether or not to enable the user time command",
                                                                                required=False,choices=["True","False"]),
                                  allowservertime : str =SlashOption(
                                                          description="Whether or not to enable the server time command",
                                                          required=False,choices=["True","False"]), allowmembertime : str = SlashOption(
                                                                                                   description="Whether or not to enable the member time command",
                                                                                                   required=False,choices=["True","False"])):
        settings = Serversettings.findifexists(serverid=str(ctx.guild.id))
        if settings is None:
            settings = Serversettings(str(ctx.guild.id)).create()
        settingstochange = {}
        if allowusertime is not None:
            settingstochange["allowusertime"] = str2bool(allowusertime)
        if allowservertime is not None:
            settingstochange["allowservertime"] = str2bool(allowservertime)
        if allowmembertime is not None:
            settingstochange["allowmembertime"] = str2bool(allowmembertime)
        print(settingstochange)
        changeresult = settings.update(**settingstochange)
        if changeresult is False:
            await ctx.send("Settings were not changed")
            return
        await ctx.send("Updated the server settings")




    @nextcord.slash_command(name="requestdatadeletion", description="Request the deletion of your data from the database of this bot.")
    async def request_data_deletion(self, interaction: Interaction):
        interaction.response.send_message("Are you sure you want to delete your data from the database of this bot? This will delete all of your data from the database of this bot. This action cannot be undone.", ephemeral=True)
        def check(interaction):
            return interaction.user == interaction.user and interaction.channel == interaction.channel
        try:
            interaction = await self.client.wait_for("interaction", check=check, timeout=60)
        except asyncio.TimeoutError:
            await interaction.response.send_message("Timed out.", ephemeral=True)
        else:
            if interaction.data["name"] == "yes":
                await interaction.response.send_message("Deleted your data from the database of this bot.", ephemeral=True)
                usertime.findifexists(userid=str(interaction.user.id)).delete()
                if type(interaction.user) == nextcord.Member:
                    MemberTime.findifexists(serverid=str(interaction.guild.id), userid=str(interaction.user.id)).delete()
            else:
                await interaction.response.send_message("Cancelled the deletion of your data from the database of this bot.", ephemeral=True)

    @nextcord.slash_command(name="help", description="Get help for the bot")
    async def help(self, ctx: Interaction):
        f = """**User Time:** `/usertime` `/setusertime`\n**Server Time:** `/servertime` `/setservertime`\n**Member Time:** `/membertime` `/setmembertime`\n**Server Settings:** `/serversettings` `/setserversettings`, Only people with the manage server permission can change these settings\n**Request Data Deletion:** `/requestdatadeletion`"""
        embed = Embed(title="Help", description=f, colour=main.rebeccapink)
        await ctx.send(embed=embed)


    @nextcord.slash_command(name="ping", description="Get the ping of the bot")
    async def ping(self, ctx: Interaction):
        await ctx.send(f"Pong! `{round(self.client.latency * 1000)}ms`")


def setup(client):
    client.add_cog(TimeCommands(client))
