import discord, json, random
from discord.ext import commands
from pymongo import MongoClient

country_list = open("./country-list.txt").read().splitlines()

country_data = {
    # Country Name, Hemisphere, Continent, Population, Avg. Temp
    "Afghanistan": "Northern, Asia, 38.9m, 12.60",
    "Albania": "Northern, Europe, 2.8m, 11.40",
    "Algeria": "Northern, Africa, 43.8m, 22.50",
    "Andorra": "Northern, Europe, 55,000, 7.60",
    "Angola": "Southern, Africa, 32.8m, 21.55"
}

class countryle(commands.Cog):
    def __init__(self, client):
        self.client = client

    with open("./config.json") as f:
        config = json.load(f)

    cluster = MongoClient(config['c01password'])

    global db_countryle
    db_countryle = cluster['pyguesser']['countryle']

    @commands.command(aliases=['countryle'])
    async def play_countryle(self, ctx):
        puzzle_id = random_puzzle_id()
        embed = generate_puzzle_embed(puzzle_id)
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_msg(self, message: discord.Message):
        print(self.client)
        print(self.client.user.id)
        ref = message.reference
        if not ref or not isinstance(ref.resolved, discord.Message):
            return
        parent = ref.resolved

        print(self.client)
        if parent.author.id != self.client.user.id:
            return
        
        if not parent.embeds:
            return
        
        embed = parent.embeds[0]
        
        if not is_valid_country(message.content):
            await message.reply("Sorry! This country doesn't exist. :(", delete_after=5)
            await message.delete(delay=5)
            return
        
        print("yes")
        embed = update_embed(embed, message .content)
        await parent.edit(embed=embed)

        try:
            await message.delete()
        except Exception:
            pass

    
def generate_puzzle_embed(puzzle_id: int) -> discord.Embed:
    embed = discord.Embed(title="Countryle")
    embed.description = f"🌐 Hemisphere | <:earth_oceania:1080012117035450408> Continent | 👩🏼‍🤝‍🧑🏿 Population | 🌡 Avg. Temp"

    global guess1, guess2, guess3, guess4, guess5, guess6
    guess1 = embed.add_field(name="Guess 1:", value="", inline=True)
    guess2 = embed.add_field(name="Guess 2:", value="", inline=True)
    guess3 = embed.add_field(name="Guess 3:", value="", inline=True)
    guess4 = embed.add_field(name="Guess 4:", value="", inline=True)
    guess5 = embed.add_field(name="Guess 5:", value="", inline=True)
    guess6 = embed.add_field(name="Guess 6:", value="", inline=True)


    embed.set_footer(text=f"Game ID: {puzzle_id}\nTo play, use the command **pycountryle**!\nTo guess, reply to this message with a valid country.")
    return embed

def is_valid_country(word: str) -> bool:
    return word.lower() in country_list

def random_puzzle_id() -> int:
    return random.randint(0, len(country_list) - 1)

'''
def generate_blanks(start, end):
    str = ""
    for i in range(start, end):
        i += 1
        str = f"{str}\n**ATTEMPT {i}:**"
    return str
'''

def generate_guessed_country(guess, answer, puzzle_id):
    correct_country_values = country_data[puzzle_id]
    correct_country_values_split = correct_country_values.split(", ")

    global correct_hemisphere, correct_continent, correct_population, correct_avg_temp

    correct_hemisphere = correct_country_values_split[0]
    correct_continent = correct_country_values_split[1]
    correct_population = correct_country_values_split[2]
    correct_avg_temp = correct_country_values_split[3]

    guessed_country_values = country_data[f"{guess}"]
    guessed_country_values_split = guessed_country_values.split(", ")

    global guessed_hemisphere, guessed_continent, guessed_population, guessed_avg_temp

    guessed_hemisphere = guessed_country_values_split[0]
    guessed_continent = guessed_country_values_split[1]
    guessed_population = guessed_country_values_split[2]
    guessed_avg_temp = guessed_country_values_split[3]

    global hemisphere_str, continent_str, population_str, avg_temp_str

    if guessed_hemisphere == correct_hemisphere:
        hemisphere_str = f"{guessed_hemisphere} ✅"
    else:
        hemisphere_str = f"{guessed_hemisphere} ❌"
    
    if guessed_continent == correct_continent:
        continent_str = f"{guessed_continent} ✅"
    else:
        continent_str = f"{guessed_continent} ❌"

    if guessed_population == correct_population:
        population_str = f"{guessed_population} ✅"
    elif guessed_population < correct_population:
        population_str = f"{guessed_population} ⬆"
    elif guessed_population > correct_population:
        population_str = f"{guessed_population} ⬇"
    
    if guessed_avg_temp == correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp} ✅"
    elif guessed_avg_temp < correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp} ⬆"
    elif guessed_avg_temp > correct_avg_temp:
        avg_temp_str = f"{guessed_avg_temp} ⬇"
    
    return f"{hemisphere_str} | {continent_str} | {population_str} | {avg_temp_str}"


def update_embed(embed: discord.Embed, guess: str) -> discord.Embed:
    puzzle_id = int(embed.footer.text.split()[1])
    answer = country_list[puzzle_id]
    guessed_result = generate_guessed_country(guess, answer, puzzle_id)
    embed.fields[0]["value"] = f"{guess}\n{guessed_result}"
    return embed

async def setup(client):
    await client.add_cog(countryle(client))