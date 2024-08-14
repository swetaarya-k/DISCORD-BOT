print(f'\033[0;34mInitializing Bot...\033[0m')
__version__ = '0.0.0'
from typing import Optional
import aiohttp
from console import fg
from datetime import timedelta
from nextcord import Interaction, SlashOption, ChannelType
from nextcord.abc import GuildChannel
from nextcord.ext import commands, application_checks
from nextcord.interactions import Interaction
from nextcord.ui import Button, View
import random
import requests
import nextcord
from dotenv import load_dotenv
import os
import giphy_client
from giphy_client.rest import ApiException
import random
import replicate
import asyncio

load_dotenv()
token=os.getenv('TOKEN')
imagine = os.getenv("REPLICATE_API_TOKEN")

intents = nextcord.Intents.all()
intents.members = True

game= nextcord.Game("B.Tech CSE")
bot = commands.Bot(command_prefix="-", intents=intents, activity=game)

#bot.remove_command('help')


@bot.event
async def on_ready():
    bot.session = aiohttp.ClientSession()
    print(f'Bot Version: {fg.lightgreen}{__version__}{fg.default}')
    print(f'Connected to bot: {fg.lightgreen}{bot.user.name}{fg.default}')
    print(f'Bot ID: {fg.lightgreen}{bot.user.id}{fg.default}')
    print(
    f'I\'m in {fg.blue}{str(len(bot.guilds))}{fg.default} server{"s" if len(bot.guilds) > 1 else ""}!'
  )

@bot.event
async def on_member_join(member: nextcord.Member):
    embed = nextcord.Embed(title=f"WELCOME TO {member.guild.name}",description=f"{member.mention} has joined the server 🥳")
    embed.set_thumbnail(url=f"{member.avatar}")
    await bot.get_channel(1100657517928906794).send(embed=embed)

abusive_words = ['one', 'two', 'three','xxx']

@bot.event
async def on_message(message : nextcord.Member):
    if not message.author.bot:
        content = message.content.lower()
        embed = nextcord.Embed(title=f'{message.author.name}, please refrain from using abusive language.')
        for word in abusive_words:
            if word in content:
                await message.delete()
                await message.channel.send(embed=embed)
                break

        await bot.process_commands(message)

#app_commands
@bot.user_command()
async def memberinfo(interaction: nextcord.Interaction, member: nextcord.Member):
    try:  
        embed= nextcord.Embed(title=member,description=f"ID: {member.id}")
        embed.add_field(name="Joined Discord", value=member.created_at.strftime("**Date:** %d/%m/%Y **Time:** %H:%M:%S"), inline=False)
        embed.add_field(name="Roles", value=", ".join([role.mention for role in member.roles]), inline=False)
        embed.add_field(name="Badges", value=", ".join([badge.name for badge in member.public_flags.all()]), inline=False)
        embed.add_field(name="Activity", value=member.activity, inline=False)
        embed.set_thumbnail(url=member.avatar.url)
        await interaction.response.send_message(embed=embed)
    except:
        embed=nextcord.Embed(description="```You cannot see this users info or user may be offline```")
        await interaction.response.send_message(embed=embed)

#help_commands
class help_button(View):
    def __init__(self):
        super().__init__()

    @nextcord.ui.button(label="Moderation", style=nextcord.ButtonStyle.green, emoji="🔧")    
    async def button1(self,button, interaction : Interaction):  
        #button.disabled = True    
        embed1=nextcord.Embed(title="Moderation Slash_commands", description="Here all the available commands", color = nextcord.Color.blue())
        embed1.add_field(name="🔧Moderation Commands:", value=" `ping` `purge` `ban` `kick` `mute`",inline=False)
        embed1.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.edit_message(embed=embed1)
    @nextcord.ui.button(label="Fun", style=nextcord.ButtonStyle.blurple, emoji="🦦")
    async def button2(self, button, interaction : Interaction):
        #button.disabled = True  
        embed2=nextcord.Embed(title="Fun Slash_commands", description="Here all the available commands", color = nextcord.Color.green())
        embed2.add_field(name="🦦Fun Commands:", value="`neko` `smug` `cuddle` `pet` `feed` `hug` `slap` `tickle` `meow` `wallpaper` `foxgirl` `lizard` `baka`",inline=False)
        embed2.add_field(name="🎮Game", value="`8ball`")
        embed2.add_field(name="💠Imagination", value="`imagine`")
        embed2.set_footer(text=f"Requested by {interaction.user}")
        await interaction.response.edit_message(embed=embed2)

