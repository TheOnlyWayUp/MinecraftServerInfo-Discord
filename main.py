import discord, os, requests, dns.resolver, logging
from discord.ext import commands
from mctools import *
bot = commands.Bot(commands.when_mentioned_or("el!"))
logging.basicConfig(filename='logger.log', level=logging.INFO)

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
        await ctx.reply(embed=stats_embed, mention_author=False)
    except Exception as e:
        await ctx.message.delete()

@bot.event
async def on_ready():
    print("Ready.")

bot.run(os.environ["token"])
