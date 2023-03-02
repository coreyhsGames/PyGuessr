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

    @commands.command(aliases=['top', 'lb'])
    async def leaderboard(self, ctx, num_of_players: int = 5):
        if num_of_players > 20:
            await ctx.reply("In order to make the message not too long, you can only see the top 20 people in the server. ❌")
            return

        rankings = db_countryle.find().sort("wins", -1)
        i = 1
        embed = discord.Embed(title = "PyGuessr Leaderboard", description = f"Displays the best players (top {num_of_players}) in all of Discord in PyGuessr's Countryle, sorted by most wins.", colour = 0xBA55D3)
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
            if i == num_of_players + 1:
                break
        await ctx.reply(embed=embed)

async def setup(client):
    await client.add_cog(database(client))