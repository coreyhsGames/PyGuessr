import discord, json, time
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
        await ctx.reply("In order to see the leaderboards, please specify the game. Currently there is only 1 avaliable game.**\n\nThe list is below:\n• Countryle: `pylb countryle`**")

    @lb.command(name = "countryle")
    async def lb_countryle(self, ctx):
        rankings = db_countryle.find().sort("wins", -1)
        i = 1
        embed = discord.Embed(title = "Countryle Leaderboard", description = f"Displays the top 10 people in all of Discord in PyGuessr's Countryle, sorted by most wins.", colour = 0xBA55D3)
        for x in rankings:
            try:
                temp = self.client.get_user(x["id"])
                temp_wins = x["wins"]
                temp_games_played = x["games_played"]
                temp_best_guess = x["best_guess"]

                field_stats = f'👑 **Wins:** {temp_wins} | 🗓️ **Games Played:** {temp_games_played} | 🔥 **Best Game: ** {temp_best_guess}'
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

    @commands.group(invoke_without_command = True)
    async def stats(self, ctx):
        await ctx.reply("In order to see a users stats, please specify the game. Currently there is only 1 avaliable game.**\n\nThe list is below:\n• Countryle: `pystats countryle [user]`**")
    
    @stats.command(name = "countryle")
    async def stats_countryle(self, ctx, user: discord.Member = None):
        if user is None:
            user = ctx.author

        if not ctx.author.bot and user.id != self.client.user.id:
            user_stats = db_countryle.find_one({"id": user.id})
            if user_stats is None:
                insert = {"id": user.id, "wins": 0, "games_played": 0, "best_guess": 0}
                db_countryle.insert_one(insert)

                time.sleep(3)

                user_stats = db_countryle.find_one({"id": user.id})
            
            temp_wins = user_stats["wins"]
            temp_games_played = user_stats["games_played"]
            temp_best_guess = user_stats["best_guess"]

            embed = discord.Embed(title = f"{user.name}'s Countryle Stats", colour = 0xBA55D3)
            embed.add_field(name = "User:", value = user.mention, inline = False)
            embed.add_field(name = "👑 Wins:", value = f"{temp_wins}", inline = True)
            embed.add_field(name = "🗓️ Games Played:", value = f"{temp_games_played}", inline = True)
            embed.add_field(name = "🔥 Best Game:", value = f"{temp_best_guess}")
            embed.set_thumbnail(url = user.display_avatar)
            await ctx.reply(embed = embed)

async def setup(client):
    await client.add_cog(database(client))