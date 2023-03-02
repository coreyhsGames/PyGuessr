import discord, platform, time, datetime, json, os
from discord.ext import commands
from psutil import Process, virtual_memory

with open("config.json") as f:
     config = json.load(f)

client = commands.Bot(command_prefix=config['prefix'], intents=discord.Intents.all())
client.remove_command('help')

async def load_extensions():
    for filename in os.listdir('cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')

@client.event
async def on_ready():
    print(f"Logged in as {client.user}.")

    await load_extensions()

    global uptime_start_time
    uptime_start_time = time.time()

    await client.change_presence(activity=discord.Activity(type = discord.ActivityType.playing, name = "🔧 Getting Reworked!"))

# Grabs time
def get_bot_uptime():
        uptime = str(datetime.timedelta(seconds=int(round(time.time() - uptime_start_time))))
        return uptime

@client.command()
async def stats(ctx):
    ping_start_time = time.time()
    proc = Process()
    with proc.oneshot():
        # Versions
        python_version = platform.python_version()
        discordpy_version = discord.__version__

        # Memory
        mem_total = virtual_memory().total / (1024**2)
        mem_of_total = proc.memory_percent()
        mem_usage = mem_total * (mem_of_total / 100)

        # Ping
        ping = round((client.latency), 2)
    
    # Embed Setup
    em = discord.Embed(title = f"{client.user.name}'s Statistics", description = "Gets <@937842334350053386>'s statistics.", colour = 0xBA55D3)
    em.add_field(name="Bot Version",
                        value = f"🐍 Python: **{python_version}**\n 💻 Discord.PY: **{discordpy_version}**", inline = False)
    em.add_field(name = "Uptime & Hardware",
                        value = f"🕒 Bot Uptime: **{get_bot_uptime()}**\n🧠 Memory: **{round(mem_usage, 1)}MB ({mem_of_total * 100:.0f}%)**\n📶 Ping: **{ping} seconds**", inline = False)
    msg = await ctx.reply(embed = em)

    # Response Time
    ping_end_time = time.time()
    response_time = round((ping_end_time - ping_start_time), 2)

    updated_em = discord.Embed(title = f"{client.user.name}'s Statistics", description = "Gets <@937842334350053386>'s statistics.", colour = 0xBA55D3)
    updated_em.add_field(name = "Bot Version",
                        value = f"🐍 Python: **{python_version}**\n 💻 Discord.PY: **{discordpy_version}**", inline = False)
    updated_em.add_field(name = "Uptime & Hardware",
                        value = f"🕒 Bot Uptime: **{get_bot_uptime()}**\n🧠 Memory: **{round(mem_usage, 1)}MB ({mem_of_total * 100:.0f}%)**\n📶 Ping: **{ping} seconds**\n⌚ Response Time: **{response_time} seconds**", inline = False)
    await msg.edit(embed = updated_em)

client.run(config['token'])