import discord, os, requests, logging
from discord.ext import commands
from mctools import PINGClient
bot = commands.Bot(commands.when_mentioned_or("el!"))
logging.basicConfig(filename='logger.log', level=logging.INFO)
bot.remove_command("help")
@bot.command(help="Pings a server. Usage - ping <ip> [port, defaults to 25565]. If the minecraft server doesn't exist, your message will be deleted.")
async def ping(ctx, ip, port=25565):
    try:
        ping = PINGClient(host=ip, timeout=5, port=port)
        ping.stop()
        stats = ping.get_stats()
        motd = ""
        try:
            motd = "".join([motd["text"] for motd in requests.get(f"https://eu.mc-api.net/v3/server/ping/{ip}").json()["description"]["extra"]])
        except KeyError:
            motd = "No MOTD."
        except:
            motd = requests.get(f"https://eu.mc-api.net/v3/server/ping/{ip}").json()["description"]["text"]
        stats_embed = discord.Embed(title=ip.upper(), description=motd, color=0x76a5af)
        stats_embed.add_field(name="Max", value=f"{stats['players']['online']}/{stats['players']['max']}")
        stats_embed.add_field(name="Players", value="\n".join(f"`{player[0][:-4]}`" for player in stats['players']['sample']))
        stats_embed.add_field(name="Version", value=stats['version']['name'])
        stats_embed.add_field(name="Info", value="[TheOnlyWayUp](https://twitch.tv/TheOnlyWayUp)  |  [Invite The bot](https://discord.com/oauth2/authorize?client_id=893908485891317800&scope=bot+applications.commands&permissions=274878000128)  \|  [View the Code](https://github.com/TheOnlyWayUp/MinecraftServerInfo-Discord)")
        await ctx.reply(embed=stats_embed, mention_author=False)
    except Exception as e:
        stats_embed = discord.Embed(title="Error, couldn't retreive information.", description=f"Cause: {e}.", color=0xcc6666)
        stats_embed.add_field(name="Info", value="[TheOnlyWayUp](https://twitch.tv/TheOnlyWayUp)  |  [Invite The bot](https://discord.com/oauth2/authorize?client_id=893908485891317800&scope=bot+applications.commands&permissions=274878000128)  \|  [View the Code](https://github.com/TheOnlyWayUp/MinecraftServerInfo-Discord)")
        await ctx.reply(embed=stats_embed, mention_author=False)
        await ctx.reply(embed=stats_embed, delete_after=5, mention_author=False)
        await ctx.message.delete()

@bot.command()
async def help(ctx):
    hembed = discord.Embed(title="Want help? You've come to the right place :D", description="Made by TheOnlyWayup#1231", color=0xbbcdff)
    hembed.add_field(name="ping", value="el!ping <put the ip here> [optional - put port here]", inline=False)
    hembed.add_field(name="Info", value="[TheOnlyWayUp](https://twitch.tv/TheOnlyWayUp)  |  [Invite The bot](https://discord.com/oauth2/authorize?client_id=893908485891317800&scope=bot+applications.commands&permissions=274878000128)  \|  [View the Code](https://github.com/TheOnlyWayUp/MinecraftServerInfo-Discord)")
    await ctx.reply(embed=hembed, mention_author=False)

@bot.event
async def on_ready():
    print("Ready.")

bot.run(os.environ["token"])