@bot.slash_command(description="Shows all the available commands")
async def help(interaction : Interaction):
    view = help_button()
    view.add_item(Button(label="INVITE ME",url="https://discord.com/api/oauth2/authorize?client_id=1055834582995456070&permissions=8&scope=bot%20applications.commands", style=nextcord.ButtonStyle.blurple))
    view.add_item(Button(label="Help Server",url="https://discord.gg/JE4MQZ9PQP", style=nextcord.ButtonStyle.link))
    embed=nextcord.Embed(title=f"{bot.user.name} Help\nSlash_commands ", description="Click below buttons to show commands ⬇️ ⬇️")
    embed.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=embed, view=view)

#slash_commands
'''random_and_fun_commands'''
@bot.slash_command( name="ping", description="Show you the latency of bot")
async def ping(interaction : Interaction):
    embed=nextcord.Embed(title=f'**Pong!** : `{round(bot.latency * 1000)}`ms', color=nextcord.Color.green())
    await interaction.response.send_message(embed=embed)



'''Moderation_commands'''
@bot.slash_command()
@application_checks.has_permissions(manage_messages=True)
async def purge(interaction : Interaction, amount : int):
    L = 101
    if amount > L :
        await interaction.response.send_message("you can not clear more than 100 messages...!!", ephemeral=True)
    else :
        a = await interaction.channel.purge(limit=amount)
        await interaction.response.send_message(f"{len(a)} messages cleared...!!", ephemeral=True)

@purge.error
async def purge_error(ctx, error):
    if isinstance (error, application_checks.ApplicationMissingPermissions):
        embed=nextcord.Embed(description="```You need `manage message` permission to run this command```")
        await ctx.send(embed=embed)
    else:
        embed=nextcord.Embed(description="```Something went wrong. Please try again..!!```")
        await ctx.send(embed=embed)

@bot.slash_command(name="ban", description="ban a member.")
@application_checks.has_permissions(ban_members = True)
async def ban(interaction : Interaction, member :
               nextcord.Member = SlashOption(name="ban",
                                             description="provide a member"),
                                             reason : str = SlashOption(name="reason", 
                                             description=" provide a reasone", required=False)):
        
        
        if not reason : reason = "no reason provided"
        await member.ban(reason=reason)
        await interaction.response.send_message(f"```{member} is ban by {interaction.user.mention} for reasone = {reason}```")

@ban.error
async def ban_error(ctx, error):
    if isinstance (error, application_checks.ApplicationMissingPermissions):
        embed=nextcord.Embed(description="```You need `ban_members` permission to run this command```")
        await ctx.send(embed=embed)

    if application_checks.has_permissions():
        embed=nextcord.Embed(description="```You can't ban an Admin```")
        await ctx.send(embed=embed, ephemeral=True)
    else:
        embed=nextcord.Embed(description="```Something went wrong. Please try again..!!```")
        await ctx.send(embed=embed, ephemeral=True)

@bot.slash_command(name="kick", description="kick a member.")
@application_checks.has_permissions(kick_members = True)
async def kick(interaction : Interaction, member : nextcord.Member = SlashOption(name="kick",description="provide a member"), reason : str = SlashOption(name="reason", description=" provide a reasone", required=False)):
    
        if not reason : reason = "No reason provided"
        await member.kick(reason=reason)
        await interaction.response.send_message(f"```{member} is kick by {interaction.user.mention} for reason = {reason}```")

@kick.error
async def kick_error(ctx, error):
    if isinstance (error, application_checks.ApplicationMissingPermissions):
        embed=nextcord.Embed(description="```You need `kick_members` permission to run this command```")
        await ctx.send(embed=embed, ephemeral=True)
    if application_checks.has_permissions():
        embed=nextcord.Embed(description="```You can't kick an Admin```")
        await ctx.send(embed=embed, ephemeral=True)
    else:
        embed=nextcord.Embed(description="```Something went wrong. Please try again..!!```")
        await ctx.send(embed=embed, ephemeral=True)

