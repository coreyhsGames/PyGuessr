import discord, platform, time, datetime, json
from discord.ext import commands
from psutil import Process, virtual_memory

with open("config.json") as f:
     config = json.load(f)

client = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

    global startTime
    startTime = time.time()

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="🔧 Getting Reworked!"))

def get_bot_uptime():
        uptime = str(datetime.timedelta(seconds=int(round(time.time()-startTime))))
        return uptime

@client.command()
async def stats(ctx):
    proc = Process()
    with proc.oneshot():
        # Versions
        python_version = platform.python_version()
        discordpy_version = discord.__version__

        # Memory
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)
    
    em = discord.Embed(title=f"{client.user}'s Statistics", description="Gets <@937842334350053386>'s statistics.", colour=0xBA55D3)
    em.add_field(name="Bot Version",
                        value=f"🐍 Python: **{python_version}**\n 💻 Discord.PY: **{discordpy_version}**", inline=False)
    em.add_field(name="Uptime & Hardware",
                        value=f"🕒 Bot Uptime: **{get_bot_uptime()}**\n🧠 Memory: **{round(mem_usage, 1)}MB ({mem_of_total * 100:.0f}%)**", inline=False)
    await ctx.reply(embed=em)

client.run(config['token'])