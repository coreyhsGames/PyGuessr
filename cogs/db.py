import discord, json
from discord.ext import commands
from pymongo import MongoClient

class database(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("./config.json") as f:
        config = json.load(f)

    cluster = MongoClient(config['c01password'])

    global db_countryle
    db_countryle = cluster['pyguesser']['countryle']

    @commands.group(invoke_without_command = True)
    async def lb(self, ctx):
        await ctx.reply("**In order to see the leaderboards, please specify the game. Currently there is only 1 avaliable game. The list is below:\n• Countryle: `pylb countryle`**")

    @lb.command(name = "countryle")
    async def lb_countryle(self, ctx):
        rankings = db_countryle.find().sort("wins", -1)
        i = 1
        embed = discord.Embed(title = "PyGuessr Leaderboard", description = f"Displays the top 10 people in all of Discord in PyGuessr's Countryle, sorted by most wins.", colour = 0xBA55D3)
        for x in rankings:
            try:
                temp = ctx.guild.get_member(x["id"])
                temp_wins = x["wins"]
                temp_games_played = x["games_played"]

                field_stats = f'👑 **Wins:** {temp_wins} | 🗓️ **Games Played:** {temp_games_played}'
                if i == 1:
                    i = "🥇"
                    embed.add_field(name = f"{i}: {temp.name}", value = field_stats, inline = False)
                    i = 2
                elif i == 2:
                    i = "🥈"
                    embed.add_field(name = f"{i}: {temp.name}", value = field_stats, inline = False)
                    i = 3
                elif i == 3: 
                    i = "🥉"
                    embed.add_field(name = f"{i}: {temp.name}", value = field_stats, inline = False)
                    i = 4
                else:
                    if i == 4:
                        i = 4
                        embed.add_field(name = f"{i}: {temp.name}", value = field_stats, inline = False)
                        i += 1
                    else:
                        embed.add_field(name = f"{i}: {temp.name}", value = field_stats, inline = False)
                        i += 1
            except:
                pass
            if i == 10 + 1:
                break
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(database(client))