@bot.slash_command()
@application_checks.has_permissions(moderate_members = True)
async def mute(interaction : Interaction, member : nextcord.Member, reason : str = SlashOption(required=False), days : int = SlashOption(max_value=28, default=00, required=False), hours : int = SlashOption(default=00, required=False), minutes : int = SlashOption(default=00, required=False), seconds : int = SlashOption(default=60, required=False)):
    duration = timedelta(days = days, hours = hours, minutes = minutes, seconds = seconds)
    if member.id == interaction.user.id :
        await interaction.response.send_message("You cannot mute yourself!", ephemeral=True)
    elif member.guild_permissions.administrator :
        await interaction.response.send_message("You cannot mute an admin", ephemeral=True)
    
    elif duration >= timedelta(days = 28): #added to check if time exceeds 28 days
        await interaction.response.send_message("I can't mute someone for more than 28 days!", ephemeral = True)
    else:
        if not reason : reason = "No reason provided"
        await member.timeout(duration, reason=reason)
        mute = nextcord.Embed(description=f"```{interaction.user} timed out {member}({member.id})``` for  {days} days || {hours}:{minutes}:{seconds}")
        await interaction.response.send_message(embed=mute)


@mute.error
async def mute_error(ctx, error):
    if isinstance (error, application_checks.ApplicationMissingPermissions):
        embed=nextcord.Embed(description=f"```{error} (╯°□°)╯︵ ┻━┻```")
        await ctx.send(embed=embed)
    else:
        raise error


'''api_commands & Fun'''

@bot.slash_command()
async def gif(ctx : Interaction, *,search="Nezuko"):
    api_key="TwOuL3yltcQBuSmdrpJGJy7NXJCevy3j"
    api_instance = giphy_client.DefaultApi()
    try: 
    # Search Endpoint
        
        api_response = api_instance.gifs_search_get(api_key, search, limit=10, rating='R')
        lst = list(api_response.data)
        giff = random.choice(lst)
        emb = nextcord.Embed(title=search)
        emb.set_image(url = f'https://media.giphy.com/media/{giff.id}/giphy.gif')
        await ctx.response.send_message(embed=emb)
    except ApiException as e:
        print("Exception when calling DefaultApi->gifs_search_get: %s\n" % e)

@bot.slash_command(name="8ball",description="gives you an random answer")
async def Eightball(interaction : Interaction , question : str):
    response= ["It is certain.",
              "It is decidedly so.",
              "Without a doubt.",
              "Yes definitely.",
              "You may rely on it.",
              "As I see it, yes.",
              "Most likely.",
              "Outlook good.",
              "Yes.",
              "Signs point to yes.",

              "Reply hazy, try again.",
              "Better not tell you now.",
              "Cannot predict now.",
              "Concentrate and ask again.",
              "Don't count on it.",
              "My reply is no.",
              "My sources say no.",
              "Outlook not so good.",
              "Very doubtful."]
    embed=nextcord.Embed(title=":8ball:**8ball**", description=f":white_small_square: **Question:** {question}\n:white_small_square:**Answer: **{random.choice(response)}",color=nextcord.Color.random())
    embed.set_thumbnail(url="https://media.tenor.com/USELDeKObkgAAAAi/8ball-activity.gif")
    await interaction.response.send_message(embed=embed)

#API integration
@bot.slash_command()
async def waifu(interaction : Interaction):
    r=requests.get(f"http://api.nekos.fun:8080/api/waifu")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['image'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def neko(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/neko")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def smug(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/smug")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)


@bot.slash_command()

async def kiss(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/kiss")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def cuddle(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/cuddle")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def pat(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/pat")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def feed(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/feed")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def hug(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/hug")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def slap(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/slap")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def tickle(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/tickle")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def meow(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/meow")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command() 
async def wallpaper(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/wallpaper")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def foxgirl(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/fox_girl")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def lizard(interaction : Interaction):
    r=requests.get(f"https://nekos.life/api/v2/img/lizard")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['url'])
    await interaction.response.send_message(embed=m)

@bot.slash_command()
async def baka(interaction : Interaction):
    r=requests.get(f"http://api.nekos.fun:8080/api/baka")
    res = r.json()
    m = nextcord.Embed(color=nextcord.Color.random())
    m.set_image(url=res['image'])
    await interaction.response.send_message(embed=m)


api_key = 'e12a1221ba504c13af0120533233105'  # Replace with your WeatherAPI.com API key


@bot.slash_command(name="weather", description="Tells you about the weather")
async def weather(ctx: Interaction, city: str):
    try:
        url = f'https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=no'
        response = requests.get(url)
        data = response.json()

        if 'current' in data:
            current = data['current']
            temperature = current['temp_c']
            condition = current['condition']['text']
            humidity = current['humidity']

            embed = nextcord.Embed(title=f'Weather in {city}', color=0x00ff00)
            embed.add_field(name='Temperature', value=f'{temperature}°C')
            embed.add_field(name='Condition', value=condition)
            embed.add_field(name='Humidity', value=f'{humidity}%')

            await ctx.response.send_message(embed=embed)
        else:
            await ctx.send(f'Failed to retrieve weather data for {city}. Please try again later.')

    except Exception as e:
        await ctx.send(f'Failed to retrieve weather data for {city}: {e}')


class downloadview(nextcord.ui.View):
    def __init__(self):
        super().__init__()
        

@bot.slash_command()
async def imagine(ctx : Interaction, prompt : str, models : str = SlashOption(
    choices=["stable-diffusion","openjourney","erlich","min-dalle","Waifu Diffusion"], required=True
)):
    view = downloadview()
    await ctx.response.defer()
    if models == "stable-diffusion":
        model = replicate.models.get("stability-ai/stable-diffusion")
        version = model.versions.get("db21e45d3f7023abc2a46ee38a23973f6dce16bb082a930b0c49861f96d1e5bf")
        image = version.predict(prompt=prompt)[0]

        embed = nextcord.Embed(title="Generated Image",color=nextcord.Color.random())
        embed.add_field(name="Prompt", value=prompt)
        embed.set_image(url=image)
        view.add_item(Button(label="Download",url=image,style=nextcord.ButtonStyle.link,emoji="⬇️"))
        await ctx.send(embed=embed,view=view)



    if models == "openjourney":
        model = replicate.models.get("prompthero/openjourney")
        version = model.versions.get("9936c2001faa2194a261c01381f90e65261879985476014a0a37a334593a05eb")
        image = version.predict(prompt=prompt)[0]

        embed = nextcord.Embed(title="Generated Image",color=nextcord.Color.random())
        embed.add_field(name="Prompt", value=prompt)
        embed.set_image(url=image)
        view.add_item(Button(label="Download",url=image,style=nextcord.ButtonStyle.link,emoji="⬇️"))
        await ctx.send(embed=embed,view=view)



    if models == "erlich":
        model = replicate.models.get("laion-ai/erlich")
        version = model.versions.get("92fa143ccefeed01534d5d6648bd47796ef06847a6bc55c0e5c5b6975f2dcdfb")
        image = version.predict(prompt=prompt)[0]

        embed = nextcord.Embed(title="Generated Image",color=nextcord.Color.random())
        embed.add_field(name="Prompt", value=prompt)
        embed.set_image(url=image)
        view.add_item(Button(label="Download",url=image,style=nextcord.ButtonStyle.link,emoji="⬇️"))
        await ctx.send(embed=embed,view=view)



    if models == "min-dalle":
        model = replicate.models.get("kuprel/min-dalle")
        version = model.versions.get("2af375da21c5b824a84e1c459f45b69a117ec8649c2aa974112d7cf1840fc0ce")
        image = version.predict(prompt=prompt)[0]

        embed = nextcord.Embed(title="Generated Image",color=nextcord.Color.random())
        embed.add_field(name="Prompt", value=prompt)
        embed.set_image(url=image)
        view.add_item(Button(label="Download",url=image,style=nextcord.ButtonStyle.link,emoji="⬇️"))
        await ctx.send(embed=embed,view=view)



    if models == "Waifu Diffusion":
        model = replicate.models.get("cjwbw/waifu-diffusion")
        version = model.versions.get("25d2f75ecda0c0bed34c806b7b70319a53a1bccad3ade1a7496524f013f48983")
        image = version.predict(prompt=prompt)[0]

        embed = nextcord.Embed(title="Generated Image",color=nextcord.Color.random())
        embed.add_field(name="Prompt", value=prompt)
        embed.set_image(url=image)
        embed.set_footer(text=f"Requested by {Interaction.user}")
        view.add_item(Button(label="Download",url=image,style=nextcord.ButtonStyle.link,emoji="⬇️"))
        await ctx.send(embed=embed,view=view)


@imagine.error
async def imagine_error(ctx, error):
    try:
        embed=nextcord.Embed(description=f"```Something went wrong : {error}```")
        await ctx.send(embed=embed)
    except:
        embed=nextcord.Embed(description="```Try again your request may contain NSFW content.```")
        await ctx.send(embed=embed)




bot.run(token)